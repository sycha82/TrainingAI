"""인터랙티브 실습 스크립트 - 직접 입력하면서 배우기"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.order import Order
from src.models.facility import Facility
from src.engine.matcher import FacilityMatcher
from src.data.sample_data import create_sample_facilities


def print_header(text):
    """헤더 출력"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def interactive_order_creation():
    """대화형 주문 생성"""
    print_header("🎓 실습 1: 나만의 주문 만들기")

    print("주문 정보를 입력하세요 (엔터 = 기본값 사용)\n")

    order_id = input("주문 ID (예: ORD-999) [ORD-TEST]: ").strip() or "ORD-TEST"

    weight_input = input("무게 (kg) [10.0]: ").strip()
    weight = float(weight_input) if weight_input else 10.0

    volume_input = input("부피 (m³) [0.5]: ").strip()
    volume = float(volume_input) if volume_input else 0.5

    item_count_input = input("품목 수 [5]: ").strip()
    item_count = int(item_count_input) if item_count_input else 5

    fragile_input = input("깨지기 쉬운 물품? (y/n) [n]: ").strip().lower()
    fragile = fragile_input == 'y'

    priority_input = input("우선순위 (1=낮음, 2=보통, 3=높음, 4=긴급) [2]: ").strip()
    priority = int(priority_input) if priority_input and priority_input in ['1','2','3','4'] else 2

    zone = input("목적지 구역 (A/B/C) [A]: ").strip().upper() or "A"

    order_type = input("주문 유형 (standard/express/bulk) [standard]: ").strip() or "standard"

    # 주문 생성
    try:
        order = Order(
            order_id=order_id,
            weight=weight,
            volume=volume,
            item_count=item_count,
            fragile=fragile,
            priority=priority,
            destination_zone=zone,
            order_type=order_type
        )

        print("\n✅ 주문이 생성되었습니다!")
        print(f"\n{order}")

        # 계산 메서드 테스트
        print(f"\n📊 주문 분석:")
        print(f"  - 밀도: {order.get_density():.2f} kg/m³")
        print(f"  - 무거운 주문? {order.is_heavy()}")
        print(f"  - 대량 주문? {order.is_bulk()}")

        return order

    except ValueError as e:
        print(f"\n❌ 오류: {e}")
        return None


def interactive_facility_matching(order):
    """대화형 설비 매칭"""
    if not order:
        print("먼저 주문을 생성해주세요!")
        return

    print_header("🎯 실습 2: AI 매칭 실행하기")

    # 설비 목록 가져오기
    facilities = create_sample_facilities()

    print(f"사용 가능한 설비: {len(facilities)}개\n")
    for i, fac in enumerate(facilities, 1):
        print(f"{i}. {fac.name} ({fac.facility_type})")
        print(f"   - 용량: 최대 {fac.max_weight}kg, {fac.max_volume}m³")
        print(f"   - 속도: {fac.speed_rating}/4, 구역: {', '.join(fac.supported_zones)}")
        print()

    # AI 매칭 실행
    print("🤖 AI 매칭 엔진 실행 중...\n")

    matcher = FacilityMatcher()

    # 최적 설비 찾기
    result = matcher.find_best_facility(order, facilities)

    if result:
        facility, score = result
        print(f"✨ 최적 설비: {facility.name}")
        print(f"📊 매칭 점수: {score:.2%}\n")

        # 상세 분석
        print("📈 왜 이 설비가 선택되었을까요?")
        print(f"  - 용량 활용률: {facility.get_capacity_utilization(order):.2%}")
        print(f"  - 깨지기 쉬운 물품 처리: {'가능' if facility.can_handle_fragile else '불가능'}")
        print(f"  - 속도 등급: {facility.speed_rating}/4")
        print(f"  - 구역 지원: {order.destination_zone} in {facility.supported_zones}")
    else:
        print("❌ 적합한 설비를 찾을 수 없습니다.")

    # 전체 순위 보기
    print("\n" + "-"*70)
    show_ranking = input("\n전체 설비 순위를 보시겠습니까? (y/n) [n]: ").strip().lower()

    if show_ranking == 'y':
        print("\n🏆 전체 설비 순위:\n")
        ranked = matcher.rank_facilities(order, facilities, top_n=len(facilities))

        for i, (fac, score) in enumerate(ranked, 1):
            print(f"{i}위. {fac.name:25s} - 점수: {score:6.2%}")


