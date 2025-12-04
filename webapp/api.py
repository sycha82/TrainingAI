"""FastAPI 백엔드 - 물류센터 설비 매칭 API

.NET 개발자를 위한 설명:
-----------------------
FastAPI는 Python의 ASP.NET Core와 같습니다.
- @app.get() = [HttpGet] 특성
- Pydantic 모델 = DTO (Data Transfer Object)
- Dependency Injection 지원
- 자동 API 문서 생성 (Swagger/OpenAPI)

실행 방법:
    uvicorn webapp.api:app --reload

API 문서 확인:
    http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional
import sys
import os

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.order import Order
from src.models.facility import Facility
from src.engine.matcher import FacilityMatcher
from src.engine.ml_matcher import MLMatcher
from src.data.sample_data import create_sample_facilities
from src.data.training_data_generator import TrainingDataGenerator


# ============================================================================
# DTO 모델 (.NET의 DTO와 동일한 역할)
# ============================================================================

class OrderRequest(BaseModel):
    """주문 요청 DTO (.NET의 Request DTO)"""
    order_id: str = Field(..., description="주문 ID", example="ORD-001")
    weight: float = Field(..., gt=0, description="무게 (kg)", example=10.0)
    volume: float = Field(..., gt=0, description="부피 (m³)", example=0.5)
    item_count: int = Field(..., gt=0, description="품목 수", example=5)
    fragile: bool = Field(default=False, description="깨지기 쉬운 물품 여부")
    priority: int = Field(default=2, ge=1, le=4, description="우선순위 (1-4)")
    destination_zone: str = Field(default="A", description="목적지 구역")
    order_type: str = Field(default="standard", description="주문 유형")

    class Config:
        # .NET의 JsonSerializerOptions와 비슷
        json_schema_extra = {
            "example": {
                "order_id": "ORD-001",
                "weight": 10.0,
                "volume": 0.5,
                "item_count": 5,
                "fragile": True,
                "priority": 3,
                "destination_zone": "A",
                "order_type": "express"
            }
        }


class FacilityResponse(BaseModel):
    """설비 응답 DTO (.NET의 Response DTO)"""
    facility_id: str
    name: str
    facility_type: str
    max_weight: float
    max_volume: float
    can_handle_fragile: bool
    speed_rating: int
    supported_zones: List[str]
    available: bool


class MatchResult(BaseModel):
    """매칭 결과 DTO"""
    success: bool
    facility: Optional[FacilityResponse] = None
    score: Optional[float] = None
    confidence: Optional[float] = None
    engine_type: str  # "rule-based" or "ml"
    message: Optional[str] = None


class HealthResponse(BaseModel):
    """헬스 체크 응답"""
    status: str
    rule_based_engine: str
    ml_engine: str
    available_facilities: int


# ============================================================================
# FastAPI 애플리케이션 (.NET의 Program.cs + Startup.cs)
# ============================================================================

app = FastAPI(
    title="물류센터 설비 매칭 API",
    description="주문에 가장 적합한 설비를 찾아주는 AI 엔진",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc UI
)

# CORS 설정 (.NET의 CORS Middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static 파일 서빙 (.NET의 app.UseStaticFiles())
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


# ============================================================================
# 전역 상태 (.NET의 Singleton Service)
# ============================================================================

class AppState:
    """애플리케이션 상태 (.NET의 Singleton)"""
    def __init__(self):
        self.rule_matcher = FacilityMatcher()
        self.ml_matcher = None  # 학습 후 사용
        self.facilities = create_sample_facilities()


state = AppState()


# ============================================================================
# API 엔드포인트 (.NET의 Controller)
# ============================================================================

@app.get("/", tags=["Health"])
def root():
    """루트 엔드포인트 (.NET의 [HttpGet("/")])"""
    return {
        "message": "물류센터 설비 매칭 API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """헬스 체크 (.NET의 Health Check Middleware)"""
    return HealthResponse(
        status="healthy",
        rule_based_engine="available",
        ml_engine="trained" if state.ml_matcher and state.ml_matcher._is_trained else "not trained",
        available_facilities=len(state.facilities)
    )


@app.get("/facilities", response_model=List[FacilityResponse], tags=["Facilities"])
def get_facilities():
    """사용 가능한 설비 목록 (.NET의 [HttpGet("api/facilities")])"""
    return [
        FacilityResponse(
            facility_id=f.facility_id,
            name=f.name,
            facility_type=f.facility_type,
            max_weight=f.max_weight,
            max_volume=f.max_volume,
            can_handle_fragile=f.can_handle_fragile,
            speed_rating=f.speed_rating,
            supported_zones=f.supported_zones,
            available=f.available
        )
        for f in state.facilities
    ]


@app.post("/match/rule-based", response_model=MatchResult, tags=["Matching"])
def match_rule_based(order_request: OrderRequest):
    """규칙 기반 매칭 (.NET의 [HttpPost("api/match/rule-based")])

    .NET 비유:
        [HttpPost("api/match/rule-based")]
        public ActionResult<MatchResult> MatchRuleBased([FromBody] OrderRequest request)
    """
    try:
        # DTO -> Domain Model 변환 (.NET의 Mapper)
        order = Order(
            order_id=order_request.order_id,
            weight=order_request.weight,
            volume=order_request.volume,
            item_count=order_request.item_count,
            fragile=order_request.fragile,
            priority=order_request.priority,
            destination_zone=order_request.destination_zone,
            order_type=order_request.order_type
        )

        # 매칭 실행
        result = state.rule_matcher.find_best_facility(order, state.facilities)

        if result:
            facility, score = result
            return MatchResult(
                success=True,
                facility=FacilityResponse(
                    facility_id=facility.facility_id,
                    name=facility.name,
                    facility_type=facility.facility_type,
                    max_weight=facility.max_weight,
                    max_volume=facility.max_volume,
                    can_handle_fragile=facility.can_handle_fragile,
                    speed_rating=facility.speed_rating,
                    supported_zones=facility.supported_zones,
                    available=facility.available
                ),
                score=score,
                engine_type="rule-based"
            )
        else:
            return MatchResult(
                success=False,
                engine_type="rule-based",
                message="적합한 설비를 찾을 수 없습니다"
            )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"내부 오류: {str(e)}")


@app.post("/match/ml", response_model=MatchResult, tags=["Matching"])
def match_ml(order_request: OrderRequest):
    """머신러닝 기반 매칭 (.NET의 [HttpPost("api/match/ml")])"""
    if not state.ml_matcher or not state.ml_matcher._is_trained:
        raise HTTPException(
            status_code=503,
            detail="ML 모델이 학습되지 않았습니다. /train/ml을 먼저 호출하세요."
        )

    try:
        order = Order(
            order_id=order_request.order_id,
            weight=order_request.weight,
            volume=order_request.volume,
            item_count=order_request.item_count,
            fragile=order_request.fragile,
            priority=order_request.priority,
            destination_zone=order_request.destination_zone,
            order_type=order_request.order_type
        )

        result = state.ml_matcher.predict(order, state.facilities)

        if result:
            facility, confidence = result
            return MatchResult(
                success=True,
                facility=FacilityResponse(
                    facility_id=facility.facility_id,
                    name=facility.name,
                    facility_type=facility.facility_type,
                    max_weight=facility.max_weight,
                    max_volume=facility.max_volume,
                    can_handle_fragile=facility.can_handle_fragile,
                    speed_rating=facility.speed_rating,
                    supported_zones=facility.supported_zones,
                    available=facility.available
                ),
                confidence=confidence,
                engine_type="ml"
            )
        else:
            return MatchResult(
                success=False,
                engine_type="ml",
                message="적합한 설비를 찾을 수 없습니다"
            )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"내부 오류: {str(e)}")


@app.post("/train/ml", tags=["Training"])
def train_ml_model(num_samples: int = 1000):
    """ML 모델 학습 (.NET의 백그라운드 서비스)

    실제 운영에서는 백그라운드 작업으로 처리해야 합니다.
    .NET의 IHostedService나 Hangfire와 비슷
    """
    try:
        generator = TrainingDataGenerator(seed=42)
        train_orders, train_labels = generator.generate_training_data(num_samples)

        state.ml_matcher = MLMatcher(n_estimators=100, random_state=42)
        result = state.ml_matcher.train(train_orders, train_labels)

        return {
            "message": "ML 모델 학습 완료",
            "num_samples": result["num_samples"],
            "accuracy": result["train_accuracy"],
            "num_features": result["num_features"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"학습 오류: {str(e)}")


# ============================================================================
# 실행 스크립트
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  물류센터 설비 매칭 API 서버                                  ║
    ╚══════════════════════════════════════════════════════════════╝

    서버 시작 중...

    📍 API 엔드포인트:
       - 메인: http://localhost:8000
       - Swagger UI: http://localhost:8000/docs
       - ReDoc: http://localhost:8000/redoc

    🔧 사용 방법:
       1. /train/ml로 ML 모델 학습 (선택)
       2. /match/rule-based 또는 /match/ml로 매칭

    .NET 개발자 참고:
       - FastAPI = ASP.NET Core Web API
       - Swagger UI = Swashbuckle
       - Pydantic = System.ComponentModel.DataAnnotations
    """)

    # .NET의 app.Run()과 동일
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
