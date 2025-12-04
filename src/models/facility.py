"""설비 데이터 모델"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Facility:
    """물류센터 설비를 나타내는 클래스

    Attributes:
        facility_id: 설비 고유 ID
        name: 설비 이름
        facility_type: 설비 유형 (conveyor, sorter, robot, manual)
        max_weight: 최대 처리 가능 무게 (kg)
        max_volume: 최대 처리 가능 부피 (m³)
        can_handle_fragile: 깨지기 쉬운 물품 처리 가능 여부
        speed_rating: 처리 속도 등급 (1: 느림, 2: 보통, 3: 빠름, 4: 매우 빠름)
        supported_zones: 지원하는 목적지 구역 리스트
        available: 현재 사용 가능 여부
    """
    facility_id: str
    name: str
    facility_type: str
    max_weight: float
    max_volume: float
    can_handle_fragile: bool = True
    speed_rating: int = 2
    supported_zones: List[str] = None
    available: bool = True

    def __post_init__(self):
        """초기화 후 처리"""
        if self.supported_zones is None:
            self.supported_zones = ["A", "B", "C"]  # 기본값

        if self.max_weight < 0:
            raise ValueError("최대 무게는 0 이상이어야 합니다")
        if self.max_volume < 0:
            raise ValueError("최대 부피는 0 이상이어야 합니다")
        if self.speed_rating not in [1, 2, 3, 4]:
            raise ValueError("속도 등급은 1-4 사이여야 합니다")

    def can_handle_order(self, order) -> bool:
        """주문 처리 가능 여부 확인"""
        if not self.available:
            return False

        # 무게와 부피 확인
        if order.weight > self.max_weight or order.volume > self.max_volume:
            return False

        # 깨지기 쉬운 물품 처리 가능 여부
        if order.fragile and not self.can_handle_fragile:
            return False

        # 목적지 구역 지원 여부
        if order.destination_zone not in self.supported_zones:
            return False

        return True

    def get_capacity_utilization(self, order) -> float:
        """주문에 대한 설비 용량 사용률 계산 (0.0 ~ 1.0)"""
        weight_ratio = order.weight / self.max_weight if self.max_weight > 0 else 0
        volume_ratio = order.volume / self.max_volume if self.max_volume > 0 else 0
        return max(weight_ratio, volume_ratio)
