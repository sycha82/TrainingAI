"""ML 매칭 수정 사항 확인 스크립트

웹 앱에서 사용하는 것과 동일한 설비로 ML 모델이 작동하는지 확인합니다.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.models.order import Order
from src.engine.ml_matcher import MLMatcher
from src.data.sample_data import create_sample_facilities
from src.data.training_data_generator import TrainingDataGenerator

print("=" * 70)
print("ML 매칭 수정 사항 확인")
print("=" * 70)

# 1. 웹 앱과 동일한 설비 로드
facilities = create_sample_facilities()
print(f"\n✅ 웹 앱 설비 로드: {len(facilities)}개")
print("   설비 ID 목록:", [f.facility_id for f in facilities])

# 2. 학습 데이터 생성 (이제 동일한 설비 사용)
print("\n" + "-" * 70)
generator = TrainingDataGenerator(seed=42)
train_orders, train_labels = generator.generate_training_data(500)

print(f"\n학습 데이터 레이블 (설비 ID) 확인:")
unique_labels = set(train_labels)
print(f"   학습 데이터에 사용된 설비 ID: {sorted(unique_labels)}")

# 3. ML 모델 학습
print("\n" + "-" * 70)
ml_matcher = MLMatcher(n_estimators=100, random_state=42)
ml_matcher.train(train_orders, train_labels)

# 4. 웹 앱 시나리오 테스트 - 여러 주문 시도
print("\n" + "-" * 70)
print("웹 앱 시나리오 테스트")
print("-" * 70)

test_orders = [
    Order("TEST-001", weight=10.0, volume=0.5, item_count=5, fragile=True, priority=3, destination_zone="A", order_type="express"),
    Order("TEST-002", weight=50.0, volume=2.5, item_count=100, fragile=False, priority=1, destination_zone="C", order_type="bulk"),
    Order("TEST-003", weight=5.0, volume=0.2, item_count=3, fragile=False, priority=2, destination_zone="B", order_type="standard"),
    Order("TEST-004", weight=2.0, volume=0.1, item_count=1, fragile=True, priority=4, destination_zone="A", order_type="express"),
    Order("TEST-005", weight=25.0, volume=1.2, item_count=30, fragile=False, priority=2, destination_zone="B", order_type="standard"),
]

success_count = 0
fail_count = 0

for order in test_orders:
    result = ml_matcher.predict(order, facilities)

    if result:
        facility, confidence = result
        print(f"\n✅ {order.order_id}: {facility.name} (확신도: {confidence:.2%})")
        print(f"   주문: {order.weight}kg, {order.volume}m³, 우선순위={order.priority}, 깨지기쉬움={order.fragile}")
        print(f"   설비: {facility.facility_id}, 속도={facility.speed_rating}/4")
        success_count += 1
    else:
        print(f"\n❌ {order.order_id}: 매칭 실패")
        print(f"   주문: {order.weight}kg, {order.volume}m³, 우선순위={order.priority}")
        fail_count += 1

# 5. 결과 요약
print("\n" + "=" * 70)
print("테스트 결과 요약")
print("=" * 70)
print(f"성공: {success_count}개")
print(f"실패: {fail_count}개")
print(f"성공률: {success_count / len(test_orders) * 100:.1f}%")

if success_count > 0:
    print("\n🎉 수정 완료! ML 매칭이 정상적으로 작동합니다.")
    print("\n웹 앱에서 사용하려면:")
    print("1. FastAPI: uvicorn webapp.api:app --reload")
    print("   - http://localhost:8000/docs 에서 /train/ml 실행")
    print("   - /match/ml 엔드포인트 테스트")
    print("\n2. Streamlit: streamlit run webapp/streamlit_app.py")
    print("   - 사이드바에서 ML 모델 학습")
    print("   - 주문 정보 입력 후 머신러닝 매칭 버튼 클릭")
else:
    print("\n⚠️ 여전히 문제가 있습니다. 추가 디버깅이 필요합니다.")

print("\n" + "=" * 70)
