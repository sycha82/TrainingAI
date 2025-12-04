"""기본 테스트 - unittest 사용법 배우기"""

import unittest
import sys
import os

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.order import Order
from src.models.facility import Facility
from src.engine.matcher import FacilityMatcher


class TestOrder(unittest.TestCase):
    """주문(Order) 클래스 테스트"""

    def test_order_creation(self):
        """주문 생성 테스트"""
        order = Order(
            order_id="TEST-001",
            weight=10.0,
            volume=0.5,
            item_count=5,
            fragile=True,
            priority=3,
            destination_zone="A",
            order_type="express"
        )

        self.assertEqual(order.order_id, "TEST-001")
        self.assertEqual(order.weight, 10.0)
        self.assertTrue(order.fragile)

    def test_order_density(self):
        """밀도 계산 테스트"""
        order = Order(
            order_id="TEST-002",
            weight=20.0,
            volume=2.0,
            item_count=10
        )

        density = order.get_density()
        self.assertEqual(density, 10.0)  # 20kg / 2m³ = 10

    def test_order_is_heavy(self):
        """무거운 주문 판별 테스트"""
        heavy_order = Order("TEST-003", weight=30.0, volume=1.0, item_count=5)
        light_order = Order("TEST-004", weight=5.0, volume=0.5, item_count=3)

        self.assertTrue(heavy_order.is_heavy())
        self.assertFalse(light_order.is_heavy())

    def test_order_is_bulk(self):
        """대량 주문 판별 테스트"""
        bulk_order = Order("TEST-005", weight=10.0, volume=1.0, item_count=100)
        normal_order = Order("TEST-006", weight=10.0, volume=1.0, item_count=10)

        self.assertTrue(bulk_order.is_bulk())
        self.assertFalse(normal_order.is_bulk())

    def test_invalid_weight(self):
        """잘못된 무게 입력 테스트"""
        with self.assertRaises(ValueError):
            Order("TEST-007", weight=-5.0, volume=1.0, item_count=5)

    def test_invalid_priority(self):
        """잘못된 우선순위 입력 테스트"""
        with self.assertRaises(ValueError):
            Order("TEST-008", weight=10.0, volume=1.0, item_count=5, priority=5)


class TestFacility(unittest.TestCase):
    """설비(Facility) 클래스 테스트"""

    def test_facility_creation(self):
        """설비 생성 테스트"""
        facility = Facility(
            facility_id="FAC-001",
            name="테스트 컨베이어",
            facility_type="conveyor",
            max_weight=50.0,
            max_volume=2.0,
            speed_rating=3
        )

        self.assertEqual(facility.facility_id, "FAC-001")
        self.assertEqual(facility.max_weight, 50.0)
        self.assertEqual(facility.speed_rating, 3)

    def test_can_handle_order(self):
        """주문 처리 가능 여부 테스트"""
        facility = Facility(
            facility_id="FAC-002",
            name="테스트 설비",
            facility_type="sorter",
            max_weight=30.0,
            max_volume=1.5,
            can_handle_fragile=True,
            supported_zones=["A", "B"]
        )

        # 처리 가능한 주문
        valid_order = Order("ORD-001", weight=20.0, volume=1.0, item_count=10,
                           fragile=True, destination_zone="A")
        self.assertTrue(facility.can_handle_order(valid_order))

        # 너무 무거운 주문
        heavy_order = Order("ORD-002", weight=50.0, volume=1.0, item_count=10,
                           destination_zone="A")
        self.assertFalse(facility.can_handle_order(heavy_order))

        # 지원하지 않는 구역
        wrong_zone_order = Order("ORD-003", weight=20.0, volume=1.0, item_count=10,
                                destination_zone="C")
        self.assertFalse(facility.can_handle_order(wrong_zone_order))

    def test_capacity_utilization(self):
        """용량 사용률 계산 테스트"""
        facility = Facility(
            facility_id="FAC-003",
            name="테스트",
            facility_type="conveyor",
            max_weight=100.0,
            max_volume=10.0
        )

        order = Order("ORD-004", weight=50.0, volume=5.0, item_count=10)
        utilization = facility.get_capacity_utilization(order)

        # 무게 50/100 = 0.5, 부피 5/10 = 0.5, 최대값 = 0.5
        self.assertEqual(utilization, 0.5)


