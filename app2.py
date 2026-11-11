
import streamlit as st
import pandas as pd

st.set_page_config(page_title="화학 반응 속도 대시보드", page_icon="🧪", layout="wide")

st.title("🧪 온도에 따른 화학 반응 속도 분석")
st.caption("10강 실습 과제 | 아래 수치는 대시보드 연습을 위한 가상 데이터입니다.")
st.markdown("온도가 높아질수록 반응 속도 상수가 어떻게 달라지는지 비교합니다. 실제 실험 결과가 아닌 **예시 데이터**입니다.")

# 학습용 가상 데이터: 실제 실험 측정값이 아님
measurements = pd.DataFrame({
    "온도(°C)": [10, 20, 30, 40, 50, 60],
    "반응 속도 상수(1/min)": [0.012, 0.019, 0.031, 0.050, 0.081, 0.132],
})

st.sidebar.header("분석 설정")
selected_temp = st.sidebar.slider("비교할 온도(°C)", 10, 60, 30, step=10)
chart_kind = st.sidebar.radio("차트 종류", ["꺾은선 그래프", "막대그래프"])
show_all = st.sidebar.checkbox("모든 온도 표시", value=True)

selected = measurements.loc[measurements["온도(°C)"] == selected_temp].iloc[0]
base_rate = float(measurements.loc[measurements["온도(°C)"] == 10, "반응 속도 상수(1/min)"].iloc[0])
selected_rate = float(selected["반응 속도 상수(1/min)"])

c1, c2, c3 = st.columns(3)
c1.metric("선택한 온도", f"{selected_temp} °C")
c2.metric("선택 온도의 속도 상수", f"{selected_rate:.3f} 1/min")
c3.metric("10°C 대비 배율", f"{selected_rate / base_rate:.2f}배")

st.header("온도별 데이터")
if show_all:
    shown = measurements.copy()
else:
    shown = measurements[measurements["온도(°C)"] <= selected_temp].copy()
st.dataframe(shown, use_container_width=True, hide_index=True)

st.header("반응 속도 상수 시각화")
chart_data = shown.set_index("온도(°C)")[["반응 속도 상수(1/min)"]]
if chart_kind == "꺾은선 그래프":
    st.line_chart(chart_data)
else:
    st.bar_chart(chart_data)

st.header("선택한 온도 해석")
st.write(f"{selected_temp}°C에서 예시 반응 속도 상수는 {selected_rate:.3f} 1/min이며, "
         f"10°C의 값보다 약 {selected_rate / base_rate:.2f}배 큽니다.")
st.info("슬라이더를 움직이면 지표와 설명이 변경됩니다. '모든 온도 표시'를 해제하면 그래프와 표도 선택 온도까지 표시됩니다.")
