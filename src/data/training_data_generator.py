"""학습 데이터 생성기 - ML 모델 훈련용"""

import random
from typing import List, Tuple
import sys
import os

# 부모 디렉토리를 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.order import Order
from src.models.facility import Facility
from src.data.sample_data import create_sample_facilities


class TrainingDataGenerator:
    """
    ML 모델 학습을 위한 과거 매칭 데이터 생성기

    실제 환경에서는 과거 운영 데이터를 사용하지만,
    여기서는 시뮬레이션으로 학습 데이터를 생성합니다.

    .NET 개발자를 위한 비유:
    - C#의 Random 데이터 생성과 비슷
    - Entity Framework로 DB에서 과거 데이터를 가져온다고 생각하면 됨
    """

    def __init__(self, seed: int = 42):
        """
        Args:
            seed: 재현 가능한 랜덤 데이터를 위한 시드
                  (C#의 new Random(seed)와 동일)
        """
        random.seed(seed)

    def generate_random_order(self, order_id: str) -> Order:
        """랜덤 주문 생성"""
        # 다양한 주문 패턴 생성
        order_types = ["standard", "express", "bulk"]
        zones = ["A", "B", "C"]

        order_type = random.choice(order_types)

        # 주문 유형에 따라 특성이 달라짐
        if order_type == "bulk":
            weight = random.uniform(30, 100)
            volume = random.uniform(1.5, 5.0)
            item_count = random.randint(50, 150)
            priority = random.choice([1, 2])
        elif order_type == "express":
            weight = random.uniform(1, 20)
            volume = random.uniform(0.1, 1.0)
            item_count = random.randint(1, 20)
            priority = random.choice([3, 4])
        else:  # standard
            weight = random.uniform(5, 30)
            volume = random.uniform(0.2, 1.5)
            item_count = random.randint(3, 40)
            priority = random.choice([1, 2, 3])

        return Order(
            order_id=order_id,
            weight=weight,
            volume=volume,
            item_count=item_count,
            fragile=random.choice([True, False]),
            priority=priority,
            destination_zone=random.choice(zones),
            order_type=order_type
        )

    def generate_facilities(self) -> List[Facility]:
        """
        실제 운영 환경과 동일한 설비 사용

        중요: ML 모델은 학습할 때 사용한 설비와 동일한 설비로 예측해야 합니다.
        따라서 sample_data.py의 설비를 사용합니다.
        """
        return create_sample_facilities()

    def simulate_expert_decision(self, order: Order, facilities: List[Facility]) -> str:
        """
        전문가의 결정을 시뮬레이션

        실제로는 과거 운영 데이터에서 '실제로 선택된 설비'를 사용하지만,
        여기서는 합리적인 규칙으로 시뮬레이션합니다.

        .NET 비유: 비즈니스 로직 레이어의 의사결정 함수
        """
        # 처리 가능한 설비만 필터링
        valid_facilities = [f for f in facilities if f.can_handle_order(order)]

        if not valid_facilities:
            return None

        # 우선순위별 전략
        if order.priority == 4:  # 긴급
            # 가장 빠른 설비 선택
            fast_facilities = [f for f in valid_facilities if f.speed_rating >= 3]
            if fast_facilities:
                return max(fast_facilities, key=lambda f: f.speed_rating).facility_id

        if order.is_bulk():  # 대량
            # 가장 큰 용량의 설비 선택
            return max(valid_facilities, key=lambda f: f.max_weight).facility_id

        if order.fragile:  # 깨지기 쉬운 물품
            # 깨지기 쉬운 물품 처리 가능한 설비 중 빠른 것
            fragile_ok = [f for f in valid_facilities if f.can_handle_fragile]
            if fragile_ok:
                return max(fragile_ok, key=lambda f: f.speed_rating).facility_id

        # 일반적인 경우: 용량 활용률이 50-80% 범위인 것 선택
        best = None
        best_score = -1

        for facility in valid_facilities:
            utilization = facility.get_capacity_utilization(order)
            # 50-80% 범위가 이상적
            if 0.5 <= utilization <= 0.8:
                score = 1.0 - abs(utilization - 0.65)
            else:
                score = 0.5 - abs(utilization - 0.65)

            if score > best_score:
                best_score = score
                best = facility

        return best.facility_id if best else valid_facilities[0].facility_id

    def generate_training_data(self, num_samples: int = 1000) -> Tuple[List[Order], List[str]]:
        """
        학습 데이터 생성

        Returns:
            (주문 리스트, 선택된 설비 ID 리스트)

        .NET 비유:
        - Tuple<List<Order>, List<string>>과 동일
        - LINQ의 Zip과 비슷한 개념
        """
        facilities = self.generate_facilities()
        orders = []
        labels = []  # ML 용어로 "정답"을 labels라고 부름

        print(f"학습 데이터 생성 중... (총 {num_samples}개)")

        for i in range(num_samples):
            if (i + 1) % 100 == 0:
                print(f"  진행: {i + 1}/{num_samples}")

            order = self.generate_random_order(f"TRAIN-{i:05d}")
            selected_facility = self.simulate_expert_decision(order, facilities)

            if selected_facility:  # 매칭 가능한 경우만 추가
                orders.append(order)
                labels.append(selected_facility)

        print(f"✅ 생성 완료: {len(orders)}개 데이터")
        return orders, labels

    def generate_test_data(self, num_samples: int = 200) -> Tuple[List[Order], List[str]]:
        """
        테스트 데이터 생성 (학습 데이터와 별도)

        ML에서는 학습 데이터와 테스트 데이터를 분리해야 합니다.
        이는 .NET에서 Unit Test와 Production 코드를 분리하는 것과 비슷합니다.
        """
        # 다른 시드로 생성 (학습 데이터와 겹치지 않게)
        original_seed = random.getstate()
        random.seed(9999)

        facilities = self.generate_facilities()
        orders = []
        labels = []

        print(f"테스트 데이터 생성 중... (총 {num_samples}개)")

        for i in range(num_samples):
            order = self.generate_random_order(f"TEST-{i:05d}")
            selected_facility = self.simulate_expert_decision(order, facilities)

            if selected_facility:
                orders.append(order)
                labels.append(selected_facility)

        random.setstate(original_seed)
        print(f"✅ 생성 완료: {len(orders)}개 데이터")
        return orders, labels


if __name__ == "__main__":
    # 간단한 테스트
    generator = TrainingDataGenerator()

    print("\n=== 학습 데이터 생성 테스트 ===\n")
    train_orders, train_labels = generator.generate_training_data(100)

    print(f"\n샘플 데이터:")
    for i in range(min(5, len(train_orders))):
        order = train_orders[i]
        label = train_labels[i]
        print(f"  {order.order_id}: {order.order_type}, {order.weight:.1f}kg -> {label}")