def interactive_custom_weights():
    """대화형 가중치 조정"""
    print_header("⚙️  실습 3: 가중치 커스터마이징")

    print("각 요소의 중요도를 설정하세요 (0-100, 합계는 자동으로 정규화)")
    print("높을수록 그 요소가 중요합니다.\n")

    def get_weight(name, default):
        while True:
            value = input(f"{name} [{default}]: ").strip()
            if not value:
                return default
            try:
                return float(value)
            except ValueError:
                print("숫자를 입력해주세요!")

    weight_capacity = get_weight("용량 활용률 중요도", 25)
    weight_speed = get_weight("처리 속도 중요도", 25)
    weight_fragile = get_weight("깨지기 쉬운 물품 처리 중요도", 20)
    weight_zone = get_weight("목적지 구역 매칭 중요도", 15)
    weight_type = get_weight("설비 유형 매칭 중요도", 15)

    # 커스텀 매처 생성
    matcher = FacilityMatcher(
        weight_capacity=weight_capacity,
        weight_speed=weight_speed,
        weight_fragile=weight_fragile,
        weight_zone=weight_zone,
        weight_type=weight_type
    )

    print(f"\n✅ 커스텀 매처 생성 완료!")
    print(f"\n정규화된 가중치:")
    print(f"  - 용량 활용률: {matcher.weight_capacity:.2%}")
    print(f"  - 처리 속도: {matcher.weight_speed:.2%}")
    print(f"  - 깨지기 쉬운 물품: {matcher.weight_fragile:.2%}")
    print(f"  - 목적지 구역: {matcher.weight_zone:.2%}")
    print(f"  - 설비 유형: {matcher.weight_type:.2%}")

    return matcher


def quick_test():
    """빠른 테스트 모드"""
    print_header("⚡ 빠른 테스트 모드")

    # 미리 정의된 테스트 시나리오
    scenarios = [
        {
            "name": "긴급 배송 (깨지기 쉬움)",
            "order": Order("TEST-1", 5.0, 0.3, 3, fragile=True, priority=4,
                          destination_zone="A", order_type="express")
        },
        {
            "name": "대량 주문 (무거움)",
            "order": Order("TEST-2", 70.0, 3.0, 120, fragile=False, priority=1,
                          destination_zone="C", order_type="bulk")
        },
        {
            "name": "일반 주문 (중간 크기)",
            "order": Order("TEST-3", 15.0, 0.8, 20, fragile=False, priority=2,
                          destination_zone="B", order_type="standard")
        }
    ]

    facilities = create_sample_facilities()
    matcher = FacilityMatcher()

    for scenario in scenarios:
        print(f"\n📦 시나리오: {scenario['name']}")
        order = scenario['order']
        print(f"   (무게: {order.weight}kg, 부피: {order.volume}m³, 우선순위: {order.priority})")

        result = matcher.find_best_facility(order, facilities)
        if result:
            facility, score = result
            print(f"   ✅ 최적 설비: {facility.name} (점수: {score:.2%})")
        else:
            print(f"   ❌ 매칭 실패")


def main():
    """메인 메뉴"""
    print("\n" + "🎓 물류센터 AI 엔진 - 인터랙티브 실습".center(70, "="))

    order = None

    while True:
        print("\n" + "-"*70)
        print("\n📚 실습 메뉴:")
        print("  1. 나만의 주문 만들기")
        print("  2. AI 매칭 실행하기 (1번 먼저 필요)")
        print("  3. 가중치 커스터마이징")
        print("  4. 빠른 테스트 (미리 정의된 시나리오)")
        print("  5. 처음부터 다시 (1→2 순서대로)")
        print("  0. 종료")

        choice = input("\n선택하세요: ").strip()

        if choice == '1':
            order = interactive_order_creation()
        elif choice == '2':
            if order:
                interactive_facility_matching(order)
            else:
                print("\n⚠️  먼저 주문을 생성해주세요 (메뉴 1번)")
        elif choice == '3':
            interactive_custom_weights()
        elif choice == '4':
            quick_test()
        elif choice == '5':
            order = interactive_order_creation()
            if order:
                interactive_facility_matching(order)
        elif choice == '0':
            print("\n👋 실습을 종료합니다. 수고하셨습니다!\n")
            break
        else:
            print("\n⚠️  올바른 메뉴를 선택해주세요.")

    print("💡 팁: examples/ 폴더의 다른 예제들도 확인해보세요!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 실습을 종료합니다.\n")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