class TestMatcher(unittest.TestCase):
    """매칭 엔진(Matcher) 테스트"""

    def setUp(self):
        """각 테스트 전에 실행 - 공통 데이터 준비"""
        self.matcher = FacilityMatcher()

        self.facilities = [
            Facility("FAC-1", "빠른 로봇", "robot", 20.0, 1.0,
                    can_handle_fragile=True, speed_rating=4, supported_zones=["A", "B"]),
            Facility("FAC-2", "대형 컨베이어", "conveyor", 100.0, 5.0,
                    can_handle_fragile=False, speed_rating=2, supported_zones=["C"]),
            Facility("FAC-3", "일반 분류기", "sorter", 30.0, 1.5,
                    can_handle_fragile=True, speed_rating=3, supported_zones=["A", "B", "C"]),
        ]

    def test_find_best_facility(self):
        """최적 설비 찾기 테스트"""
        order = Order("ORD-001", weight=10.0, volume=0.5, item_count=5,
                     fragile=True, priority=4, destination_zone="A", order_type="express")

        result = self.matcher.find_best_facility(order, self.facilities)

        self.assertIsNotNone(result)
        facility, score = result
        self.assertGreater(score, 0)

    def test_no_matching_facility(self):
        """매칭 불가능한 경우 테스트"""
        # 너무 무거운 주문
        order = Order("ORD-002", weight=200.0, volume=10.0, item_count=5,
                     destination_zone="A")

        result = self.matcher.find_best_facility(order, self.facilities)
        self.assertIsNone(result)

    def test_rank_facilities(self):
        """설비 순위 매기기 테스트"""
        order = Order("ORD-003", weight=15.0, volume=0.8, item_count=10,
                     destination_zone="A")

        ranked = self.matcher.rank_facilities(order, self.facilities, top_n=3)

        # 최소 1개 이상의 설비가 매칭되어야 함
        self.assertGreater(len(ranked), 0)

        # 점수가 내림차순으로 정렬되어 있는지 확인
        scores = [score for _, score in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_batch_match(self):
        """일괄 매칭 테스트"""
        orders = [
            Order("ORD-1", weight=10.0, volume=0.5, item_count=5, destination_zone="A"),
            Order("ORD-2", weight=50.0, volume=2.5, item_count=50, destination_zone="C"),
            Order("ORD-3", weight=5.0, volume=0.3, item_count=3, destination_zone="B"),
        ]

        results = self.matcher.batch_match(orders, self.facilities)

        # 모든 주문에 대한 결과가 있어야 함
        self.assertEqual(len(results), len(orders))

        # 각 주문 ID가 결과에 포함되어 있어야 함
        for order in orders:
            self.assertIn(order.order_id, results)

    def test_custom_weights(self):
        """커스텀 가중치 테스트"""
        # 속도 중심 매처
        speed_matcher = FacilityMatcher(
            weight_capacity=0.1,
            weight_speed=0.5,
            weight_fragile=0.2,
            weight_zone=0.1,
            weight_type=0.1
        )

        # 가중치가 정규화되었는지 확인
        total_weight = (speed_matcher.weight_capacity +
                       speed_matcher.weight_speed +
                       speed_matcher.weight_fragile +
                       speed_matcher.weight_zone +
                       speed_matcher.weight_type)

        self.assertAlmostEqual(total_weight, 1.0, places=5)


def run_tests():
    """테스트 실행 함수"""
    # 테스트 스위트 생성
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 모든 테스트 클래스 추가
    suite.addTests(loader.loadTestsFromTestCase(TestOrder))
    suite.addTests(loader.loadTestsFromTestCase(TestFacility))
    suite.addTests(loader.loadTestsFromTestCase(TestMatcher))

    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 결과 요약
    print("\n" + "="*70)
    print("테스트 결과 요약")
    print("="*70)
    print(f"실행된 테스트: {result.testsRun}개")
    print(f"성공: {result.testsRun - len(result.failures) - len(result.errors)}개")
    print(f"실패: {len(result.failures)}개")
    print(f"오류: {len(result.errors)}개")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
