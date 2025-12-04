# 📚 실습 가이드

파이썬 초보자를 위한 단계별 실습 가이드입니다. 이 문서를 따라하면서 물류센터 AI 엔진을 직접 사용하고 테스트해볼 수 있습니다.

## 📖 목차

1. [빠른 시작](#빠른-시작)
2. [인터랙티브 실습](#인터랙티브-실습)
3. [단계별 연습 문제](#단계별-연습-문제)
4. [테스트 실행](#테스트-실행)
5. [Python 기초 개념](#python-기초-개념)
6. [문제 해결 가이드](#문제-해결-가이드)

---

## 🚀 빠른 시작

### 1. 예제 실행해보기

가장 먼저 기본 예제를 실행해서 어떻게 동작하는지 확인하세요:

```bash
# 기본 예제 실행
python examples/basic_matching.py
```

이 명령어는 4가지 예제를 자동으로 실행하고 결과를 보여줍니다:
- 단일 주문 매칭
- 설비 순위 매기기
- 여러 주문 일괄 처리
- 커스텀 가중치 설정

### 2. 인터랙티브 실습

직접 값을 입력하면서 배우고 싶다면:

```bash
# 대화형 실습 실행
python examples/interactive_practice.py
```

메뉴가 나타나면 숫자를 입력하여 원하는 실습을 선택할 수 있습니다.

---

## 🎮 인터랙티브 실습

`interactive_practice.py`는 직접 값을 입력하면서 배울 수 있는 대화형 실습입니다.

### 사용 방법

```bash
python examples/interactive_practice.py
```

### 메뉴 설명

1. **나만의 주문 만들기** (초보자 추천)
   - 주문 정보를 직접 입력
   - 무게, 부피, 우선순위 등을 설정
   - 입력값이 어떻게 주문 객체가 되는지 확인

2. **AI 매칭 실행하기**
   - 만든 주문에 최적의 설비 찾기
   - 왜 그 설비가 선택되었는지 이유 확인
   - 전체 설비 순위도 볼 수 있음

3. **가중치 커스터마이징**
   - 각 요소의 중요도를 직접 조정
   - 가중치 변경에 따른 결과 차이 확인

4. **빠른 테스트**
   - 미리 정의된 시나리오로 빠르게 테스트
   - 여러 상황을 한번에 확인

5. **처음부터 다시**
   - 1번과 2번을 순서대로 실행
   - 전체 흐름을 한번에 체험

### 실습 예시

```
📚 실습 메뉴:
  1. 나만의 주문 만들기
  2. AI 매칭 실행하기 (1번 먼저 필요)
  3. 가중치 커스터마이징
  4. 빠른 테스트 (미리 정의된 시나리오)
  5. 처음부터 다시 (1→2 순서대로)
  0. 종료

선택하세요: 1

주문 정보를 입력하세요 (엔터 = 기본값 사용)

주문 ID (예: ORD-999) [ORD-TEST]: MY-ORDER
무게 (kg) [10.0]: 15.5
부피 (m³) [0.5]: 0.8
품목 수 [5]: 12
깨지기 쉬운 물품? (y/n) [n]: y
...
```

---

## 📝 단계별 연습 문제

코드를 직접 작성하면서 배우는 단계별 연습 문제입니다.

### 초급 (Beginner)

```bash
python exercises/beginner_exercises.py
```

**배우는 내용:**
- Order 객체 생성하기
- Facility 객체 생성하기
- 메서드 호출하기 (get_density, is_heavy 등)
- 기본 조건문과 반복문

**진행 방법:**
1. 파일을 텍스트 에디터로 열기
2. `# TODO: 여기에 코드를 작성하세요` 부분 찾기
3. 힌트를 참고하여 코드 작성
4. 정답을 보려면 주석 해제

**예시:**
```python
# TODO: 여기에 코드를 작성하세요
# order = Order(...)

# ============ 정답 (주석 해제하여 확인) ============
# order = Order(
#     order_id="MY-ORDER-001",
#     weight=12.5,
#     ...
# )
```

### 중급 (Intermediate)

```bash
python exercises/intermediate_exercises.py
```

**배우는 내용:**
- FacilityMatcher 사용하기
- find_best_facility 메서드
- rank_facilities로 순위 매기기
- batch_match로 일괄 처리
- 커스텀 가중치 설정

**주요 연습:**
1. AI 매칭 엔진 기본 사용
2. 설비 순위 매기기
3. 여러 주문 일괄 처리
4. 가중치 변경 효과 확인
5. 나만의 설비 디자인

### 고급 (Advanced)

```bash
python exercises/advanced_exercises.py
```

**배우는 내용:**
- 성능 분석 및 통계
- 설비 가용성 시뮬레이션
- 클래스 확장하기
- 복잡한 비즈니스 로직 구현

**주요 연습:**
1. 매칭 성공률, 평균 점수 계산
2. 설비별 주문 할당 현황 분석
3. 여러 가중치 조합 비교
4. 설비 사용 중 시나리오 시뮬레이션
5. 실전 비즈니스 규칙 구현

---

## 🧪 테스트 실행

프로그램이 제대로 동작하는지 확인하는 자동 테스트입니다.

### 테스트 실행하기

```bash
python tests/test_basic.py
```

### 테스트 결과 읽는 법

```
test_can_handle_order (test_basic.TestFacility) ... ok
test_capacity_utilization (test_basic.TestFacility) ... ok
test_facility_creation (test_basic.TestFacility) ... ok
...

----------------------------------------------------------------------
Ran 13 tests in 0.005s

OK

================================================================================
테스트 결과 요약
================================================================================
실행된 테스트: 13개
성공: 13개
실패: 0개
오류: 0개
```

- `ok` - 테스트 성공
- `FAIL` - 예상과 다른 결과
- `ERROR` - 코드 실행 중 오류

### 테스트 파일 구조

```python
class TestOrder(unittest.TestCase):
    """주문 테스트"""

    def test_order_creation(self):
        """주문 생성 테스트"""
        order = Order(...)
        self.assertEqual(order.order_id, "TEST-001")
```

**주요 검증 메서드:**
- `assertEqual(a, b)` - a와 b가 같은지
- `assertTrue(x)` - x가 True인지
- `assertFalse(x)` - x가 False인지
- `assertGreater(a, b)` - a가 b보다 큰지
- `assertIsNone(x)` - x가 None인지

---

## 🐍 Python 기초 개념

### 1. 클래스와 객체

```python
# 클래스 정의 (설계도)
class Order:
    def __init__(self, order_id, weight):
        self.order_id = order_id
        self.weight = weight

# 객체 생성 (실제 사용)
order = Order("ORD-001", 10.0)
print(order.order_id)  # "ORD-001"
```

### 2. 메서드 호출

```python
# 객체의 메서드 호출
density = order.get_density()  # 메서드 호출
is_heavy = order.is_heavy()    # 메서드 호출
```

### 3. 리스트

```python
# 리스트 생성
orders = [order1, order2, order3]

# 반복문으로 순회
for order in orders:
    print(order.order_id)
```

### 4. 조건문

```python
# if-else 문
if order.is_heavy():
    print("무거운 주문입니다")
else:
    print("가벼운 주문입니다")
```

### 5. 딕셔너리

```python
# 키-값 쌍으로 데이터 저장
results = {
    "ORD-001": facility1,
    "ORD-002": facility2
}

# 값 가져오기
facility = results["ORD-001"]
```

---

## 🔧 문제 해결 가이드

### 자주 발생하는 오류

#### 1. ModuleNotFoundError

```
ModuleNotFoundError: No module named 'src'
```

**해결방법:**
```bash
# 프로젝트 루트 디렉토리에서 실행하세요
cd /home/user/TrainingAI
python examples/basic_matching.py
```

#### 2. ImportError

```
ImportError: cannot import name 'Order'
```

**원인:** 파일 경로가 잘못되었거나 파일이 없음

**해결방법:**
```bash
# 파일이 있는지 확인
ls src/models/order.py
```

#### 3. ValueError

```
ValueError: 무게는 0 이상이어야 합니다
```

**원인:** 잘못된 값 입력 (예: 음수 무게)

**해결방법:** 올바른 값으로 수정
```python
# 잘못된 예
order = Order("ORD-001", weight=-10.0, ...)  # ❌

# 올바른 예
order = Order("ORD-001", weight=10.0, ...)   # ✅
```

#### 4. AttributeError

```
AttributeError: 'Order' object has no attribute 'weigth'
```

**원인:** 오타 (weigth → weight)

**해결방법:** 철자 확인
```python
# 잘못된 예
print(order.weigth)  # ❌

# 올바른 예
print(order.weight)  # ✅
```

### 디버깅 팁

#### 1. print()로 값 확인

```python
order = Order(...)
print(f"주문 정보: {order}")
print(f"무게: {order.weight}")
```

#### 2. type()으로 타입 확인

```python
result = matcher.find_best_facility(...)
print(f"결과 타입: {type(result)}")  # <class 'tuple'> 또는 <class 'NoneType'>
```

#### 3. dir()로 사용 가능한 메서드 확인

```python
order = Order(...)
print(dir(order))  # 사용 가능한 모든 메서드 목록
```

---

## 💡 실습 진행 순서 (추천)

### 초급자 (파이썬 처음)

1. ✅ **기본 예제 실행** (`basic_matching.py`)
   - 프로그램이 어떻게 동작하는지 확인

2. ✅ **인터랙티브 실습** (`interactive_practice.py`)
   - 직접 값을 입력하면서 체험

3. ✅ **초급 연습 문제** (`beginner_exercises.py`)
   - 간단한 코드 작성 연습

4. ✅ **코드 읽어보기**
   - `src/models/order.py` 파일 열어서 천천히 읽기
   - 각 줄이 무슨 의미인지 이해하기

5. ✅ **테스트 실행** (`test_basic.py`)
   - 자동 테스트가 어떻게 작동하는지 확인

### 중급자 (파이썬 기본 지식 있음)

1. ✅ **기본 예제 빠르게 확인**
2. ✅ **중급 연습 문제** (`intermediate_exercises.py`)
3. ✅ **인터랙티브 실습으로 실험**
4. ✅ **코드 수정해보기**
   - 주문 속성 변경
   - 설비 추가
   - 가중치 조정

### 고급자 (실전 프로젝트 준비)

1. ✅ **고급 연습 문제** (`advanced_exercises.py`)
2. ✅ **새로운 기능 추가**
   - 새 속성 (온도 관리, 배송 시간 등)
   - 새 설비 유형
   - 복잡한 매칭 규칙
3. ✅ **테스트 작성**
   - 새 기능에 대한 테스트 케이스 추가
4. ✅ **최적화**
   - 성능 개선
   - 더 나은 알고리즘

---

## 🎯 학습 목표 체크리스트

### 기본 개념

- [ ] Order 객체를 만들 수 있다
- [ ] Facility 객체를 만들 수 있다
- [ ] 메서드를 호출할 수 있다
- [ ] 조건문과 반복문을 사용할 수 있다

### AI 매칭 엔진

- [ ] FacilityMatcher를 생성할 수 있다
- [ ] find_best_facility를 사용할 수 있다
- [ ] rank_facilities로 순위를 매길 수 있다
- [ ] batch_match로 일괄 처리할 수 있다
- [ ] 커스텀 가중치를 설정할 수 있다

### 고급 활용

- [ ] 새로운 속성을 추가할 수 있다
- [ ] 비즈니스 규칙을 구현할 수 있다
- [ ] 테스트 케이스를 작성할 수 있다
- [ ] 성능을 분석할 수 있다

---

## 📚 추가 학습 자료

### Python 기초

- [Python 공식 튜토리얼](https://docs.python.org/ko/3/tutorial/)
- [점프 투 파이썬](https://wikidocs.net/book/1)

### 객체지향 프로그래밍

- 클래스와 객체 개념
- 상속과 다형성
- 캡슐화

### 테스트

- unittest 프레임워크
- 테스트 주도 개발 (TDD)

---

## 🤝 도움이 필요하세요?

1. **README.md** - 프로젝트 전체 개요
2. **코드 주석** - 각 파일의 상세 설명
3. **연습 문제 정답** - 주석 해제하여 확인
4. **테스트 코드** - 올바른 사용법 참고

---

**즐거운 코딩 되세요! 🚀**
