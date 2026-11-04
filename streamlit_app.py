import streamlit as st
import pandas as pd
import numpy as np

# 앱 제목
st.title("나의 첫 번째 Streamlit 앱")

# 사이드바
st.sidebar.title("설정")

# 차트 유형 선택
chart_type = st.sidebar.radio(
    "차트 유형",
    ["꺾은선 그래프", "막대 그래프", "면적 그래프"]
)

# 데이터 개수 선택
n = st.sidebar.slider(
    "데이터 개수",
    min_value=10,
    max_value=100,
    value=30
)

# 수정한 부분: 앱 설명 문구
st.write(
    "슬라이더로 데이터 개수를 조절하고 차트 유형을 선택해 "
    "무작위로 생성한 샘플 데이터를 시각화해 보세요."
)

# n행 3열의 무작위 샘플 데이터 생성
data = pd.DataFrame(
    np.random.randn(n, 3),
    columns=["A", "B", "C"]
)

# 선택한 유형에 맞는 차트 표시
if chart_type == "꺾은선 그래프":
    st.line_chart(data)
elif chart_type == "막대 그래프":
    st.bar_chart(data)
else:
    st.area_chart(data)

# 데이터의 처음 5행 표시
st.dataframe(data.head(5))
