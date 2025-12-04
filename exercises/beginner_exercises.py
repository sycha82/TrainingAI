"""초급 연습 문제 - 기본 개념 익히기"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.order import Order
from src.models.facility import Facility


def exercise_1():
    """연습 1: 주문 객체 생성하기"""
    print("="*70)
    print("연습 1: 주문 객체 생성하기")
    print("="*70)
    print("""
과제: 다음 정보를 가진 주문을 생성하세요.
  - 주문 ID: "MY-ORDER-001"
  - 무게: 12.5 kg
  - 부피: 0.6 m³
  - 품목 수: 8개
  - 깨지기 쉬움: True
  - 우선순위: 3
  - 목적지 구역: "B"
  - 주문 유형: "express"

힌트: Order(...) 클래스를 사용하세요.
""")

    # TODO: 여기에 코드를 작성하세요
    # order = Order(...)

    # ============ 정답 (주석 해제하여 확인) ============
    # order = Order(
    #     order_id="MY-ORDER-001",
    #     weight=12.5,
    #     volume=0.6,
    #     item_count=8,
    #     fragile=True,
    #     priority=3,
    #     destination_zone="B",
    #     order_type="express"
    # )
    # print("\n✅ 생성된 주문:")
    # print(order)
    # print(f"\n밀도: {order.get_density():.2f} kg/m³")

    print("\n💡 정답을 보려면 코드의 주석을 해제하세요!")


def exercise_2():
    """연습 2: 주문 메서드 사용하기"""
    print("\n" + "="*70)
    print("연습 2: 주문 메서드 사용하기")
    print("="*70)

    order = Order(
        order_id="EX-002",
        weight=25.0,
        volume=1.2,
        item_count=60,
        fragile=False,
        priority=1,
        destination_zone="C",
        order_type="bulk"
    )

    print(f"\n주문 정보:")
    print(order)

    print(f"""
과제: 위 주문에 대해 다음 정보를 출력하세요.

1. 밀도 (density) - order.get_density() 사용
2. 무거운 주문인지 (is_heavy) - order.is_heavy() 사용
3. 대량 주문인지 (is_bulk) - order.is_bulk() 사용

힌트: print(f"밀도: {{order.get_density():.2f}} kg/m³")
""")

    # TODO: 여기에 코드를 작성하세요

    # ============ 정답 (주석 해제하여 확인) ============
    # print("\n📊 주문 분석:")
    # print(f"  - 밀도: {order.get_density():.2f} kg/m³")
    # print(f"  - 무거운 주문? {order.is_heavy()}")
    # print(f"  - 대량 주문? {order.is_bulk()}")


def exercise_3():
    """연습 3: 설비 객체 생성하기"""
    print("\n" + "="*70)
    print("연습 3: 설비 객체 생성하기")
    print("="*70)
    print("""
과제: 다음 정보를 가진 설비를 생성하세요.
  - 설비 ID: "MY-FAC-001"
  - 이름: "나의 첫 컨베이어"
  - 설비 유형: "conveyor"
  - 최대 무게: 50.0 kg
  - 최대 부피: 2.0 m³
  - 깨지기 쉬운 물품 처리: False
  - 속도 등급: 3
  - 지원 구역: ["A", "B", "C"]
  - 사용 가능: True

힌트: Facility(...) 클래스를 사용하세요.
""")

    # TODO: 여기에 코드를 작성하세요
    # facility = Facility(...)

    # ============ 정답 (주석 해제하여 확인) ============
    # facility = Facility(
    #     facility_id="MY-FAC-001",
    #     name="나의 첫 컨베이어",
    #     facility_type="conveyor",
    #     max_weight=50.0,
    #     max_volume=2.0,
    #     can_handle_fragile=False,
    #     speed_rating=3,
    #     supported_zones=["A", "B", "C"],
    #     available=True
    # )
    # print("\n✅ 생성된 설비:")
    # print(facility)


def exercise_4():
    """연습 4: 설비가 주문을 처리할 수 있는지 확인하기"""
    print("\n" + "="*70)
    print("연습 4: 설비가 주문을 처리할 수 있는지 확인")
    print("="*70)

    order = Order(
        order_id="TEST-ORDER",
        weight=15.0,
        volume=0.7,
        item_count=10,
        fragile=True,
        priority=2,
        destination_zone="A",
        order_type="standard"
    )

    facility = Facility(
        facility_id="TEST-FAC",
        name="테스트 설비",
        facility_type="sorter",
        max_weight=30.0,
        max_volume=1.5,
        can_handle_fragile=True,
        speed_rating=3,
        supported_zones=["A", "B"],
        available=True
    )

    print(f"\n주문: {order.order_id} (무게: {order.weight}kg, 깨지기 쉬움: {order.fragile})")
    print(f"설비: {facility.name} (최대: {facility.max_weight}kg, 깨지기 쉬운 물품: {facility.can_handle_fragile})")

    print(f"""
