"""머신러닝 기반 설비 매칭 엔진

.NET 개발자를 위한 개념 설명:
-----------------------------
C#에서 ML.NET을 사용하는 것과 유사합니다.

1. 학습(Training): 과거 데이터로 패턴 학습
   - C#: mlContext.Model.Fit(trainingData)
   - Python: model.fit(X_train, y_train)

2. 예측(Prediction): 새 데이터에 대해 추론
   - C#: predictionEngine.Predict(newData)
   - Python: model.predict(new_data)

3. 모델 저장/로드
   - C#: mlContext.Model.Save(model, stream)
   - Python: joblib.dump(model, filename)
"""

import os
from typing import List, Optional, Tuple
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

from ..models.order import Order
from ..models.facility import Facility


class MLMatcher:
    """
    머신러닝 기반 설비 매칭 엔진

    Random Forest Classifier 사용:
    - 의사결정나무(Decision Tree) 여러 개를 앙상블
    - 과적합(Overfitting) 방지
    - 특성 중요도(Feature Importance) 확인 가능

    .NET 비유:
    - C#의 클래스와 동일한 구조
    - 인스턴스 필드(self._model 등)는 C#의 private 필드와 같음
    """

    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: Optional[int] = None,
        random_state: int = 42
    ):
        """
        Args:
            n_estimators: 의사결정나무 개수 (더 많을수록 정확하지만 느림)
            max_depth: 트리의 최대 깊이 (None이면 제한 없음)
            random_state: 재현 가능성을 위한 시드
        """
        # ML 모델 (C#의 private 필드와 비슷)
        self._model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1  # 모든 CPU 코어 사용
        )

        # 설비 ID를 숫자로 변환하는 인코더
        # C#의 Dictionary<string, int>와 비슷한 역할
        self._label_encoder = LabelEncoder()

        # 학습 완료 여부
        self._is_trained = False

        # 학습에 사용된 설비 목록
        self._facilities = []

    def _extract_features(self, order: Order) -> np.ndarray:
        """
        주문에서 특성(Feature) 추출

        ML 모델은 숫자만 이해할 수 있으므로,
        Order 객체를 숫자 배열로 변환합니다.

        .NET 비유:
        - Order 객체 -> double[] 배열로 변환
        - C#의 Linq Select()와 비슷한 개념

        Returns:
            특성 벡터 [weight, volume, item_count, ...]
        """
        features = [
            order.weight,                                    # 무게
            order.volume,                                    # 부피
            order.item_count,                                # 품목 수
            order.get_density(),                             # 밀도
            1.0 if order.fragile else 0.0,                   # 깨지기 쉬운지 (boolean -> float)
            float(order.priority),                           # 우선순위
            1.0 if order.is_heavy() else 0.0,                # 무거운 주문인지
            1.0 if order.is_bulk() else 0.0,                 # 대량 주문인지
            # 목적지 구역을 숫자로 (A=1, B=2, C=3)
            ord(order.destination_zone) - ord('A') + 1,
            # 주문 유형을 숫자로
            {"standard": 1, "express": 2, "bulk": 3}.get(order.order_type, 0)
        ]

        return np.array(features)

    def _extract_features_batch(self, orders: List[Order]) -> np.ndarray:
        """
        여러 주문의 특성을 한번에 추출

        .NET 비유:
        - List<Order> -> double[,] 2차원 배열
        - LINQ의 Select().ToArray()와 비슷
        """
        return np.array([self._extract_features(order) for order in orders])

    def train(self, orders: List[Order], labels: List[str]) -> dict:
        """
        과거 데이터로 모델 학습

        Args:
            orders: 과거 주문 리스트
            labels: 각 주문에 대해 실제로 선택된 설비 ID

        Returns:
            학습 결과 통계

        .NET 비유:
        - public TrainingResult Train(List<Order> orders, List<string> labels)
        - Entity Framework로 DB에서 가져온 과거 데이터를 학습
        """
        if len(orders) != len(labels):
            raise ValueError("주문 수와 레이블 수가 일치하지 않습니다")

        if len(orders) == 0:
            raise ValueError("학습 데이터가 없습니다")

        print(f"\n🎓 머신러닝 모델 학습 시작...")
        print(f"   학습 데이터: {len(orders)}개")

        # 1. 특성 추출 (Order -> 숫자 배열)
        X = self._extract_features_batch(orders)
        print(f"   특성 차원: {X.shape[1]}개")

        # 2. 레이블 인코딩 (설비 ID 문자열 -> 숫자)
        # "FAC-001" -> 0, "FAC-002" -> 1, ...
        y = self._label_encoder.fit_transform(labels)
        unique_facilities = len(self._label_encoder.classes_)
        print(f"   설비 종류: {unique_facilities}개")

        # 3. 모델 학습 (실제 ML이 일어나는 부분!)
        self._model.fit(X, y)
        self._is_trained = True

        # 4. 학습 성능 평가
        train_score = self._model.score(X, y)

        print(f"✅ 학습 완료!")
        print(f"   학습 정확도: {train_score:.2%}")

        # 5. 특성 중요도 출력 (어떤 특성이 중요한지)
        feature_names = [
            "weight", "volume", "item_count", "density",
            "fragile", "priority", "is_heavy", "is_bulk",
            "destination_zone", "order_type"
        ]
        importances = self._model.feature_importances_

        print(f"\n   특성 중요도 (높을수록 중요):")
        for name, importance in sorted(
            zip(feature_names, importances),
            key=lambda x: x[1],
            reverse=True
        )[:5]:
            print(f"     - {name:20s}: {importance:.4f}")

        return {
            "num_samples": len(orders),
            "num_features": X.shape[1],
            "num_classes": unique_facilities,
            "train_accuracy": train_score,
            "feature_importances": dict(zip(feature_names, importances))
        }

    def predict(self, order: Order, facilities: List[Facility]) -> Optional[Tuple[Facility, float]]:
        """
        새 주문에 대해 최적 설비 예측

        Args:
            order: 새로운 주문
            facilities: 사용 가능한 설비 리스트

        Returns:
            (예측된 설비, 확신도) 또는 None

        .NET 비유:
        - public (Facility, double)? Predict(Order order, List<Facility> facilities)
        - Nullable Tuple 반환
        """
        if not self._is_trained:
            raise RuntimeError("모델이 학습되지 않았습니다. train()을 먼저 호출하세요.")

        # 1. 특성 추출
        X = self._extract_features(order).reshape(1, -1)  # 2D 배열로 변환

        # 2. 예측 (실제 ML 추론!)
        # predict(): 가장 가능성 높은 클래스
        predicted_class = self._model.predict(X)[0]

        # predict_proba(): 각 클래스의 확률
        probabilities = self._model.predict_proba(X)[0]
        confidence = probabilities[predicted_class]

        # 3. 숫자 -> 설비 ID로 역변환
        facility_id = self._label_encoder.inverse_transform([predicted_class])[0]

        # 4. 설비 객체 찾기
        facility = next((f for f in facilities if f.facility_id == facility_id), None)

        if facility is None:
            # 예측된 설비가 현재 사용 가능한 설비 목록에 없음
            return None

        # 5. 실제로 처리 가능한지 확인
        if not facility.can_handle_order(order):
            # ML 모델은 처리 불가능한 설비를 예측할 수 있음
            # 이 경우 두 번째로 확률이 높은 설비를 찾거나 None 반환
            return None

        return (facility, confidence)

    def predict_top_k(
        self,
        order: Order,
        facilities: List[Facility],
        k: int = 3
    ) -> List[Tuple[Facility, float]]:
        """
        상위 k개 설비 예측

        .NET 비유:
        - public List<(Facility, double)> PredictTopK(Order order, List<Facility> facilities, int k)
        """
        if not self._is_trained:
            raise RuntimeError("모델이 학습되지 않았습니다.")

        X = self._extract_features(order).reshape(1, -1)
        probabilities = self._model.predict_proba(X)[0]

        # 확률이 높은 순서로 정렬
        top_k_indices = np.argsort(probabilities)[::-1][:k]

        results = []
        for idx in top_k_indices:
            facility_id = self._label_encoder.inverse_transform([idx])[0]
            confidence = probabilities[idx]

            facility = next((f for f in facilities if f.facility_id == facility_id), None)

            if facility and facility.can_handle_order(order):
                results.append((facility, confidence))

        return results

    def save_model(self, filepath: str):
        """
        학습된 모델을 파일로 저장

        .NET 비유:
        - C#의 Serialization과 비슷
        - mlContext.Model.Save(model, stream)
        """
        if not self._is_trained:
            raise RuntimeError("학습된 모델이 없습니다.")

        model_data = {
            'model': self._model,
            'label_encoder': self._label_encoder,
            'is_trained': self._is_trained
        }

        joblib.dump(model_data, filepath)
        print(f"✅ 모델 저장 완료: {filepath}")

    def load_model(self, filepath: str):
        """
        저장된 모델 로드

        .NET 비유:
        - C#의 Deserialization
        - mlContext.Model.Load(stream)
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {filepath}")

        model_data = joblib.load(filepath)

        self._model = model_data['model']
        self._label_encoder = model_data['label_encoder']
        self._is_trained = model_data['is_trained']

        print(f"✅ 모델 로드 완료: {filepath}")

    def evaluate(self, test_orders: List[Order], test_labels: List[str]) -> dict:
        """
        테스트 데이터로 모델 성능 평가

        .NET 비유:
        - Unit Test에서 Assert와 비슷한 개념
        - 학습 데이터가 아닌 새로운 데이터로 성능 측정
        """
        if not self._is_trained:
            raise RuntimeError("모델이 학습되지 않았습니다.")

        # 학습에 없던 레이블 필터링
        known_labels = set(self._label_encoder.classes_)
        filtered_orders = []
        filtered_labels = []

        for order, label in zip(test_orders, test_labels):
            if label in known_labels:
                filtered_orders.append(order)
                filtered_labels.append(label)

        if len(filtered_orders) == 0:
            return {"accuracy": 0.0, "correct": 0, "total": 0}

        X_test = self._extract_features_batch(filtered_orders)
        y_test = self._label_encoder.transform(filtered_labels)

        # 정확도 계산
        accuracy = self._model.score(X_test, y_test)

        # 예측 수행
        y_pred = self._model.predict(X_test)

        # 혼동 행렬 정보
        correct = np.sum(y_pred == y_test)
        total = len(y_test)

        print(f"\n📊 모델 평가 결과:")
        print(f"   테스트 데이터: {len(test_orders)}개 (학습에 있던 레이블: {total}개)")
        print(f"   정확도: {accuracy:.2%}")
        print(f"   정답: {correct}개 / {total}개")

        return {
            "accuracy": accuracy,
            "correct": int(correct),
            "total": int(total)
        }

    def get_feature_names(self) -> List[str]:
        """특성 이름 목록 반환"""
        return [
            "weight", "volume", "item_count", "density",
            "fragile", "priority", "is_heavy", "is_bulk",
            "destination_zone", "order_type"
        ]

    def get_feature_importances(self) -> dict:
        """특성 중요도 반환"""
        if not self._is_trained:
            return {}

        return dict(zip(
            self.get_feature_names(),
            self._model.feature_importances_
        ))
