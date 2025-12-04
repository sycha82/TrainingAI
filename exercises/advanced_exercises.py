"""고급 연습 문제 - 확장 및 최적화"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.order import Order
from src.models.facility import Facility
from src.engine.matcher import FacilityMatcher
from src.data.sample_data import create_sample_orders, create_sample_facilities


def exercise_1():
    """연습 1: 매칭 성능 분석하기"""
    print("="*70)
    print("연습 1: 매칭 성능 분석 - 얼마나 잘 매칭되었나?")
    print("="*70)

    orders = create_sample_orders()
    facilities = create_sample_facilities()
    matcher = FacilityMatcher()

    print(f"""
과제: 모든 주문을 매칭한 후, 다음 통계를 계산하세요.

1. 매칭 성공률 (매칭된 주문 수 / 전체 주문 수)
2. 평균 매칭 점수
3. 가장 높은 점수와 가장 낮은 점수
4. 각 설비별 할당된 주문 수

힌트:
    results = matcher.batch_match(orders, facilities)
    success_count = sum(1 for r in results.values() if r is not None)
    total = len(results)
    success_rate = success_count / total
""")

    # TODO: 여기에 코드를 작성하세요

    # ============ 정답 (주석 해제하여 확인) ============
    # results = matcher.batch_match(orders, facilities)
    #
    # # 1. 매칭 성공률
    # success_count = sum(1 for r in results.values() if r is not None)
    # total = len(results)
    # success_rate = success_count / total
    #
    # # 2. 평균 점수
    # scores = [score for result in results.values() if result for _, score in [result]]
    # avg_score = sum(scores) / len(scores) if scores else 0
    #
    # # 3. 최고/최저 점수
    # max_score = max(scores) if scores else 0
    # min_score = min(scores) if scores else 0
    #
    # # 4. 설비별 할당 수
    # facility_counts = {}
    # for result in results.values():
    #     if result:
    #         facility, _ = result
    #         facility_counts[facility.name] = facility_counts.get(facility.name, 0) + 1
    #
    # # 결과 출력
    # print("\n📊 매칭 성능 분석:\n")
    # print(f"✅ 매칭 성공률: {success_rate:.2%} ({success_count}/{total})")
    # print(f"📈 평균 매칭 점수: {avg_score:.2%}")
    # print(f"🔝 최고 점수: {max_score:.2%}")
    # print(f"🔻 최저 점수: {min_score:.2%}")
    #
    # print("\n🏭 설비별 할당 현황:")
    # for fac_name, count in sorted(facility_counts.items(), key=lambda x: x[1], reverse=True):
    #     print(f"  {fac_name:25s}: {count}개 주문")


def exercise_2():
    """연습 2: 최적 가중치 찾기"""
    print("\n" + "="*70)
    print("연습 2: 다양한 가중치 조합 시도해보기")
    print("="*70)

    order = Order(
        order_id="ADV-002",
        weight=12.0,
        volume=0.6,
        item_count=18,
        fragile=True,
        priority=3,
        destination_zone="B",
        order_type="express"
    )

    facilities = create_sample_facilities()

    print(f"\n테스트 주문: {order.order_id}")
    print(f"  - 무게: {order.weight}kg, 깨지기 쉬움: {order.fragile}")
    print(f"  - 우선순위: {order.priority}, 유형: {order.order_type}")

    print(f"""
과제: 여러 가지 가중치 조합을 테스트하고 어떤 설비가 선택되는지 비교하세요.

시도할 조합:
1. 균형형 (모든 가중치 동일)
2. 속도 우선 (speed=0.5)
3. 효율성 우선 (capacity=0.5)
4. 안전 우선 (fragile=0.5)