과제: 이 설비가 주문을 처리할 수 있는지 확인하세요.

힌트: facility.can_handle_order(order) 메서드를 사용하세요.
""")

    # TODO: 여기에 코드를 작성하세요
    # can_handle = ...
    # print(f"\n처리 가능? {can_handle}")

    # ============ 정답 (주석 해제하여 확인) ============
    # can_handle = facility.can_handle_order(order)
    # print(f"\n✅ 처리 가능? {can_handle}")
    #
    # if can_handle:
    #     utilization = facility.get_capacity_utilization(order)
    #     print(f"📊 용량 사용률: {utilization:.2%}")


def exercise_5():
    """연습 5: 여러 주문과 설비 비교하기"""
    print("\n" + "="*70)
    print("연습 5: 여러 주문과 설비 비교하기")
    print("="*70)

    orders = [
        Order("ORD-1", 5.0, 0.2, 3, fragile=False, priority=2, destination_zone="A", order_type="standard"),
        Order("ORD-2", 30.0, 1.5, 50, fragile=False, priority=1, destination_zone="C", order_type="bulk"),
        Order("ORD-3", 2.0, 0.1, 1, fragile=True, priority=4, destination_zone="B", order_type="express"),
    ]

    facility = Facility(
        facility_id="FAC-TEST",
        name="만능 설비",
        facility_type="sorter",
        max_weight=40.0,
        max_volume=2.0,
        can_handle_fragile=True,
        speed_rating=4,
        supported_zones=["A", "B", "C"],
        available=True
    )

    print(f"\n설비: {facility.name}")
    print(f"  - 최대 용량: {facility.max_weight}kg, {facility.max_volume}m³")
    print(f"  - 깨지기 쉬운 물품 처리: {facility.can_handle_fragile}")

    print(f"""
과제: 각 주문에 대해 다음을 출력하세요.
  1. 처리 가능 여부
  2. 처리 가능하다면 용량 사용률

힌트: for 문을 사용하여 orders를 순회하세요.
""")

    # TODO: 여기에 코드를 작성하세요
    # for order in orders:
    #     ...

    # ============ 정답 (주석 해제하여 확인) ============
    # print("\n📊 주문별 분석:\n")
    # for order in orders:
    #     can_handle = facility.can_handle_order(order)
    #     print(f"{order.order_id} (무게: {order.weight}kg, 부피: {order.volume}m³)")
    #     if can_handle:
    #         utilization = facility.get_capacity_utilization(order)
    #         print(f"  ✅ 처리 가능 - 용량 사용률: {utilization:.2%}")
    #     else:
    #         print(f"  ❌ 처리 불가")
    #     print()


def main():
    """모든 연습 문제 실행"""
    print("\n🎓 초급 연습 문제 - 기본 개념 익히기\n")
    print("각 연습 문제의 TODO 부분에 코드를 작성한 후,")
    print("주석을 해제하여 정답을 확인할 수 있습니다.\n")

    input("엔터를 눌러 시작하세요...")

    exercise_1()
    input("\n다음 연습으로 가려면 엔터...")

    exercise_2()
    input("\n다음 연습으로 가려면 엔터...")

    exercise_3()
    input("\n다음 연습으로 가려면 엔터...")

    exercise_4()
    input("\n다음 연습으로 가려면 엔터...")

    exercise_5()

    print("\n" + "="*70)
    print("🎉 초급 연습 완료!")
    print("="*70)
    print("\n다음 단계: intermediate_exercises.py를 확인하세요!")


if __name__ == "__main__":
    main()
