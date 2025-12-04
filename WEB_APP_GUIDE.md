# 🌐 웹 애플리케이션 가이드

물류센터 설비 매칭을 웹에서 사용할 수 있는 세 가지 방법을 제공합니다!

## 📋 목차

- [Option 1: FastAPI + HTML (REST API)](#option-1-fastapi--html-rest-api)
- [Option 2: Streamlit (대시보드)](#option-2-streamlit-대시보드)
- [Option 3: FastAPI만 사용 (백엔드)](#option-3-fastapi만-사용-백엔드)
- [.NET 개발자를 위한 가이드](#net-개발자를-위한-가이드)

---

## Option 1: FastAPI + HTML (REST API)

**가장 실전적인 방법** - 프로덕션 환경에 적합

### 특징
- ✅ RESTful API 백엔드
- ✅ 반응형 HTML 프론트엔드
- ✅ 자동 API 문서 (Swagger)
- ✅ .NET ASP.NET Core와 유사

### 실행 방법

#### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

#### 2. API 서버 시작
```bash
# 방법 1: uvicorn 직접 실행
uvicorn webapp.api:app --reload

# 방법 2: Python으로 실행
python -m webapp.api
```

서버가 시작되면:
- 🌐 API: http://localhost:8000
- 📚 Swagger UI: http://localhost:8000/docs
- 📖 ReDoc: http://localhost:8000/redoc
- 🎨 웹 UI: http://localhost:8000/static/index.html

#### 3. (선택) ML 모델 학습

**방법 A: Swagger UI 사용**
1. http://localhost:8000/docs 접속
2. `POST /train/ml` 엔드포인트 찾기
3. "Try it out" 클릭
4. "Execute" 클릭

**방법 B: curl 사용**
```bash
curl -X POST "http://localhost:8000/train/ml?num_samples=1000"
```

**방법 C: Python 코드**
```python
import requests
response = requests.post("http://localhost:8000/train/ml?num_samples=1000")
print(response.json())
```

#### 4. 웹 UI 사용
http://localhost:8000/static/index.html 에서:
1. 주문 정보 입력
2. "규칙 기반 매칭" 또는 "머신러닝 매칭" 클릭
3. 결과 확인!

### API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 루트 (API 정보) |
| GET | `/health` | 헬스 체크 |
| GET | `/facilities` | 설비 목록 |
| POST | `/match/rule-based` | 규칙 기반 매칭 |
| POST | `/match/ml` | ML 매칭 |
| POST | `/train/ml` | ML 모델 학습 |

### 예제 요청

```bash
# 규칙 기반 매칭
curl -X POST "http://localhost:8000/match/rule-based" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "ORD-001",
    "weight": 10.0,
    "volume": 0.5,
    "item_count": 5,
    "fragile": true,
    "priority": 3,
    "destination_zone": "A",
    "order_type": "express"
  }'
```

### .NET 개발자를 위한 비교

```csharp
// C# (ASP.NET Core)
[HttpPost("api/match/rule-based")]
public ActionResult<MatchResult> MatchRuleBased([FromBody] OrderRequest request)
{
    // ...
}
```

```python
# Python (FastAPI)
@app.post("/match/rule-based", response_model=MatchResult)
def match_rule_based(order_request: OrderRequest):
    # ...
```

---

## Option 2: Streamlit (대시보드)

**가장 빠른 프로토타입** - 데이터 사이언스 앱에 적합

### 특징
- ✅ 코드만으로 UI 생성
- ✅ 실시간 인터랙션
- ✅ ML 학습 버튼 내장
- ✅ Blazor보다 간단

### 실행 방법

```bash
streamlit run webapp/streamlit_app.py
```

자동으로 브라우저가 열립니다:
- 🌐 URL: http://localhost:8501

### 기능

1. **사이드바**
   - ML 모델 학습
   - 엔진 상태 확인

2. **주문 매칭 탭**
   - 주문 정보 입력
   - 규칙 기반 / ML 매칭 선택
   - 결과 즉시 표시

3. **설비 목록 탭**
   - 사용 가능한 모든 설비 보기
   - 유형별 필터링

4. **매칭 기록 탭**
   - 과거 매칭 기록 확인
   - 데이터프레임으로 표시

### 사용 예제

1. 왼쪽 사이드바에서 "ML 모델 학습 시작" 클릭 (선택)
2. "주문 매칭" 탭에서 정보 입력
3. "규칙 기반 매칭" 또는 "머신러닝 매칭" 클릭
4. 결과 확인!

---

## Option 3: FastAPI만 사용 (백엔드)

프론트엔드를 별도로 개발하고 싶다면 FastAPI만 실행

### 실행
```bash
uvicorn webapp.api:app --reload
```

### 통합 예제

**React/Vue.js/Angular와 통합:**
```javascript
// JavaScript (Fetch API)
async function matchOrder(orderData) {
    const response = await fetch('http://localhost:8000/match/rule-based', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
    });
    return await response.json();
}
```

**Blazor와 통합:**
```csharp
// C# (HttpClient)
public async Task<MatchResult> MatchOrderAsync(OrderRequest request)
{
    var response = await _httpClient.PostAsJsonAsync(
        "http://localhost:8000/match/rule-based",
        request
    );
    return await response.Content.ReadFromJsonAsync<MatchResult>();
}
```

---

## .NET 개발자를 위한 가이드

### 기술 스택 비교

| Python | .NET/C# |
|--------|---------|
| FastAPI | ASP.NET Core Web API |
| Pydantic | FluentValidation / DataAnnotations |
| Uvicorn | Kestrel |
| Streamlit | Blazor Server (간소화 버전) |

### 주요 개념 매핑

**1. Dependency Injection**
```python
# Python (FastAPI)
@app.on_event("startup")
def startup():
    state.rule_matcher = FacilityMatcher()
```
```csharp
// C# (ASP.NET Core)
services.AddSingleton<FacilityMatcher>();
```

**2. Middleware**
```python
# Python
app.add_middleware(CORSMiddleware, ...)
```
```csharp
// C#
app.UseCors(...);
```

**3. Model Validation**
```python
# Python (Pydantic)
class OrderRequest(BaseModel):
    weight: float = Field(..., gt=0)
```
```csharp
// C# (DataAnnotations)
public class OrderRequest
{
    [Range(0.1, double.MaxValue)]
    public double Weight { get; set; }
}
```

### 디버깅

**Python (FastAPI)**
```bash
# 디버그 모드 실행
uvicorn webapp.api:app --reload --log-level debug
```

**C# (ASP.NET Core)**
```bash
# 디버그 모드 실행
dotnet run --environment Development
```

---

## 성능 비교

| 항목 | FastAPI | Streamlit |
|------|---------|-----------|
| 시작 속도 | ⚡ 빠름 | 보통 |
| 프로덕션 | ✅ 적합 | ⚠️ 프로토타입용 |
| API 문서 | ✅ 자동 생성 | ❌ 없음 |
| 커스터마이징 | ✅ 완전 제어 | ⚠️ 제한적 |
| 학습 곡선 | 보통 | ⚡ 매우 낮음 |

---

## 운영 환경 배포

### Docker (권장)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "webapp.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# 빌드 및 실행
docker build -t logistics-api .
docker run -p 8000:8000 logistics-api
```

### 클라우드 배포

**Azure (App Service)**
```bash
az webapp up --name logistics-api --resource-group myResourceGroup
```

**AWS (Elastic Beanstalk)**
```bash
eb init -p python-3.11 logistics-api
eb create logistics-env
eb deploy
```

---

## 문제 해결

### 포트가 이미 사용 중
```bash
# 다른 포트 사용
uvicorn webapp.api:app --port 8001
streamlit run webapp/streamlit_app.py --server.port 8502
```

### CORS 오류
FastAPI의 `allow_origins`를 프론트엔드 도메인으로 변경:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 등
    ...
)
```

### ML 모델 미학습 오류
```bash
# API를 통해 학습
curl -X POST "http://localhost:8000/train/ml"
```

---

## 다음 단계

1. **프로덕션 배포**
   - Docker 컨테이너화
   - 클라우드 배포 (Azure/AWS)

2. **인증 추가**
   - JWT 토큰
   - OAuth 2.0

3. **데이터베이스 연동**
   - PostgreSQL / MongoDB
   - ORM (SQLAlchemy)

4. **모니터링**
   - Prometheus + Grafana
   - Application Insights

---

**축하합니다! 이제 웹에서 AI 엔진을 사용할 수 있습니다!** 🎉
