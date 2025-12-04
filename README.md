# 🏭 물류센터 설비 AI 매칭 엔진

물류센터 주문의 여러 속성을 분석하여 가장 적합한 설비를 자동으로 찾아주는 AI 엔진입니다.

## 📋 목차

- [소개](#소개)
- [주요 기능](#주요-기능)
- [프로젝트 구조](#프로젝트-구조)
- [시작하기](#시작하기)
- [사용 방법](#사용-방법)
- [예제](#예제)
- [커스터마이징](#커스터마이징)
- [향후 계획](#향후-계획)

## 🎯 소개

이 프로젝트는 **파이썬 초보자**도 쉽게 이해하고 사용할 수 있도록 설계된 물류센터 자동화 시스템입니다.

### 해결하는 문제

- 수많은 주문을 어떤 설비로 처리해야 할까?
- 긴급 주문은 어떤 설비가 가장 빠를까?
- 깨지기 쉬운 물품은 어디로 보내야 안전할까?
- 설비 용량을 효율적으로 활용하려면?

### AI 매칭 방식

여러 요소를 점수화하여 최적의 설비를 선택합니다:

1. **용량 활용률** (25%) - 설비를 효율적으로 사용하는가?
2. **처리 속도** (25%) - 주문 우선순위에 맞는 속도인가?
3. **깨지기 쉬운 물품 처리** (20%) - 안전하게 처리할 수 있는가?
4. **목적지 구역** (15%) - 목적지까지 직접 연결되는가?
5. **설비 유형** (15%) - 주문 특성에 맞는 설비 유형인가?

> 가중치는 필요에 따라 조정 가능합니다!

## ✨ 주요 기능

- ✅ **자동 매칭**: 주문에 가장 적합한 설비 자동 선택
- ✅ **순위 매기기**: 여러 후보 설비를 점수순으로 정렬
- ✅ **일괄 처리**: 여러 주문을 한번에 처리
- ✅ **커스텀 가중치**: 상황에 맞게 매칭 기준 조정
- ✅ **검증 로직**: 잘못된 데이터 자동 차단
- ✅ **확장 가능**: 새로운 속성 추가 용이

## 📁 프로젝트 구조

```
TrainingAI/
├── README.md                    # 이 파일
├── requirements.txt             # 필요한 패키지 목록
├── src/                         # 소스 코드
│   ├── models/                  # 데이터 모델
│   │   ├── order.py            # 주문 클래스
│   │   └── facility.py         # 설비 클래스
│   ├── engine/                  # AI 엔진
│   │   └── matcher.py          # 매칭 알고리즘
│   └── data/                    # 샘플 데이터
│       └── sample_data.py      # 예제 데이터 생성
└── examples/                    # 사용 예제
    └── basic_matching.py       # 기본 사용법
```

## 🚀 시작하기

### 1. 필수 요구사항

- Python 3.7 이상
- 현재는 외부 패키지 불필요 (표준 라이브러리만 사용)

### 2. 설치

```bash
# 저장소 클론 (이미 되어있다면 생략)
cd TrainingAI

# (선택) 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치 (현재는 없음)
pip install -r requirements.txt
```

### 3. 예제 실행

```bash
python examples/basic_matching.py
```

## 📖 사용 방법

### 기본 사용법

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