각 경우의 결과를 비교하고 분석하세요.
""")

    # TODO: 여기에 코드를 작성하세요

    # ============ 정답 (주석 해제하여 확인) ============
    # configs = [
    #     ("균형형", {"weight_capacity": 0.2, "weight_speed": 0.2, "weight_fragile": 0.2, "weight_zone": 0.2, "weight_type": 0.2}),
    #     ("속도 우선", {"weight_capacity": 0.1, "weight_speed": 0.5, "weight_fragile": 0.2, "weight_zone": 0.1, "weight_type": 0.1}),
    #     ("효율성 우선", {"weight_capacity": 0.6, "weight_speed": 0.1, "weight_fragile": 0.1, "weight_zone": 0.1, "weight_type": 0.1}),
    #     ("안전 우선", {"weight_capacity": 0.1, "weight_speed": 0.1, "weight_fragile": 0.5, "weight_zone": 0.15, "weight_type": 0.15}),
    # ]
    #
    # print("\n🔬 가중치 조합별 결과:\n")
    # for name, weights in configs:
    #     matcher = FacilityMatcher(**weights)
    #     result = matcher.find_best_facility(order, facilities)
    #
    #     print(f"{name:15s}: ", end="")
    #     if result:
    #         facility, score = result
    #         print(f"{facility.name:25s} (점수: {score:.2%})")
    #     else:
    #         print("매칭 실패")
    #
    # print("\n💡 같은 주문이어도 가중치에 따라 다른 설비가 선택될 수 있습니다!")


def exercise_3():
    """연습 3: 설비 가용성 시뮬레이션"""
    print("\n" + "="*70)
    print("연습 3: 설비 사용 중일 때의 시나리오")
    print("="*70)

    orders = create_sample_orders()
    facilities = create_sample_facilities()

    print(f"\n주문: {len(orders)}개")
    print(f"설비: {len(facilities)}개")

    print(f"""
과제: 설비를 순차적으로 사용한다고 가정하고 시뮬레이션하세요.

시나리오:
1. 첫 번째 주문을 매칭하고, 그 설비를 사용 불가(available=False)로 설정
2. 두 번째 주문을 남은 설비 중에서 매칭
3. 계속 반복
4. 모든 주문이 처리될 때까지 또는 설비가 부족할 때까지

힌트:
    for order in orders:
        result = matcher.find_best_facility(order, facilities)
        if result:
            facility, score = result
            facility.available = False  # 사용 중으로 표시
""")

    # TODO: 여기에 코드를 작성하세요

    # ============ 정답 (주석 해제하여 확인) ============
    # # 설비를 복사해서 사용 (원본 유지)
    # import copy
    # facilities_copy = copy.deepcopy(facilities)
    #
    # matcher = FacilityMatcher()
    # assignments = []
    #
    # print("\n📦 순차 처리 시뮬레이션:\n")
    # for i, order in enumerate(orders, 1):
    #     # 사용 가능한 설비만 필터링
    #     available_facilities = [f for f in facilities_copy if f.available]
    #
    #     print(f"{i}. {order.order_id} ({order.order_type}, {order.weight}kg)")
    #     print(f"   사용 가능한 설비: {len(available_facilities)}개")
    #
    #     result = matcher.find_best_facility(order, available_facilities)
    #
    #     if result:
    #         facility, score = result
    #         print(f"   ✅ 할당: {facility.name} (점수: {score:.2%})")
    #         facility.available = False  # 사용 중으로 표시
    #         assignments.append((order.order_id, facility.name, score))
    #     else:
    #         print(f"   ❌ 사용 가능한 설비 없음!")
    #         assignments.append((order.order_id, None, 0))
    #     print()
    #
    # # 요약
    # success_count = sum(1 for _, fac, _ in assignments if fac is not None)
    # print(f"📊 최종 결과: {success_count}/{len(orders)} 주문 처리 성공")


def exercise_4():
    """연습 4: 새로운 속성 추가하기"""
    print("\n" + "="*70)
    print("연습 4: Order 클래스 확장하기")
    print("="*70)

    print(f"""
과제: Order 클래스에 새로운 속성을 추가하고 사용해보세요.

예를 들어:
- temperature_controlled (온도 관리 필요 여부)
- max_handling_time (최대 처리 시간)
- special_packaging (특수 포장 필요)

단계:
1. src/models/order.py 파일 열기
2. Order 클래스에 새 속성 추가
3. 필요하다면 Facility 클래스에도 대응하는 속성 추가
4. 매칭 알고리즘에 새 속성 반영

힌트:
    @dataclass
    class Order:
        # 기존 속성들...
        temperature_controlled: bool = False  # 새 속성 추가

