"""머신러닝 엔진 사용 예제

.NET 개발자를 위한 가이드:
- 이 예제는 C#의 콘솔 애플리케이션과 비슷한 구조입니다
- Main() 메서드부터 시작하여 순차적으로 실행됩니다
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engine.ml_matcher import MLMatcher
from src.data.training_data_generator import TrainingDataGenerator
from src.data.sample_data import create_sample_orders, create_sample_facilities


def example_1_basic_training():
    """예제 1: 기본 학습 및 예측"""
    print("="*80)
    print("예제 1: 머신러닝 모델 학습 및 예측")
    print("="*80)

    # 1. 학습 데이터 생성
    print("\n[1단계] 학습 데이터 생성")
    print("-" * 80)
    generator = TrainingDataGenerator(seed=42)
    train_orders, train_labels = generator.generate_training_data(500)

    # 2. ML 모델 생성 및 학습
    print("\n[2단계] 머신러닝 모델 학습")
    print("-" * 80)
    ml_matcher = MLMatcher(n_estimators=100, random_state=42)
    train_result = ml_matcher.train(train_orders, train_labels)

    # 3. 새로운 주문에 대해 예측
    print("\n[3단계] 새 주문 예측")
    print("-" * 80)

    test_orders = create_sample_orders()
    facilities = generator.generate_facilities()

    for order in test_orders[:3]:  # 처음 3개만
        print(f"\n📦 주문: {order.order_id}")
        print(f"   - 무게: {order.weight:.1f}kg, 부피: {order.volume:.2f}m³")
        print(f"   - 유형: {order.order_type}, 우선순위: {order.priority}")

        result = ml_matcher.predict(order, facilities)

        if result:
            facility, confidence = result
            print(f"   ✅ 예측: {facility.name}")
            print(f"   📊 확신도: {confidence:.2%}")
        else:
            print(f"   ❌ 예측 실패")


def example_2_model_evaluation():
    """예제 2: 모델 성능 평가"""
    print("\n" + "="*80)
    print("예제 2: 모델 성능 평가 (Train vs Test)")
    print("="*80)

    generator = TrainingDataGenerator(seed=42)

    # 학습 데이터
    print("\n[1단계] 학습 데이터 생성")
    train_orders, train_labels = generator.generate_training_data(800)

    # 테스트 데이터 (학습에 사용하지 않은 새로운 데이터)
    print("\n[2단계] 테스트 데이터 생성")
    test_orders, test_labels = generator.generate_test_data(200)

    # 학습
    print("\n[3단계] 모델 학습")
    ml_matcher = MLMatcher(n_estimators=100, random_state=42)
    ml_matcher.train(train_orders, train_labels)

    # 평가
    print("\n[4단계] 모델 평가")
    print("-" * 80)
    eval_result = ml_matcher.evaluate(test_orders, test_labels)

    print(f"\n💡 해석:")
    print(f"   정확도 {eval_result['accuracy']:.2%}는")
    print(f"   모델이 새로운 주문에 대해 얼마나 잘 예측하는지를 나타냅니다.")

    if eval_result['accuracy'] > 0.8:
        print(f"   ✅ 우수한 성능입니다!")
    elif eval_result['accuracy'] > 0.6:
        print(f"   ⚠️  괜찮은 성능이지만 개선 여지가 있습니다.")
    else:
        print(f"   ❌ 성능 개선이 필요합니다.")


def example_3_feature_importance():
    """예제 3: 특성 중요도 분석"""
    print("\n" + "="*80)
    print("예제 3: 어떤 특성이 중요한가?")
    print("="*80)

    generator = TrainingDataGenerator(seed=42)
    train_orders, train_labels = generator.generate_training_data(500)

    ml_matcher = MLMatcher(n_estimators=100, random_state=42)
    ml_matcher.train(train_orders, train_labels)

    print("\n📊 특성 중요도 상위 5개:")
    print("-" * 80)

    importances = ml_matcher.get_feature_importances()
    sorted_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)

    for i, (feature, importance) in enumerate(sorted_features[:5], 1):
        bar_length = int(importance * 50)
        bar = "█" * bar_length
        print(f"{i}. {feature:20s} {bar} {importance:.4f}")

    print(f"\n💡 해석:")
    print(f"   높은 특성일수록 모델의 의사결정에 큰 영향을 미칩니다.")
    print(f"   이는 실제 물류 운영에서 중요한 요소를 나타냅니다.")


def example_4_top_k_predictions():
    """예제 4: 상위 k개 예측"""
    print("\n" + "="*80)
    print("예제 4: 상위 3개 설비 추천")
    print("="*80)

    generator = TrainingDataGenerator(seed=42)
    train_orders, train_labels = generator.generate_training_data(500)

    ml_matcher = MLMatcher(n_estimators=100, random_state=42)
    ml_matcher.train(train_orders, train_labels)

    # 테스트 주문
    test_order = create_sample_orders()[0]
    facilities = generator.generate_facilities()

    print(f"\n📦 주문 정보:")
    print(f"   - ID: {test_order.order_id}")
    print(f"   - 무게: {test_order.weight:.1f}kg, 부피: {test_order.volume:.2f}m³")
    print(f"   - 유형: {test_order.order_type}, 우선순위: {test_order.priority}")

    print(f"\n🏆 추천 설비 (상위 3개):")
    print("-" * 80)

    top_k = ml_matcher.predict_top_k(test_order, facilities, k=3)

    for i, (facility, confidence) in enumerate(top_k, 1):
        print(f"\n{i}위. {facility.name}")
        print(f"     - 확신도: {confidence:.2%}")
        print(f"     - 유형: {facility.facility_type}, 속도: {facility.speed_rating}/4")
        print(f"     - 용량: {facility.max_weight}kg, {facility.max_volume}m³")


def example_5_save_and_load():
    """예제 5: 모델 저장 및 로드"""
    print("\n" + "="*80)
    print("예제 5: 모델 저장 및 재사용")
    print("="*80)

    # 크로스 플랫폼 경로 (Windows/Linux/Mac 모두 지원)
    import tempfile
    temp_dir = tempfile.gettempdir()
    model_path = os.path.join(temp_dir, "facility_matcher_model.pkl")

    print(f"\n💾 모델 저장 경로: {model_path}")

    # 학습 및 저장
    print("\n[1단계] 모델 학습 및 저장")
    print("-" * 80)

    generator = TrainingDataGenerator(seed=42)
    train_orders, train_labels = generator.generate_training_data(300)

    ml_matcher = MLMatcher(n_estimators=50, random_state=42)
    ml_matcher.train(train_orders, train_labels)
    ml_matcher.save_model(model_path)

    # 새 인스턴스에서 로드
    print("\n[2단계] 저장된 모델 로드")
    print("-" * 80)

    new_matcher = MLMatcher()
    new_matcher.load_model(model_path)

    # 예측 테스트
    print("\n[3단계] 로드된 모델로 예측")
    print("-" * 80)

    test_order = create_sample_orders()[0]
    facilities = generator.generate_facilities()

    result = new_matcher.predict(test_order, facilities)

    if result:
        facility, confidence = result
        print(f"\n✅ 예측 성공!")
        print(f"   설비: {facility.name}")
        print(f"   확신도: {confidence:.2%}")

    print(f"\n💡 이점:")
    print(f"   - 학습은 한번만 하고 모델을 저장")
    print(f"   - 이후에는 로드해서 바로 사용 (학습 시간 절약)")
    print(f"   - C#의 직렬화(Serialization)와 비슷한 개념")


def main():
    """메인 함수"""
    print("\n" + "🤖 머신러닝 기반 설비 매칭 엔진".center(80, "="))
    print("ML이 데이터를 학습하여 패턴을 발견하고 예측합니다".center(80))
    print("="*80)

    try:
        example_1_basic_training()

        input("\n[엔터를 눌러 다음 예제로 이동...]")
        example_2_model_evaluation()

        input("\n[엔터를 눌러 다음 예제로 이동...]")
        example_3_feature_importance()

        input("\n[엔터를 눌러 다음 예제로 이동...]")
        example_4_top_k_predictions()

        input("\n[엔터를 눌러 다음 예제로 이동...]")
        example_5_save_and_load()

        print("\n" + "="*80)
        print("✨ 모든 예제 완료!")
        print("="*80)

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
