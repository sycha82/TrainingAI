"""중급 연습 문제 - AI 매칭 엔진 사용하기"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.order import Order
from src.models.facility import Facility
from src.engine.matcher import FacilityMatcher
from src.data.sample_data import create_sample_orders, create_sample_facilities


def exercise_1():
    """연습 1: AI 매칭 엔진 사용하기"""
    print("="*70)
    print("연습 1: AI 매칭 엔진으로 최적 설비 찾기")
    print("="*70)

    order = Order(
        order_id="INTER-001",
        weight=8.0,
        volume=0.4,
        item_count=12,
        fragile=True,
        priority=3,
        destination_zone="A",
        order_type="express"
    )

    facilities = create_sample_facilities()

    print(f"\n주문: {order.order_id}")
    print(f"  - 무게: {order.weight}kg, 부피: {order.volume}m³")
    print(f"  - 깨지기 쉬움: {order.fragile}, 우선순위: {order.priority}")
    print(f"\n사용 가능한 설비: {len(facilities)}개")

    print(f"""
과제: FacilityMatcher를 사용하여 최적의 설비를 찾으세요.

단계:
1. FacilityMatcher() 객체 생성
2. find_best_facility(order, facilities) 메서드 호출
3. 결과 출력 (설비 이름과 점수)

힌트:
    matcher = FacilityMatcher()
    result = matcher.find_best_facility(order, facilities)
    if result:
        facility, score = result
""")

    # TODO: 여기에 코드를 작성하세요

    # ============ 정답 (주석 해제하여 확인) ============
    # matcher = FacilityMatcher()
    # result = matcher.find_best_facility(order, facilities)
    #
    # if result:
    #     facility, score = result
    #     print(f"\n✅ 최적 설비: {facility.name}")
    #     print(f"📊 매칭 점수: {score:.2%}")
    #     print(f"🏷️  설비 유형: {facility.facility_type}")
    #     print(f"⚡ 속도 등급: {facility.speed_rating}/4")
    # else:
    #     print("\n❌ 적합한 설비를 찾을 수 없습니다.")


def exercise_2():
    """연습 2: 설비 순위 매기기"""
    print("\n" + "="*70)
    print("연습 2: 여러 설비의 순위 매기기")
    print("="*70)

    order = Order(
        order_id="INTER-002",
        weight=20.0,
        volume=1.0,
        item_count=30,
        fragile=False,
        priority=2,
        destination_zone="B",
        order_type="standard"
    )

    facilities = create_sample_facilities()

    print(f"\n주문: {order.order_id} (무게: {order.weight}kg, 부피: {order.volume}m³)")

    print(f"""
과제: 이 주문에 적합한 상위 3개 설비를 점수순으로 출력하세요.

힌트:
    matcher = FacilityMatcher()
    ranked = matcher.rank_facilities(order, facilities, top_n=3)
    for i, (facility, score) in enumerate(ranked, 1):
        print(f"{{i}}위. {{facility.name}} - {{score:.2%}}")
""")

    # TODO: 여기에 코드를 작성하세요

    # ============ 정답 (주석 해제하여 확인) ============
    # matcher = FacilityMatcher()
    # ranked = matcher.rank_facilities(order, facilities, top_n=3)
    #
    # print("\n🏆 상위 3개 설비:\n")
    # for i, (facility, score) in enumerate(ranked, 1):
    #     print(f"{i}위. {facility.name:25s} - 점수: {score:.2%}")
    #     print(f"     유형: {facility.facility_type:10s} 속도: {facility.speed_rating}/4")
    #     print()


def exercise_3():
    """연습 3: 일괄 처리"""
    print("\n" + "="*70)
    print("연습 3: 여러 주문 일괄 처리하기")
    print("="*70)

    orders = create_sample_orders()
    facilities = create_sample_facilities()

    print(f"\n처리할 주문: {len(orders)}개")
    print(f"사용 가능한 설비: {len(facilities)}개")

    print(f"""
과제: 모든 주문을 일괄 처리하고 결과를 출력하세요.

힌트:
    matcher = FacilityMatcher()
    results = matcher.batch_match(orders, facilities)
    for order_id, result in results.items():
        if result:
            facility, score = result
            print(f"{{order_id}} -> {{facility.name}} ({{score:.2%}})")
""")

    # TODO: 여기에 코드를 작성하세요

    # ============ 정답 (주석 해제하여 확인) ============
    # matcher = FacilityMatcher()
    # results = matcher.batch_match(orders, facilities)
    #
    # print("\n📦 일괄 처리 결과:\n")
    # for order_id, result in results.items():
    #     order = next(o for o in orders if o.order_id == order_id)
    #     print(f"{order_id:12s} ({order.order_type:8s}, {order.weight:5.1f}kg)", end="")
    #
    #     if result:
    #         facility, score = result
    #         print(f" -> {facility.name:25s} ({score:.2%})")
    #     else:
    #         print(f" -> ❌ 매칭 실패")


def exercise_4():
    """연습 4: 커스텀 가중치로 매칭"""
    print("\n" + "="*70)
    print("연습 4: 커스텀 가중치로 다른 결과 만들기")
    print("="*70)

    order = Order(
        order_id="INTER-004",
        weight=10.0,
        volume=0.5,
        item_count=15,
        fragile=True,
        priority=4,
        destination_zone="A",
        order_type="express"
    )

    facilities = create_sample_facilities()

    print(f"\n주문: 긴급 배송 (깨지기 쉬움)")
    print(f"  - {order.order_id}: {order.weight}kg, 우선순위 {order.priority}")

    print(f"""
