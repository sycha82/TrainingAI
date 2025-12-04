"""규칙 기반 vs 머신러닝 엔진 비교

.NET 개발자를 위한 설명:
-----------------------
두 가지 접근 방식을 비교합니다:

1. 규칙 기반 (Rule-based):
   - if-else 로직으로 구현
   - 명시적인 규칙 (가중치, 조건문)
   - C#의 Strategy Pattern과 비슷
   - 투명하고 예측 가능

2. 머신러닝 (Machine Learning):
   - 데이터에서 패턴을 학습
   - 암묵적인 규칙 (자동 발견)
   - ML.NET의 학습 모델과 비슷
   - 적응적이고 개선 가능
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engine.matcher import FacilityMatcher
from src.engine.ml_matcher import MLMatcher
from src.data.training_data_generator import TrainingDataGenerator
from src.data.sample_data import create_sample_orders


def compare_performance():
    """성능 비교: 정확도와 속도"""
    print("="*80)
    print("비교 1: 성능 (정확도 & 속도)")
    print("="*80)

    # 데이터 준비
    generator = TrainingDataGenerator(seed=42)
    train_orders, train_labels = generator.generate_training_data(1000)
    test_orders, test_labels = generator.generate_test_data(200)
    facilities = generator.generate_facilities()

    # 규칙 기반 엔진
    print("\n📐 규칙 기반 엔진")
    print("-" * 80)

    rule_matcher = FacilityMatcher()

    # 규칙 기반은 학습이 없으므로 바로 예측
    start_time = time.time()
    rule_correct = 0

    for order, true_label in zip(test_orders, test_labels):
        result = rule_matcher.find_best_facility(order, facilities)
        if result and result[0].facility_id == true_label:
            rule_correct += 1

    rule_time = time.time() - start_time
    rule_accuracy = rule_correct / len(test_orders)

    print(f"   정확도: {rule_accuracy:.2%} ({rule_correct}/{len(test_orders)})")
    print(f"   실행 시간: {rule_time:.3f}초")

    # 머신러닝 엔진
    print("\n🤖 머신러닝 엔진")
    print("-" * 80)

    ml_matcher = MLMatcher(n_estimators=100, random_state=42)

    # ML은 먼저 학습 필요
    train_start = time.time()
    ml_matcher.train(train_orders, train_labels)
    train_time = time.time() - train_start

    # 예측
    predict_start = time.time()
    ml_correct = 0

    for order, true_label in zip(test_orders, test_labels):
        result = ml_matcher.predict(order, facilities)
        if result and result[0].facility_id == true_label:
            ml_correct += 1

    predict_time = time.time() - predict_start
    ml_accuracy = ml_correct / len(test_orders)

    print(f"   학습 시간: {train_time:.3f}초")
    print(f"   예측 시간: {predict_time:.3f}초")
    print(f"   정확도: {ml_accuracy:.2%} ({ml_correct}/{len(test_orders)})")

    # 비교 결과
    print("\n📊 비교 결과")
    print("-" * 80)
    print(f"{'항목':<20} {'규칙 기반':>15} {'머신러닝':>15} {'승자':>10}")
    print("-" * 80)

    accuracy_winner = "ML" if ml_accuracy > rule_accuracy else "Rule" if rule_accuracy > ml_accuracy else "동점"
    speed_winner = "Rule" if rule_time < predict_time else "ML"

    print(f"{'정확도':<20} {rule_accuracy:>14.2%} {ml_accuracy:>14.2%} {accuracy_winner:>10}")
    print(f"{'예측 속도':<20} {rule_time:>13.3f}초 {predict_time:>13.3f}초 {speed_winner:>10}")

    print(f"\n💡 해석:")
    print(f"   - 정확도: ML이 데이터에서 패턴을 학습하여 더 정확할 수 있음")
    print(f"   - 속도: 규칙 기반이 단순 계산이라 보통 더 빠름")
    print(f"   - 학습 시간: ML은 초기 학습이 필요하지만 한번만 하면 됨")


def compare_decision_process():
    """의사결정 과정 비교"""
    print("\n" + "="*80)
    print("비교 2: 의사결정 과정")
    print("="*80)

    # 데이터 준비
    generator = TrainingDataGenerator(seed=42)
    train_orders, train_labels = generator.generate_training_data(500)
    facilities = generator.generate_facilities()

    # 테스트 주문
    test_order = create_sample_orders()[2]  # 대량 주문

    print(f"\n📦 테스트 주문:")
    print(f"   - ID: {test_order.order_id}")
    print(f"   - 무게: {test_order.weight:.1f}kg, 부피: {test_order.volume:.2f}m³")
    print(f"   - 유형: {test_order.order_type}, 품목: {test_order.item_count}개")
    print(f"   - 깨지기 쉬움: {test_order.fragile}, 우선순위: {test_order.priority}")

    # 규칙 기반 의사결정
    print(f"\n📐 규칙 기반 엔진의 의사결정:")
    print("-" * 80)

    rule_matcher = FacilityMatcher()
    result = rule_matcher.find_best_facility(test_order, facilities)

    if result:
        facility, score = result
        print(f"   선택: {facility.name}")
        print(f"   점수: {score:.2%}")
        print(f"\n   의사결정 근거:")
        print(f"     - 용량 활용률: {facility.get_capacity_utilization(test_order):.2%}")
        print(f"     - 속도 등급: {facility.speed_rating}/4")
        print(f"     - 설비 유형: {facility.facility_type}")
        print(f"     - 가중치 조합으로 점수 계산")
        print(f"\n   ✅ 투명함: 점수 계산 과정을 모두 알 수 있음")

    # ML 의사결정
    print(f"\n🤖 머신러닝 엔진의 의사결정:")
    print("-" * 80)

    ml_matcher = MLMatcher(n_estimators=100, random_state=42)
    ml_matcher.train(train_orders, train_labels)

    result = ml_matcher.predict(test_order, facilities)

    if result:
        facility, confidence = result
        print(f"   선택: {facility.name}")
        print(f"   확신도: {confidence:.2%}")
        print(f"\n   의사결정 근거:")
        print(f"     - 과거 유사한 주문들의 패턴 학습")
        print(f"     - {ml_matcher._model.n_estimators}개 의사결정나무의 투표")
        print(f"     - 확률적 예측: {confidence:.2%}가 이 설비에 투표")
        print(f"\n   ⚠️  블랙박스: 내부 과정은 복잡하지만 결과는 신뢰 가능")

    # 특성 중요도
    print(f"\n   ML이 중요하게 본 특성 (상위 3개):")
    importances = ml_matcher.get_feature_importances()
    for i, (feature, imp) in enumerate(
        sorted(importances.items(), key=lambda x: x[1], reverse=True)[:3], 1
    ):
        print(f"     {i}. {feature}: {imp:.4f}")


def compare_adaptability():
    """적응성 비교"""
    print("\n" + "="*80)
    print("비교 3: 적응성 (새로운 패턴 학습)")
    print("="*80)

    generator = TrainingDataGenerator(seed=42)

    print("\n시나리오: 새로운 비즈니스 규칙 추가")
    print("-" * 80)
    print("  '긴급 주문(priority=4)은 항상 로봇(robot) 설비를 선호'")

    # 이 규칙을 반영한 데이터 생성 (시뮬레이션)
    train_orders, train_labels = generator.generate_training_data(800)
    test_orders, test_labels = generator.generate_test_data(200)
    facilities = generator.generate_facilities()

    # 규칙 기반
    print(f"\n📐 규칙 기반 엔진:")
    print(f"   ❌ 코드 수정 필요")
    print(f"   - matcher.py 파일을 열어서")
    print(f"   - _calculate_type_score() 메서드 수정")
    print(f"   - 가중치 재조정")
    print(f"   - 재배포")

    # ML
    print(f"\n🤖 머신러닝 엔진:")
    print(f"   ✅ 재학습만 하면 됨")
    print(f"   - 새로운 데이터로 다시 학습")
    print(f"   - 코드 수정 불필요")
    print(f"   - 자동으로 새 패턴 반영")

    ml_matcher = MLMatcher(n_estimators=100, random_state=42)
    ml_matcher.train(train_orders, train_labels)

    # 긴급 주문 테스트
    urgent_orders = [o for o in test_orders if o.priority == 4][:5]

    print(f"\n   긴급 주문 {len(urgent_orders)}개 테스트:")
    robot_count = 0

    for order in urgent_orders:
        result = ml_matcher.predict(order, facilities)
        if result:
            facility, _ = result
            if facility.facility_type == "robot":
                robot_count += 1

    print(f"     - 로봇 설비 선택: {robot_count}/{len(urgent_orders)}개")
    print(f"     - ML이 패턴을 학습함!")


def print_recommendations():
    """추천 사항"""
    print("\n" + "="*80)
    print("💡 어떤 엔진을 선택해야 할까?")
    print("="*80)

    print("\n📐 규칙 기반 엔진을 선택하는 경우:")
    print("   ✅ 비즈니스 규칙이 명확하고 안정적")
    print("   ✅ 의사결정 근거를 명확히 설명해야 함")
    print("   ✅ 실시간 처리 속도가 중요")
    print("   ✅ 과거 데이터가 부족함")
    print("   ✅ 규정/컴플라이언스 때문에 투명성 필요")

    print("\n🤖 머신러닝 엔진을 선택하는 경우:")
    print("   ✅ 과거 운영 데이터가 충분함 (수천 개 이상)")
    print("   ✅ 패턴이 복잡하고 명확한 규칙 정의가 어려움")
    print("   ✅ 비즈니스 환경이 자주 변함")
    print("   ✅ 최고의 정확도가 중요")
    print("   ✅ 초기 학습 시간을 감수할 수 있음")

    print("\n🎯 하이브리드 접근 (추천!):")
    print("   ✅ 규칙 기반으로 기본 필터링 (처리 불가능한 설비 제거)")
    print("   ✅ ML로 최종 선택 (남은 후보 중 최적 선택)")
    print("   ✅ 두 엔진의 장점을 모두 활용")


def main():
    """메인 함수"""
    print("\n" + "⚔️  규칙 기반 vs 머신러닝 엔진 비교".center(80, "="))
    print("="*80)

    try:
        compare_performance()

        input("\n[엔터를 눌러 다음 비교로 이동...]")
        compare_decision_process()

        input("\n[엔터를 눌러 다음 비교로 이동...]")
        compare_adaptability()

        print_recommendations()

        print("\n" + "="*80)
        print("✨ 비교 완료!")
        print("="*80)
        print("\n.NET 개발자 팁:")
        print("  - 규칙 기반 = Strategy Pattern")
        print("  - ML = ML.NET의 학습 모델")
        print("  - 실무에서는 두 가지를 조합하여 사용하는 것이 best practice")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