이것은 실제 코드를 수정하는 연습입니다!
""")

    print("\n💡 이 연습은 직접 코드를 수정해야 합니다.")
    print("   src/models/order.py 파일을 열어서 새 속성을 추가해보세요!")


def exercise_5():
    """연습 5: 복잡한 비즈니스 로직 구현"""
    print("\n" + "="*70)
    print("연습 5: 복잡한 규칙 추가하기")
    print("="*70)

    print(f"""
과제: 다음과 같은 비즈니스 규칙을 구현하세요.

규칙:
1. 우선순위 4(긴급)인 주문은 속도 등급 3 이상의 설비만 사용 가능
2. 대량 주문(bulk)은 최대 용량의 50% 이상을 사용하는 설비만 선택
3. 깨지기 쉬운 물품은 robot 또는 manual 설비만 사용
4. 같은 목적지 구역의 주문은 가능한 같은 설비에 할당 (배치 효율성)

힌트:
    def find_best_facility_with_rules(order, facilities):
        # 규칙에 맞는 설비만 필터링
        valid_facilities = []
        for facility in facilities:
            # 규칙 1 체크
            if order.priority == 4 and facility.speed_rating < 3:
                continue
            # 규칙 2 체크
            if order.is_bulk():
                utilization = facility.get_capacity_utilization(order)
                if utilization < 0.5:
                    continue
            # ... 계속

이것은 실전 프로젝트 수준의 연습입니다!
""")

    # TODO: 여기에 코드를 작성하세요
    # 힌트: 새로운 함수를 만들어서 규칙을 구현하세요

    # ============ 정답 예시 (주석 해제하여 확인) ============
    # def find_best_facility_with_rules(order, facilities, matcher):
    #     """비즈니스 규칙이 적용된 매칭"""
    #     valid_facilities = []
    #
    #     for facility in facilities:
    #         # 기본 처리 가능 여부
    #         if not facility.can_handle_order(order):
    #             continue
    #
    #         # 규칙 1: 긴급 주문은 빠른 설비만
    #         if order.priority == 4 and facility.speed_rating < 3:
    #             continue
    #
    #         # 규칙 2: 대량 주문은 충분히 큰 설비만
    #         if order.is_bulk():
    #             utilization = facility.get_capacity_utilization(order)
    #             if utilization < 0.5:
    #                 continue
    #
    #         # 규칙 3: 깨지기 쉬운 물품은 특정 설비만
    #         if order.fragile and facility.facility_type not in ['robot', 'manual', 'sorter']:
    #             continue
    #
    #         valid_facilities.append(facility)
    #
    #     # 유효한 설비 중에서 매칭
    #     if not valid_facilities:
    #         return None
    #
    #     return matcher.find_best_facility(order, valid_facilities)
    #
    # # 테스트
    # orders = create_sample_orders()
    # facilities = create_sample_facilities()
    # matcher = FacilityMatcher()
    #
    # print("\n🔐 비즈니스 규칙 적용 결과:\n")
    # for order in orders:
    #     print(f"📦 {order.order_id} (우선순위: {order.priority}, 유형: {order.order_type})")
    #
    #     # 규칙 없이
    #     result_normal = matcher.find_best_facility(order, facilities)
    #
    #     # 규칙 적용
    #     result_with_rules = find_best_facility_with_rules(order, facilities, matcher)
    #
    #     print(f"   일반 매칭: ", end="")
    #     if result_normal:
    #         fac, score = result_normal
    #         print(f"{fac.name} ({score:.2%})")
    #     else:
    #         print("매칭 실패")
    #
    #     print(f"   규칙 적용:  ", end="")
    #     if result_with_rules:
    #         fac, score = result_with_rules
    #         print(f"{fac.name} ({score:.2%})")
    #     else:
    #         print("매칭 실패")
    #     print()


def main():
    """모든 연습 문제 실행"""
    print("\n🎓 고급 연습 문제 - 확장 및 최적화\n")
    print("이 단계부터는 실제 프로젝트 수준의 문제를 다룹니다.")
    print("코드를 직접 수정하고 확장하는 연습을 하게 됩니다.\n")

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
    print("🎉 고급 연습 완료!")
    print("="*70)
    print("\n축하합니다! 이제 실전 프로젝트를 시작할 준비가 되었습니다!")
    print("다음 단계: 실제 데이터로 프로젝트를 확장해보세요!")


if __name__ == "__main__":
    main()
