"""Streamlit 대시보드 - 물류센터 설비 매칭

.NET 개발자를 위한 설명:
-----------------------
Streamlit은 Python의 빠른 프로토타이핑 도구입니다.
- Blazor나 WPF보다 훨씬 간단
- 코드만으로 UI 자동 생성
- 데이터 사이언스/ML 앱에 특화

실행 방법:
    streamlit run webapp/streamlit_app.py

브라우저 자동 열림:
    http://localhost:8501
"""

import streamlit as st
import sys
import os
import time

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.order import Order
from src.models.facility import Facility
from src.engine.matcher import FacilityMatcher
from src.engine.ml_matcher import MLMatcher
from src.data.sample_data import create_sample_facilities
from src.data.training_data_generator import TrainingDataGenerator


# ============================================================================
# 페이지 설정
# ============================================================================

st.set_page_config(
    page_title="물류센터 설비 매칭",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# 세션 상태 초기화 (.NET의 Session/State Management)
# ============================================================================

if 'rule_matcher' not in st.session_state:
    st.session_state.rule_matcher = FacilityMatcher()

if 'ml_matcher' not in st.session_state:
    st.session_state.ml_matcher = None

if 'facilities' not in st.session_state:
    st.session_state.facilities = create_sample_facilities()

if 'match_history' not in st.session_state:
    st.session_state.match_history = []


# ============================================================================
# 사이드바 - 설정 및 학습
# ============================================================================

with st.sidebar:
    st.title("⚙️ 설정")

    st.header("ML 모델 학습")

    if st.button("🎓 ML 모델 학습 시작", use_container_width=True):
        with st.spinner("학습 중... 잠시만 기다려주세요."):
            generator = TrainingDataGenerator(seed=42)
            train_orders, train_labels = generator.generate_training_data(500)

            st.session_state.ml_matcher = MLMatcher(n_estimators=100, random_state=42)
            result = st.session_state.ml_matcher.train(train_orders, train_labels)

            st.success(f"✅ 학습 완료! 정확도: {result['train_accuracy']:.2%}")
            st.balloons()

    # ML 상태 표시
    st.divider()
    st.header("엔진 상태")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("규칙 기반", "✅ 사용 가능")
    with col2:
        ml_status = "✅ 학습됨" if (st.session_state.ml_matcher and
                                  st.session_state.ml_matcher._is_trained) else "❌ 미학습"
        st.metric("머신러닝", ml_status)

    st.metric("사용 가능 설비", len(st.session_state.facilities))


# ============================================================================
# 메인 페이지
# ============================================================================

st.title("🏭 물류센터 설비 AI 매칭 시스템")
st.markdown("주문 정보를 입력하면 AI가 최적의 설비를 추천해드립니다")

st.divider()

# ============================================================================
# 탭 구성
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs(["📦 주문 매칭", "🏭 설비 목록", "📊 매칭 기록", "ℹ️ 도움말"])


# ----------------------------------------------------------------------------
# 탭 1: 주문 매칭
# ----------------------------------------------------------------------------
with tab1:
    st.header("주문 정보 입력")

    col1, col2 = st.columns(2)

    with col1:
        order_id = st.text_input("주문 ID", value="ORD-001", placeholder="ORD-XXX")
        weight = st.number_input("무게 (kg)", min_value=0.1, max_value=200.0, value=10.0, step=0.5)
        volume = st.number_input("부피 (m³)", min_value=0.01, max_value=10.0, value=0.5, step=0.1)
        item_count = st.number_input("품목 수", min_value=1, max_value=500, value=5, step=1)

    with col2:
        fragile = st.checkbox("깨지기 쉬운 물품", value=False)
        priority = st.select_slider("우선순위", options=[1, 2, 3, 4],
                                    value=2,
                                    format_func=lambda x: {1: "낮음", 2: "보통", 3: "높음", 4: "긴급"}[x])
        destination_zone = st.selectbox("목적지 구역", options=["A", "B", "C"], index=0)
        order_type = st.selectbox("주문 유형", options=["standard", "express", "bulk"], index=0)

    st.divider()

    # 매칭 엔진 선택
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📐 규칙 기반 매칭", use_container_width=True, type="primary"):
            try:
                order = Order(
                    order_id=order_id,
                    weight=weight,
                    volume=volume,
                    item_count=item_count,
                    fragile=fragile,
                    priority=priority,
                    destination_zone=destination_zone,
                    order_type=order_type
                )

                result = st.session_state.rule_matcher.find_best_facility(
                    order, st.session_state.facilities
                )

                if result:
                    facility, score = result

                    st.success("✅ 최적 설비를 찾았습니다!")

                    # 결과 표시
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("설비 이름", facility.name)
                    with col_b:
                        st.metric("설비 유형", facility.facility_type)
                    with col_c:
                        st.metric("매칭 점수", f"{score:.2%}")

                    # 상세 정보
                    with st.expander("📋 상세 정보"):
                        st.write(f"**설비 ID:** {facility.facility_id}")
                        st.write(f"**최대 용량:** {facility.max_weight}kg, {facility.max_volume}m³")
                        st.write(f"**속도 등급:** {facility.speed_rating}/4")
                        st.write(f"**깨지기 쉬운 물품 처리:** {'가능' if facility.can_handle_fragile else '불가능'}")
                        st.write(f"**지원 구역:** {', '.join(facility.supported_zones)}")

                    # 기록 추가
                    st.session_state.match_history.append({
                        "order_id": order_id,
                        "facility": facility.name,
                        "engine": "규칙 기반",
                        "score": f"{score:.2%}",
                        "time": time.strftime("%Y-%m-%d %H:%M:%S")
                    })

                else:
                    st.error("❌ 적합한 설비를 찾을 수 없습니다.")

            except ValueError as e:
                st.error(f"❌ 입력 오류: {e}")

    with col2:
        ml_disabled = not (st.session_state.ml_matcher and
                          st.session_state.ml_matcher._is_trained)

        if st.button("🤖 머신러닝 매칭", use_container_width=True,
                    disabled=ml_disabled, type="secondary"):
            try:
                order = Order(
                    order_id=order_id,
                    weight=weight,
                    volume=volume,
                    item_count=item_count,
                    fragile=fragile,
                    priority=priority,
                    destination_zone=destination_zone,
                    order_type=order_type
                )

                result = st.session_state.ml_matcher.predict(
                    order, st.session_state.facilities
                )

                if result:
                    facility, confidence = result

                    st.success("✅ 최적 설비를 예측했습니다!")

                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("설비 이름", facility.name)
                    with col_b:
                        st.metric("설비 유형", facility.facility_type)
                    with col_c:
                        st.metric("확신도", f"{confidence:.2%}")

                    with st.expander("📋 상세 정보"):
                        st.write(f"**설비 ID:** {facility.facility_id}")
                        st.write(f"**최대 용량:** {facility.max_weight}kg, {facility.max_volume}m³")
                        st.write(f"**속도 등급:** {facility.speed_rating}/4")

                    st.session_state.match_history.append({
                        "order_id": order_id,
                        "facility": facility.name,
                        "engine": "머신러닝",
                        "score": f"{confidence:.2%}",
                        "time": time.strftime("%Y-%m-%d %H:%M:%S")
                    })

                else:
                    st.error("❌ 적합한 설비를 찾을 수 없습니다.")

            except ValueError as e:
                st.error(f"❌ 입력 오류: {e}")

        if ml_disabled:
            st.info("💡 ML 엔진을 사용하려면 왼쪽 사이드바에서 먼저 학습하세요.")


# ----------------------------------------------------------------------------
# 탭 2: 설비 목록
# ----------------------------------------------------------------------------
with tab2:
    st.header("사용 가능한 설비 목록")

    # 필터
    filter_type = st.multiselect(
        "설비 유형 필터",
        options=list(set(f.facility_type for f in st.session_state.facilities)),
        default=list(set(f.facility_type for f in st.session_state.facilities))
    )

    filtered_facilities = [f for f in st.session_state.facilities
                          if f.facility_type in filter_type]

    for facility in filtered_facilities:
        with st.expander(f"🏭 {facility.name} ({facility.facility_type})"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"**ID:** {facility.facility_id}")
                st.write(f"**유형:** {facility.facility_type}")
                st.write(f"**상태:** {'🟢 사용 가능' if facility.available else '🔴 사용 중'}")

            with col2:
                st.write(f"**최대 무게:** {facility.max_weight} kg")
                st.write(f"**최대 부피:** {facility.max_volume} m³")
                st.write(f"**속도 등급:** {facility.speed_rating}/4")

            with col3:
                st.write(f"**깨지기 쉬운 물품:** {'✅' if facility.can_handle_fragile else '❌'}")
                st.write(f"**지원 구역:** {', '.join(facility.supported_zones)}")


# ----------------------------------------------------------------------------
# 탭 3: 매칭 기록
# ----------------------------------------------------------------------------
with tab3:
    st.header("매칭 기록")

    if st.session_state.match_history:
        # 데이터프레임으로 표시
        import pandas as pd
        df = pd.DataFrame(st.session_state.match_history)
        st.dataframe(df, use_container_width=True)

        if st.button("🗑️ 기록 초기화"):
            st.session_state.match_history = []
            st.rerun()
    else:
        st.info("아직 매칭 기록이 없습니다.")


# ----------------------------------------------------------------------------
# 탭 4: 도움말
# ----------------------------------------------------------------------------
with tab4:
    st.header("💡 사용 방법")

    st.markdown("""
    ### 시작하기

    1. **ML 모델 학습 (선택)**
       - 왼쪽 사이드바에서 "ML 모델 학습 시작" 클릭
       - 약 5-10초 소요

    2. **주문 정보 입력**
       - "📦 주문 매칭" 탭에서 주문 정보 입력
       - 모든 필드는 필수입니다

    3. **매칭 실행**
       - 규칙 기반 또는 머신러닝 매칭 버튼 클릭
       - 결과 확인

    ### 두 엔진의 차이

    | 특성 | 규칙 기반 | 머신러닝 |
    |------|-----------|----------|
    | 학습 | 불필요 | 필요 |
    | 투명성 | 높음 | 낮음 (블랙박스) |
    | 적응성 | 낮음 | 높음 |
    | 속도 | 매우 빠름 | 빠름 |

    ### .NET 개발자를 위한 팁

    - Streamlit = Blazor의 간소화 버전
    - Session State = HttpContext.Session
    - Tabs = Tab Control
    - Expander = Accordion

    ### 문의

    문제가 있으면 README.md를 확인하세요.
    """)


# ============================================================================
# 푸터
# ============================================================================

st.divider()
st.caption("🏭 물류센터 설비 AI 매칭 시스템 v1.0 | Made with Streamlit")
