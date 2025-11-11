import streamlit as st
import pandas as pd
import numpy as np

# --- UI 커스터마이징 및 입력 요소 ---
st.title('💰 간단한 투자 수익률 계산기')
st.markdown('### Streamlit UI 및 Python 연동 연습')

# 입력 필드 1: 클릭/슬라이드 가능한 입력 칸
initial_investment = st.slider(
    '1. 초기 투자금 (만원)',
    min_value=100,
    max_value=10000,
    value=1000,
    step=100
)

# 입력 필드 2: 텍스트 입력 칸
annual_return = st.number_input(
    '2. 연간 예상 수익률 (%)',
    min_value=0.0,
    max_value=100.0,
    value=10.0,
    step=0.1
)

# 입력 필드 3: 전략 선택 (클릭 요소)
strategy = st.selectbox(
    '3. 투자 전략 (백테스트 유니버스/전략의 Placeholder)',
    ['가치 투자', '성장 투자', '모멘텀']
)

st.write(f"선택된 전략: **{strategy}**")

# --- 데이터 계산 및 결과 도출 (백테스트 코어 로직 Placeholder) ---

# 수익률 계산 함수
def calculate_growth(initial, rate, years=5):
    rate_decimal = rate / 100
    # 5년간의 연도별 자산 변화 계산
    data = {'Year': list(range(1, years + 1))}
    data['Value'] = [initial * ((1 + rate_decimal) ** year) for year in range(1, years + 1)]
    return pd.DataFrame(data)

# '계산' 버튼 (클릭 시 계산 진행)
if st.button('결과 계산 및 시각화'):
    st.success('계산이 완료되었습니다! 짠~!')
    
    # 계산 실행
    results_df = calculate_growth(initial_investment, annual_return)
    
    # 결과 표시
    final_value = results_df['Value'].iloc[-1]
    st.metric(label="최종 예상 투자금 (만원)", value=f"{final_value:,.0f}")
    
    st.subheader('📈 5년 간의 투자금 성장 시뮬레이션')
    
    # 시각화 (Streamlit에서 제공하는 간단한 차트)
    st.line_chart(results_df, x='Year', y='Value')
    
    st.caption('이것이 바로 클릭으로 커스터마이즈하고 Python과 연동되는 UI입니다.')