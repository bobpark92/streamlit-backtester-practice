
import streamlit as st
import pandas as pd
import numpy as np

# --- 0. 페이지 기본 설정 ---
st.set_page_config(layout="wide", page_title="퀀트 백테스트 시뮬레이터")

# --- 1. 가상 데이터 생성 (실제 데이터 대신 사용) ---
@st.cache_data
def load_mock_data():
    data = {
        'Company': [
            'KOREA PETROCHEMICAL IND. CO LTD', 'KOREA-LINE CORPORATION', 
            'SINWON COMPANY LIMITED', 'LG HAUSYS LIMITED', 
            'ACE BED COMPANY LIMITED'
        ] * 10,
        'MktCap(USD)': np.random.randint(10, 1000, 50),
        'Industry': ['Plastics', 'Deep Sea Freight', 'Commercial Document Management', 'Construction Supplies & Fixtures', 'Home Furnishings'] * 10,
        'BasicScore': np.random.randint(0, 100, 50),
        'Turnaround': np.random.randint(0, 10, 50),
        'Debt/Value': np.random.randint(0, 10, 50),
        'Efficency/Growth': np.random.randint(0, 10, 50),
    }
    return pd.DataFrame(data)

df = load_mock_data()

# --- 2. 사이드바 (좌측 필터 및 조건 설정) ---
with st.sidebar:
    st.subheader("Filter & Factor Selection")
    
    # --- Absolute Section (상단 좌측) ---
    st.markdown("#### Absolute Filter")
    
    # Absolute Factor 1: Turnaround
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.selectbox("Factor", ["Turnaround", "PBR", "PER"], key="abs_factor_1")
    with col_a2:
        st.number_input("Value", min_value=0, max_value=10, value=5, key="abs_value_1")
    
    # Absolute Factor 2: (예시 추가)
    st.selectbox("Factor", ["PBR", "PER", "Turnaround"], key="abs_factor_2")
    st.selectbox("HL Type", ["H", "L", "="], key="abs_hl_type_2")
    st.number_input("Value", min_value=0, max_value=100, value=10, key="abs_value_2")

    st.markdown("---")

    # --- Relative Section (중앙 좌측) ---
    st.markdown("#### Relative Filter")
    st.selectbox("Factor", ["EPS/Price", "CF/Price"], key="rel_factor")
    
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        st.selectbox("Asc/Desc", ["Asc", "Desc"], key="rel_asc_desc")
    with col_r2:
        st.selectbox("DataType", ["Day", "Week", "Month"], key="rel_data_type")
    with col_r3:
        st.number_input("Top Pct", min_value=1, max_value=100, value=20, key="rel_top_pct")

    st.checkbox("Risk Value", key="rel_risk")
    
    st.markdown("---")

    # --- Screening Section (하단 좌측) ---
    st.markdown("#### Screening Setting")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.selectbox("Theme", ["ALL", "IT"], key="scr_theme")
        st.selectbox("Cond", ["ALL", "CondSelecter"], key="scr_cond")
    with col_s2:
        st.selectbox("Industry", ["ALL", "Plastics"], key="scr_industry")
        st.selectbox("Period", ["Annual", "Quarter"], key="scr_period")
    with col_s3:
        st.selectbox("Data", ["Index", "Indicator"], key="scr_data")
        st.checkbox("Adjusted", key="scr_adjusted")

    # 백테스트 버튼 (이미지 하단의 버튼)
    st.markdown("---")
    st.subheader("BACKTEST EXECUTION")
    
    # 이미지처럼 하단에 위치한 옵션들
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.selectbox("Start", ["2010-01-01"], key="back_start")
    with col_b2:
        st.selectbox("End", ["2024-12-31"], key="back_end")

    st.selectbox("Rebalance Cycle", ["No rebal.", "Weekly", "Monthly"], key="back_rebal")
    st.selectbox("Weight Method", ["Equal", "Mkt Cap"], key="back_weight")
    
    # 백테스트 실행 버튼
    if st.button("백테스트 실행 🚀", use_container_width=True):
        st.session_state['backtest_executed'] = True
        st.success("백테스트 전략 성과 평가 완료! (가상)")


# --- 3. 메인 콘텐츠 (우측 테이블 및 결과) ---
st.header("📊 Backtest Result & Stock Universe")

# 탭 구성 (Monitoring, Backtest Performance)
tab1, tab2 = st.tabs(["Monitoring (Stock Universe)", "Backtest Performance"])

with tab1:
    st.subheader("선택된 종목 유니버스")
    st.markdown("현재 필터 및 조건에 의해 선택된 종목 목록입니다.")
    
    # 데이터프레임 표시 (이미지의 테이블 부분)
    # Streamlit은 st.data_editor 또는 st.dataframe을 사용하며, 사용자가 스크롤, 정렬, 검색 가능
    st.dataframe(
        df,
        use_container_width=True,
        height=550 # 이미지와 유사하게 높이 설정
    )

with tab2:
    st.subheader("전략 성과 평가")
    if st.session_state.get('backtest_executed'):
        # 실제 백테스트 결과 지표 및 차트 표시 영역
        st.metric(label="CAGR (연평균 복합 성장률)", value="18.5%", delta="10.2%", delta_color="normal")
        st.metric(label="MDD (최대 낙폭)", value="-25.1%", delta_color="inverse")
        st.line_chart(np.cumsum(np.random.randn(100, 1) / 10 + 0.01), use_container_width=True)
    else:
        st.info("좌측 사이드바에서 조건을 설정하고 '백테스트 실행' 버튼을 눌러주세요.")