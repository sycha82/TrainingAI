"""설비 매칭 AI 엔진"""

from typing import List, Dict, Optional, Tuple
from ..models.order import Order
from ..models.facility import Facility


class FacilityMatcher:
    """주문에 가장 적합한 설비를 찾는 AI 엔진

    이 엔진은 여러 속성을 점수화하여 최적의 설비를 선택합니다.
    각 요소마다 가중치를 부여하여 종합 점수를 계산합니다.
    """

    def __init__(
        self,
        weight_capacity: float = 0.25,      # 용량 활용률 가중치
        weight_speed: float = 0.25,         # 속도 가중치
        weight_fragile: float = 0.20,       # 깨지기 쉬운 물품 처리 가중치
        weight_zone: float = 0.15,          # 구역 매칭 가중치
        weight_type: float = 0.15           # 설비 유형 매칭 가중치
    ):
        """
        Args:
            weight_capacity: 용량 활용률 가중치 (효율성)
            weight_speed: 처리 속도 가중치
            weight_fragile: 깨지기 쉬운 물품 처리 능력 가중치
            weight_zone: 목적지 구역 일치 가중치
            weight_type: 설비 유형 매칭 가중치
        """
        # 가중치 정규화 (합계가 1이 되도록)
        total = weight_capacity + weight_speed + weight_fragile + weight_zone + weight_type
        self.weight_capacity = weight_capacity / total
        self.weight_speed = weight_speed / total
        self.weight_fragile = weight_fragile / total
        self.weight_zone = weight_zone / total
        self.weight_type = weight_type / total

    def calculate_score(self, order: Order, facility: Facility) -> float:
        """주문과 설비의 매칭 점수 계산 (0.0 ~ 1.0)

        Args:
            order: 주문 객체
            facility: 설비 객체

        Returns:
            매칭 점수 (0.0 ~ 1.0, 높을수록 좋음)
        """
        # 기본적으로 처리 불가능하면 0점
        if not facility.can_handle_order(order):
            return 0.0

        score = 0.0

        # 1. 용량 활용률 점수 (적절한 활용률이 높은 점수)
        # 너무 크거나 너무 작으면 비효율적
        utilization = facility.get_capacity_utilization(order)
        if 0.5 <= utilization <= 0.8:  # 최적 구간
            capacity_score = 1.0
        elif 0.3 <= utilization < 0.5:  # 약간 낮은 활용
            capacity_score = 0.7 + (utilization - 0.3) * 1.5
        elif 0.8 < utilization <= 1.0:  # 약간 높은 활용
            capacity_score = 1.0 - (utilization - 0.8) * 1.5
        else:  # 너무 낮은 활용
            capacity_score = utilization / 0.3 * 0.7
        score += capacity_score * self.weight_capacity

        # 2. 속도 점수 (우선순위가 높으면 빠른 설비 선호)
        speed_requirement = self._get_speed_requirement(order)
        if facility.speed_rating >= speed_requirement:
            speed_score = facility.speed_rating / 4.0  # 정규화
        else:
            speed_score = (facility.speed_rating / speed_requirement) * 0.5
        score += speed_score * self.weight_speed

        # 3. 깨지기 쉬운 물품 처리 점수
        if order.fragile:
            fragile_score = 1.0 if facility.can_handle_fragile else 0.0
        else:
            fragile_score = 0.8  # 깨지기 쉽지 않으면 중간 점수
        score += fragile_score * self.weight_fragile

        # 4. 목적지 구역 점수
        zone_score = 1.0 if order.destination_zone in facility.supported_zones else 0.0
        score += zone_score * self.weight_zone

        # 5. 설비 유형 점수
        type_score = self._calculate_type_score(order, facility)
        score += type_score * self.weight_type

        return min(score, 1.0)  # 최대 1.0으로 제한

    def _get_speed_requirement(self, order: Order) -> int:
        """주문의 속도 요구사항 계산"""
        if order.priority == 4:  # 긴급
            return 4
        elif order.priority == 3:  # 높음
            return 3
        elif order.order_type == "express":
            return 3
        elif order.priority == 2:  # 보통
            return 2
        else:
            return 1

    def _calculate_type_score(self, order: Order, facility: Facility) -> float:
        """설비 유형과 주문 특성의 매칭 점수 계산"""
        # 설비 유형별 선호도 매핑
        type_preferences = {
            "bulk": {"conveyor": 1.0, "sorter": 0.6, "robot": 0.4, "manual": 0.3},
            "express": {"robot": 1.0, "sorter": 0.8, "conveyor": 0.5, "manual": 0.3},
            "standard": {"sorter": 1.0, "conveyor": 0.9, "robot": 0.7, "manual": 0.5}
        }

        order_type = order.order_type
        facility_type = facility.facility_type

        if order_type in type_preferences:
            return type_preferences[order_type].get(facility_type, 0.5)
        return 0.5  # 기본값

    def find_best_facility(
        self,
        order: Order,
        facilities: List[Facility]
    ) -> Optional[Tuple[Facility, float]]:
        """주문에 가장 적합한 설비 찾기

        Args:
            order: 주문 객체
            facilities: 사용 가능한 설비 리스트

        Returns:
            (최적 설비, 점수) 튜플, 없으면 None
        """
        best_facility = None
        best_score = 0.0

        for facility in facilities:
            score = self.calculate_score(order, facility)
            if score > best_score:
                best_score = score
                best_facility = facility

        if best_facility is None:
            return None

        return (best_facility, best_score)

    def rank_facilities(
        self,
        order: Order,
        facilities: List[Facility],
        top_n: int = 5
    ) -> List[Tuple[Facility, float]]:
        """주문에 적합한 설비들을 점수순으로 정렬

        Args:
            order: 주문 객체
            facilities: 사용 가능한 설비 리스트
            top_n: 반환할 상위 설비 수

        Returns:
            (설비, 점수) 튜플 리스트 (점수 내림차순)
        """
        scored_facilities = []

        for facility in facilities:
            score = self.calculate_score(order, facility)
            if score > 0:  # 처리 가능한 설비만
                scored_facilities.append((facility, score))

        # 점수순으로 정렬 (내림차순)
        scored_facilities.sort(key=lambda x: x[1], reverse=True)

        return scored_facilities[:top_n]

    def batch_match(
        self,
        orders: List[Order],
        facilities: List[Facility]
    ) -> Dict[str, Optional[Tuple[Facility, float]]]:
        """여러 주문을 한번에 매칭

        Args:
            orders: 주문 리스트
            facilities: 설비 리스트

        Returns:
            {order_id: (설비, 점수) 또는 None} 딕셔너리
        """
        results = {}

        for order in orders:
            match = self.find_best_facility(order, facilities)
            results[order.order_id] = match

        return results
