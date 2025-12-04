"""기본 사용 예제 - 물류센터 설비 AI 매칭"""

import sys
import os

# 상위 디렉토리의 src 모듈을 import하기 위한 경로 설정
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.order import Order
from src.models.facility import Facility
from src.engine.matcher import FacilityMatcher
from src.data.sample_data import create_sample_orders, create_sample_facilities


def print_separator():
    """구분선 출력"""
    print("\n" + "="*80 + "\n")


def example_1_single_order():
    """예제 1: 단일 주문에 최적 설비 찾기"""
    print("📦 예제 1: 단일 주문에 최적 설비 찾기")
    print_separator()

    # 주문 생성
    order = Order(
        order_id="ORD-100",
        weight=8.0,
        volume=0.4,
        item_count=10,
        fragile=True,
        priority=3,
        destination_zone="A",
        order_type="express"
    )

    print(f"주문 정보:")
    print(f"  - ID: {order.order_id}")
    print(f"  - 무게: {order.weight}kg, 부피: {order.volume}m³")
    print(f"  - 품목 수: {order.item_count}개")
    print(f"  - 깨지기 쉬움: {'예' if order.fragile else '아니오'}")
    print(f"  - 우선순위: {order.priority} (4=긴급)")
    print(f"  - 목적지 구역: {order.destination_zone}")
    print(f"  - 주문 유형: {order.order_type}")

    # 설비 목록 생성
    facilities = create_sample_facilities()

    # AI 매칭 엔진 생성
    matcher = FacilityMatcher()

    # 최적 설비 찾기
    result = matcher.find_best_facility(order, facilities)

    if result:
        facility, score = result
        print(f"\n✅ 최적 설비 발견!")
        print(f"  - 설비 ID: {facility.facility_id}")
        print(f"  - 설비 이름: {facility.name}")
        print(f"  - 설비 유형: {facility.facility_type}")
        print(f"  - 매칭 점수: {score:.2%}")
    else:
        print("\n❌ 적합한 설비를 찾을 수 없습니다.")


def example_2_rank_facilities():
    """예제 2: 상위 설비 순위 매기기"""
    print("📊 예제 2: 주문에 적합한 설비 순위")
    print_separator()

    # 대량 주문 생성
    order = Order(
        order_id="ORD-200",
        weight=45.0,
        volume=2.0,
        item_count=80,
        fragile=False,
        priority=2,
        destination_zone="C",
        order_type="bulk"
    )

    print(f"대량 주문: {order.order_id}")
    print(f"  - 무게: {order.weight}kg, 부피: {order.volume}m³")
    print(f"  - 품목 수: {order.item_count}개")

    facilities = create_sample_facilities()
    matcher = FacilityMatcher()

    # 상위 3개 설비 순위
    ranked = matcher.rank_facilities(order, facilities, top_n=3)

    print(f"\n🏆 상위 {len(ranked)}개 설비:")
    for i, (facility, score) in enumerate(ranked, 1):
        print(f"\n{i}위. {facility.name} (점수: {score:.2%})")
        print(f"     - 유형: {facility.facility_type}")
        print(f"     - 최대 용량: {facility.max_weight}kg, {facility.max_volume}m³")
        print(f"     - 속도 등급: {facility.speed_rating}/4")


def example_3_batch_matching():
    """예제 3: 여러 주문 일괄 매칭"""
    print("🔄 예제 3: 여러 주문 일괄 처리")
    print_separator()

    orders = create_sample_orders()
    facilities = create_sample_facilities()
    matcher = FacilityMatcher()

    # 일괄 매칭
    results = matcher.batch_match(orders, facilities)

    print(f"총 {len(orders)}개 주문 처리 결과:\n")

    for order_id, result in results.items():
        order = next(o for o in orders if o.order_id == order_id)
        print(f"📦 {order_id} ({order.order_type}, {order.weight}kg)")

        if result:
            facility, score = result
            print(f"   ➜ {facility.name} (점수: {score:.2%})")
        else:
            print(f"   ➜ ❌ 매칭 실패")
        print()


def example_4_custom_weights():
    """예제 4: 커스텀 가중치로 매칭"""
    print("⚙️  예제 4: 커스텀 가중치 설정")
    print_separator()

    order = Order(
        order_id="ORD-300",
        weight=5.0,
        volume=0.3,
        item_count=5,
        fragile=True,
        priority=4,
        destination_zone="A",
        order_type="express"
    )

    facilities = create_sample_facilities()

    # 기본 가중치
    print("1️⃣  기본 가중치 (균형잡힌 매칭):")
    matcher_default = FacilityMatcher()
    result = matcher_default.find_best_facility(order, facilities)
    if result:
        facility, score = result
        print(f"   {facility.name} (점수: {score:.2%})\n")

    # 속도 중심 가중치
    print("2️⃣  속도 중심 가중치 (빠른 처리 우선):")
    matcher_speed = FacilityMatcher(
        weight_capacity=0.1,
        weight_speed=0.5,      # 속도 가중치 높임
        weight_fragile=0.2,
        weight_zone=0.1,
        weight_type=0.1
    )
    result = matcher_speed.find_best_facility(order, facilities)
    if result:
        facility, score = result
        print(f"   {facility.name} (점수: {score:.2%})\n")

    # 효율성 중심 가중치
    print("3️⃣  효율성 중심 가중치 (용량 활용 최적화):")
    matcher_efficiency = FacilityMatcher(
        weight_capacity=0.6,   # 용량 활용률 가중치 높임
        weight_speed=0.1,
        weight_fragile=0.1,
        weight_zone=0.1,
        weight_type=0.1
    )
    result = matcher_efficiency.find_best_facility(order, facilities)
    if result:
        facility, score = result
        print(f"   {facility.name} (점수: {score:.2%})")


def main():
    """메인 함수 - 모든 예제 실행"""
    print("\n" + "🚀 물류센터 설비 AI 매칭 엔진 - 사용 예제".center(80))
    print("="*80)

    try:
        example_1_single_order()
        print_separator()

        example_2_rank_facilities()
        print_separator()

        example_3_batch_matching()
        print_separator()

        example_4_custom_weights()
        print_separator()

        print("✨ 모든 예제 실행 완료!")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
