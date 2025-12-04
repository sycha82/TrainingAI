"""샘플 데이터 생성 함수"""

from typing import List
from ..models.order import Order
from ..models.facility import Facility


def create_sample_orders() -> List[Order]:
    """다양한 유형의 샘플 주문 생성"""
    return [
        # 일반 주문
        Order(
            order_id="ORD-001",
            weight=5.0,
            volume=0.2,
            item_count=3,
            fragile=False,
            priority=2,
            destination_zone="A",
            order_type="standard"
        ),
        # 긴급 주문
        Order(
            order_id="ORD-002",
            weight=2.0,
            volume=0.1,
            item_count=1,
            fragile=True,
            priority=4,
            destination_zone="B",
            order_type="express"
        ),
        # 대량 주문
        Order(
            order_id="ORD-003",
            weight=50.0,
            volume=2.5,
            item_count=100,
            fragile=False,
            priority=1,
            destination_zone="C",
            order_type="bulk"
        ),
        # 깨지기 쉬운 물품
        Order(
            order_id="ORD-004",
            weight=3.0,
            volume=0.15,
            item_count=5,
            fragile=True,
            priority=3,
            destination_zone="A",
            order_type="standard"
        ),
        # 중간 크기 빠른 배송
        Order(
            order_id="ORD-005",
            weight=10.0,
            volume=0.5,
            item_count=15,
            fragile=False,
            priority=3,
            destination_zone="B",
            order_type="express"
        ),
    ]


def create_sample_facilities() -> List[Facility]:
    """다양한 유형의 샘플 설비 생성"""
    return [
        # 고속 컨베이어 벨트
        Facility(
            facility_id="FAC-001",
            name="고속 컨베이어 A",
            facility_type="conveyor",
            max_weight=30.0,
            max_volume=1.5,
            can_handle_fragile=False,
            speed_rating=3,
            supported_zones=["A", "B"],
            available=True
        ),
        # 자동 분류기
        Facility(
            facility_id="FAC-002",
            name="자동 분류기 B",
            facility_type="sorter",
            max_weight=20.0,
            max_volume=1.0,
            can_handle_fragile=True,
            speed_rating=4,
            supported_zones=["A", "B", "C"],
            available=True
        ),
        # 로봇 픽커
        Facility(
            facility_id="FAC-003",
            name="로봇 픽커 R1",
            facility_type="robot",
            max_weight=15.0,
            max_volume=0.8,
            can_handle_fragile=True,
            speed_rating=4,
            supported_zones=["A", "B"],
            available=True
        ),
        # 대형 컨베이어 (대량 처리용)
        Facility(
            facility_id="FAC-004",
            name="대형 컨베이어 C",
            facility_type="conveyor",
            max_weight=100.0,
            max_volume=5.0,
            can_handle_fragile=False,
            speed_rating=2,
            supported_zones=["C"],
            available=True
        ),
        # 수동 처리 구역
        Facility(
            facility_id="FAC-005",
            name="수동 처리 구역 M1",
            facility_type="manual",
            max_weight=50.0,
            max_volume=2.0,
            can_handle_fragile=True,
            speed_rating=1,
            supported_zones=["A", "B", "C"],
            available=True
        ),
        # 소형 분류기
        Facility(
            facility_id="FAC-006",
            name="소형 분류기 S1",
            facility_type="sorter",
            max_weight=10.0,
            max_volume=0.5,
            can_handle_fragile=True,
            speed_rating=3,
            supported_zones=["A"],
            available=True
        ),
    ]