과제: 두 가지 다른 가중치로 매칭하고 결과를 비교하세요.

1. 속도 중심 매칭 (weight_speed=0.5로 설정)
2. 안전 중심 매칭 (weight_fragile=0.5로 설정)

각각의 결과가 어떻게 다른지 확인하세요.

힌트:
    matcher_speed = FacilityMatcher(
        weight_capacity=0.1,
        weight_speed=0.5,
        weight_fragile=0.2,
        weight_zone=0.1,
        weight_type=0.1
    )
""")

    # TODO: 여기에 코드를 작성하세요

    # ============ 정답 (주석 해제하여 확인) ============
    # # 속도 중심
    # matcher_speed = FacilityMatcher(
    #     weight_capacity=0.1,
    #     weight_speed=0.5,
    #     weight_fragile=0.2,
    #     weight_zone=0.1,
    #     weight_type=0.1
    # )
    # result1 = matcher_speed.find_best_facility(order, facilities)
    #
    # # 안전 중심
    # matcher_safety = FacilityMatcher(
    #     weight_capacity=0.1,
    #     weight_speed=0.2,
    #     weight_fragile=0.5,
    #     weight_zone=0.1,
    #     weight_type=0.1
    # )
    # result2 = matcher_safety.find_best_facility(order, facilities)
    #
    # print("\n⚡ 속도 중심 매칭:")
    # if result1:
    #     facility, score = result1
    #     print(f"  {facility.name} (점수: {score:.2%}, 속도: {facility.speed_rating}/4)")
    #
    # print("\n🛡️  안전 중심 매칭:")
    # if result2:
    #     facility, score = result2
    #     print(f"  {facility.name} (점수: {score:.2%}, 깨지기 쉬운 물품: {facility.can_handle_fragile})")
    #
    # print("\n💡 같은 설비가 선택되었나요? 다른 설비가 선택되었나요?")


def exercise_5():
    """연습 5: 직접 설비 만들어서 테스트하기"""
    print("\n" + "="*70)
    print("연습 5: 나만의 설비를 만들어서 테스트")
    print("="*70)

    order = Order(
        order_id="CUSTOM-ORDER",
        weight=15.0,
        volume=0.8,
        item_count=20,
        fragile=True,
        priority=3,
        destination_zone="A",
        order_type="express"
    )

    print(f"\n테스트 주문: {order.order_id}")
    print(f"  - 무게: {order.weight}kg, 부피: {order.volume}m³")
    print(f"  - 깨지기 쉬움: {order.fragile}, 우선순위: {order.priority}")

    print(f"""
과제: 이 주문을 완벽하게 처리할 수 있는 최적의 설비를 직접 디자인하세요.

요구사항:
1. 주문을 처리할 수 있어야 함 (무게, 부피, 깨지기 쉬운 물품)
2. 목적지 구역을 지원해야 함
3. 빠른 처리 속도 (속도 등급 3 이상)
4. 만든 설비로 실제 매칭 테스트

힌트:
    my_facility = Facility(
        facility_id="MY-PERFECT-FAC",
        name="완벽한 설비",
        facility_type="robot",  # 또는 다른 타입
        max_weight=...,  # 주문을 처리할 수 있는 용량
        max_volume=...,
        can_handle_fragile=...,
        speed_rating=...,
        supported_zones=[...],
        available=True
    )
""")

    # TODO: 여기에 코드를 작성하세요
    # my_facility = Facility(...)

    # ============ 정답 예시 (주석 해제하여 확인) ============
    # my_facility = Facility(
    #     facility_id="MY-PERFECT-FAC",
    #     name="완벽한 Express 로봇",
    #     facility_type="robot",
    #     max_weight=20.0,  # 주문(15kg)을 처리 가능
    #     max_volume=1.0,   # 주문(0.8m³)을 처리 가능
    #     can_handle_fragile=True,  # 깨지기 쉬운 물품 OK
    #     speed_rating=4,   # 최고 속도
    #     supported_zones=["A", "B"],  # 목적지 A 지원
    #     available=True
    # )
    #
    # print(f"\n🏭 내가 만든 설비: {my_facility.name}")
    # print(f"  - 유형: {my_facility.facility_type}")
    # print(f"  - 용량: {my_facility.max_weight}kg, {my_facility.max_volume}m³")
    # print(f"  - 속도: {my_facility.speed_rating}/4")
    #
    # # 테스트
    # can_handle = my_facility.can_handle_order(order)
    # print(f"\n처리 가능? {can_handle}")
    #
    # if can_handle:
    #     utilization = my_facility.get_capacity_utilization(order)
    #     print(f"용량 사용률: {utilization:.2%}")
    #
    #     # 기존 설비들과 비교
    #     facilities = create_sample_facilities()
    #     facilities.append(my_facility)
    #
    #     matcher = FacilityMatcher()
    #     result = matcher.find_best_facility(order, facilities)
    #
    #     if result:
    #         facility, score = result
    #         print(f"\n🏆 최종 선택된 설비: {facility.name} (점수: {score:.2%})")
    #         if facility.facility_id == my_facility.facility_id:
    #             print("✅ 내가 만든 설비가 선택되었습니다!")
    #         else:
    #             print(f"❌ 다른 설비가 선택되었습니다. 더 최적화해보세요!")


def main():
    """모든 연습 문제 실행"""
    print("\n🎓 중급 연습 문제 - AI 매칭 엔진 사용하기\n")
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
    print("🎉 중급 연습 완료!")
    print("="*70)
    print("\n다음 단계: advanced_exercises.py를 확인하세요!")


if __name__ == "__main__":
    main()
