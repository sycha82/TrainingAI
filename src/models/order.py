"""주문 데이터 모델"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Order:
    """물류센터 주문을 나타내는 클래스

    Attributes:
        order_id: 주문 고유 ID
        weight: 주문 무게 (kg)
        volume: 주문 부피 (m³)
        item_count: 주문 품목 수
        fragile: 깨지기 쉬운 물품 여부
        priority: 우선순위 (1: 낮음, 2: 보통, 3: 높음, 4: 긴급)
        destination_zone: 목적지 구역 (A, B, C 등)
        order_type: 주문 유형 (standard, express, bulk)
    """
    order_id: str
    weight: float
    volume: float
    item_count: int
    fragile: bool = False
    priority: int = 2
    destination_zone: str = "A"
    order_type: str = "standard"

    def __post_init__(self):
        """입력 값 검증"""
        if self.weight < 0:
            raise ValueError("무게는 0 이상이어야 합니다")
        if self.volume < 0:
            raise ValueError("부피는 0 이상이어야 합니다")
        if self.item_count < 1:
            raise ValueError("품목 수는 1 이상이어야 합니다")
        if self.priority not in [1, 2, 3, 4]:
            raise ValueError("우선순위는 1-4 사이여야 합니다")

    def get_density(self) -> float:
        """밀도 계산 (kg/m³)"""
        if self.volume == 0:
            return 0
        return self.weight / self.volume

    def is_heavy(self, threshold: float = 20.0) -> bool:
        """무거운 주문인지 확인"""
        return self.weight > threshold

    def is_bulk(self) -> bool:
        """대량 주문인지 확인"""
        return self.order_type == "bulk" or self.item_count > 50
