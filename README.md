# 🏭 물류센터 설비 AI 매칭 엔진

물류센터 주문의 여러 속성을 분석하여 가장 적합한 설비를 자동으로 찾아주는 AI 엔진입니다.

## 📋 목차

- [소개](#소개)
- [주요 기능](#주요-기능)
- [프로젝트 구조](#프로젝트-구조)
- [시작하기](#시작하기)
- [사용 방법](#사용-방법)
- [예제](#예제)
- [실습 및 테스트](#실습-및-테스트)
- [커스터마이징](#커스터마이징)
- [향후 계획](#향후-계획)

## 🎯 소개

이 프로젝트는 **파이썬 초보자**와 **.NET 개발자**도 쉽게 이해하고 사용할 수 있도록 설계된 물류센터 자동화 시스템입니다.

### 해결하는 문제

- 수많은 주문을 어떤 설비로 처리해야 할까?
- 긴급 주문은 어떤 설비가 가장 빠를까?
- 깨지기 쉬운 물품은 어디로 보내야 안전할까?
- 설비 용량을 효율적으로 활용하려면?

### 두 가지 매칭 엔진

#### 📐 규칙 기반 엔진 (Rule-based)

여러 요소를 점수화하여 최적의 설비를 선택합니다:

1. **용량 활용률** (25%) - 설비를 효율적으로 사용하는가?
2. **처리 속도** (25%) - 주문 우선순위에 맞는 속도인가?
3. **깨지기 쉬운 물품 처리** (20%) - 안전하게 처리할 수 있는가?
4. **목적지 구역** (15%) - 목적지까지 직접 연결되는가?
5. **설비 유형** (15%) - 주문 특성에 맞는 설비 유형인가?

- ✅ 투명하고 예측 가능
- ✅ 빠른 실행 속도
- ✅ 설명 가능한 의사결정

#### 🤖 머신러닝 엔진 (ML-based)

과거 운영 데이터를 학습하여 패턴을 자동으로 발견합니다:

- ✅ **데이터 학습**: 과거 매칭 데이터에서 패턴 학습
- ✅ **자동 최적화**: 비즈니스 환경 변화에 적응
- ✅ **높은 정확도**: 복잡한 패턴 인식
- ✅ **특성 중요도**: 어떤 요소가 중요한지 자동 분석

**Random Forest Classifier** 사용 (scikit-learn)

## ✨ 주요 기능

### 규칙 기반 엔진
- ✅ **자동 매칭**: 주문에 가장 적합한 설비 자동 선택
- ✅ **순위 매기기**: 여러 후보 설비를 점수순으로 정렬
- ✅ **일괄 처리**: 여러 주문을 한번에 처리
- ✅ **커스텀 가중치**: 상황에 맞게 매칭 기준 조정

### 머신러닝 엔진 🆕
- ✅ **데이터 학습**: 과거 매칭 데이터로 모델 훈련
- ✅ **예측 추론**: 학습된 패턴으로 최적 설비 예측
- ✅ **모델 평가**: 정확도 및 성능 측정
- ✅ **특성 분석**: 중요한 요소 자동 발견
- ✅ **모델 저장/로드**: 한번 학습 후 재사용

### 공통
- ✅ **검증 로직**: 잘못된 데이터 자동 차단
- ✅ **확장 가능**: 새로운 속성 추가 용이
- ✅ **완전한 테스트**: 27개 자동화 테스트

## 📁 프로젝트 구조

```
TrainingAI/
├── README.md                         # 이 파일
├── PRACTICE_GUIDE.md                 # 실습 가이드
├── requirements.txt                  # 필요한 패키지 (numpy, scikit-learn)
├── src/                              # 소스 코드
│   ├── models/                       # 데이터 모델
│   │   ├── order.py                 # 주문 클래스
│   │   └── facility.py              # 설비 클래스
│   ├── engine/                       # 매칭 엔진
│   │   ├── matcher.py               # 규칙 기반 엔진
│   │   └── ml_matcher.py            # 머신러닝 엔진 🆕
│   └── data/                         # 데이터 생성
│       ├── sample_data.py           # 샘플 데이터
│       └── training_data_generator.py  # ML 학습 데이터 생성기 🆕
├── examples/                         # 사용 예제
│   ├── basic_matching.py            # 규칙 기반 예제
│   ├── ml_matching.py               # 머신러닝 예제 🆕
│   ├── compare_engines.py           # 두 엔진 비교 🆕
│   └── interactive_practice.py      # 대화형 실습
├── exercises/                        # 단계별 연습 문제
│   ├── beginner_exercises.py
│   ├── intermediate_exercises.py
│   └── advanced_exercises.py
└── tests/                            # 자동화 테스트
    ├── test_basic.py                # 기본 테스트 (14개)
    └── test_ml.py                   # ML 테스트 (13개) 🆕
```

## 🚀 시작하기

### 1. 필수 요구사항

- Python 3.7 이상
- **머신러닝 엔진 사용 시**: numpy, scikit-learn, joblib

### 2. 설치

```bash
# 저장소 클론 (이미 되어있다면 생략)
cd TrainingAI

# (선택) 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

> **참고**: 규칙 기반 엔진만 사용한다면 외부 패키지 불필요합니다.
> ML 엔진을 사용하려면 numpy와 scikit-learn이 필요합니다.

### 3. 예제 실행

```bash
# 규칙 기반 엔진 예제
python examples/basic_matching.py

# 머신러닝 엔진 예제 🆕
python examples/ml_matching.py

# 두 엔진 비교 🆕
python examples/compare_engines.py
```

## 📖 사용 방법

### 규칙 기반 엔진 사용법

```python
from src.models.order import Order
from src.models.facility import Facility
from src.engine.matcher import FacilityMatcher

# 1. 주문 생성
order = Order(
    order_id="ORD-001",
    weight=10.0,        # 무게 (kg)
    volume=0.5,         # 부피 (m³)
    item_count=15,      # 품목 수
    fragile=True,       # 깨지기 쉬운 물품
    priority=3,         # 우선순위 (1~4)
    destination_zone="A",
    order_type="express"
)

# 2. 설비 목록 준비
facilities = [
    Facility(
        facility_id="FAC-001",
        name="고속 컨베이어",
        facility_type="conveyor",
        max_weight=30.0,
        max_volume=1.5,
        can_handle_fragile=True,
        speed_rating=4,
        supported_zones=["A", "B"]
    ),
    # ... 더 많은 설비
]

# 3. AI 매칭 엔진 생성
matcher = FacilityMatcher()

# 4. 최적 설비 찾기
result = matcher.find_best_facility(order, facilities)

if result:
    facility, score = result
    print(f"최적 설비: {facility.name}")
    print(f"매칭 점수: {score:.2%}")
```

### 머신러닝 엔진 사용법 🆕

```python
from src.engine.ml_matcher import MLMatcher
from src.data.training_data_generator import TrainingDataGenerator

# 1. 학습 데이터 생성
generator = TrainingDataGenerator(seed=42)
train_orders, train_labels = generator.generate_training_data(1000)

# 2. ML 모델 생성 및 학습
ml_matcher = MLMatcher(n_estimators=100, random_state=42)
ml_matcher.train(train_orders, train_labels)

# 3. 새 주문 예측
order = Order(...)  # 주문 생성
facilities = generator.generate_facilities()

result = ml_matcher.predict(order, facilities)

if result:
    facility, confidence = result
    print(f"예측 설비: {facility.name}")
    print(f"확신도: {confidence:.2%}")

# 4. 모델 저장 (재사용)
ml_matcher.save_model("model.pkl")

# 5. 나중에 로드
new_matcher = MLMatcher()
new_matcher.load_model("model.pkl")
```

> **.NET 개발자를 위한 팁**:
> - `train()` = ML.NET의 `Fit()`
> - `predict()` = ML.NET의 `Predict()`
> - `save_model()` = `Model.Save()`
> - Random Forest = 의사결정나무 앙상블 (배깅)

## 💡 예제

프로젝트에는 4가지 예제가 포함되어 있습니다:

1. **단일 주문 매칭** - 하나의 주문에 최적 설비 찾기
2. **설비 순위** - 여러 후보 설비 점수순 정렬
3. **일괄 처리** - 여러 주문 한번에 처리
4. **커스텀 가중치** - 상황별 가중치 조정

```bash
# 모든 예제 실행
python examples/basic_matching.py
```

### 예제 출력 (일부)

```
📦 예제 1: 단일 주문에 최적 설비 찾기
================================================================================

주문 정보:
  - ID: ORD-100
  - 무게: 8.0kg, 부피: 0.4m³
  - 품목 수: 10개
  - 깨지기 쉬움: 예
  - 우선순위: 3 (4=긴급)
  - 목적지 구역: A
  - 주문 유형: express

✅ 최적 설비 발견!
  - 설비 ID: FAC-003
  - 설비 이름: 로봇 픽커 R1
  - 설비 유형: robot
  - 매칭 점수: 87.50%
```

## 🎓 실습 및 테스트

파이썬 초보자를 위한 다양한 실습 자료가 준비되어 있습니다!

### 📖 실습 가이드

자세한 실습 방법은 [PRACTICE_GUIDE.md](PRACTICE_GUIDE.md)를 참고하세요.

### 1. 인터랙티브 실습

직접 값을 입력하면서 배울 수 있는 대화형 실습:

```bash
python examples/interactive_practice.py
```

메뉴에서 선택하여:
- 나만의 주문 만들기
- AI 매칭 실행해보기
- 가중치 커스터마이징
- 빠른 테스트 실행

### 2. 단계별 연습 문제

#### 초급 (beginner_exercises.py)
```bash
python exercises/beginner_exercises.py
```
- Order, Facility 객체 생성
- 기본 메서드 사용법
- 조건문과 반복문

#### 중급 (intermediate_exercises.py)
```bash
python exercises/intermediate_exercises.py
```
- FacilityMatcher 사용
- 최적 설비 찾기
- 일괄 처리
- 커스텀 가중치 설정

#### 고급 (advanced_exercises.py)
```bash
python exercises/advanced_exercises.py
```
- 성능 분석 및 통계
- 설비 가용성 시뮬레이션
- 새로운 기능 확장
- 복잡한 비즈니스 로직

### 3. 자동 테스트

프로그램이 제대로 동작하는지 확인:

```bash
python tests/test_basic.py
```

14개의 테스트 케이스가 자동으로 실행됩니다:
- Order 클래스 테스트
- Facility 클래스 테스트
- FacilityMatcher 테스트

### 📚 학습 경로 (추천)

**파이썬 처음이라면:**
1. 기본 예제 실행 → 2. 인터랙티브 실습 → 3. 초급 연습 문제 → 4. 테스트 실행

**파이썬 기본을 아신다면:**
1. 기본 예제 확인 → 2. 중급 연습 문제 → 3. 인터랙티브 실습으로 실험

**실전 프로젝트를 원한다면:**
1. 고급 연습 문제 → 2. 새 기능 추가 → 3. 테스트 작성 → 4. 최적화

## 🎨 커스터마이징

### 1. 가중치 조정

상황에 맞게 매칭 기준을 조정할 수 있습니다:

```python
# 속도 우선 (긴급 주문이 많을 때)
matcher = FacilityMatcher(
    weight_capacity=0.1,
    weight_speed=0.5,    # 속도 가중치 높임
    weight_fragile=0.2,
    weight_zone=0.1,
    weight_type=0.1
)

# 효율성 우선 (비용 절감이 중요할 때)
matcher = FacilityMatcher(
    weight_capacity=0.6,  # 용량 활용률 가중치 높임
    weight_speed=0.1,
    weight_fragile=0.1,
    weight_zone=0.1,
    weight_type=0.1
)
```

### 2. 새로운 주문 속성 추가

`src/models/order.py`에서 Order 클래스를 확장:

```python
@dataclass
class Order:
    # 기존 속성...
    temperature_controlled: bool = False  # 온도 관리 필요
    delivery_deadline: str = None         # 배송 마감시간
```

### 3. 새로운 설비 유형 추가

`src/models/facility.py`와 `src/engine/matcher.py` 수정

## 📚 주요 클래스 설명

### Order (주문)

| 속성 | 타입 | 설명 |
|------|------|------|
| order_id | str | 주문 고유 ID |
| weight | float | 무게 (kg) |
| volume | float | 부피 (m³) |
| item_count | int | 품목 수 |
| fragile | bool | 깨지기 쉬운 물품 여부 |
| priority | int | 우선순위 (1~4) |
| destination_zone | str | 목적지 구역 |
| order_type | str | 주문 유형 |

### Facility (설비)

| 속성 | 타입 | 설명 |
|------|------|------|
| facility_id | str | 설비 고유 ID |
| name | str | 설비 이름 |
| facility_type | str | 설비 유형 |
| max_weight | float | 최대 처리 무게 |
| max_volume | float | 최대 처리 부피 |
| can_handle_fragile | bool | 깨지기 쉬운 물품 처리 가능 |
| speed_rating | int | 속도 등급 (1~4) |
| supported_zones | List[str] | 지원 구역 |
| available | bool | 사용 가능 여부 |

### FacilityMatcher (매칭 엔진)

| 메서드 | 설명 |
|--------|------|
| `find_best_facility()` | 최적 설비 1개 찾기 |
| `rank_facilities()` | 설비 순위 매기기 |
| `batch_match()` | 여러 주문 일괄 매칭 |
| `calculate_score()` | 매칭 점수 계산 |

## 🔮 향후 계획

- [ ] 머신러닝 모델 통합 (scikit-learn)
- [ ] 실시간 설비 가용성 추적
- [ ] 데이터베이스 연동
- [ ] 웹 API 제공 (FastAPI/Flask)
- [ ] 대시보드 UI
- [ ] 성능 최적화 및 캐싱
- [ ] 상세한 분석 리포트 생성
- [ ] 설비 점유율 예측

## 🤝 기여하기

개선 아이디어나 버그 제보는 언제나 환영합니다!

## 📄 라이선스

MIT License

## 💬 문의

질문이나 제안사항이 있으시면 이슈를 등록해주세요.

---

**파이썬 처음이세요?** 걱정 마세요! 이 프로젝트는 초보자도 이해할 수 있도록 만들어졌습니다.
코드를 천천히 읽어보고, 예제를 실행해보면서 하나씩 배워가세요. 🚀
