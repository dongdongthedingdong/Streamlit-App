# 여기에 작성한다. (streamlit run app.py 로 실행해서 확인한다)
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_KEY2 = "9e118a8d110b82f4525d2e7b5292e748cfa5e0e96ae29f0d9aa8faa5d5ea922c"
year_to_uddi = {
    2020: "uddi:400b5a86-8396-4e4e-9e0f-d7f92d57acfe",
    2022: "uddi:34f1f0b1-1289-49db-be1b-a4566880bb97",
    2024: "uddi:dce2549b-efb3-4920-b611-c9548590b6f0",
}

st.title("교통사고 통계 조회")
year = st.selectbox("연도 선택", list(year_to_uddi.keys()))

if st.button("조회하기"):
    if API_KEY2.startswith("여기에_"):
        st.warning("API_KEY2에 본인의 인증키를 입력하세요.")
    else:
        url = f"https://api.odcloud.kr/api/15070282/v1/{year_to_uddi[year]}"
        params = {"page": 1, "perPage": 1000, "serviceKey": API_KEY2, "returnType": "JSON"}
        try:
            response = requests.get(url, params=params, timeout=20)
            response.raise_for_status()
            result = response.json()
            df_accident = pd.DataFrame(result.get("data", []))
            st.write(f"{year}년 조회 건수: {len(df_accident)}건")
            if df_accident.empty:
                st.warning("데이터가 없습니다.")
            else:
                st.dataframe(df_accident, use_container_width=True)
                # 강의에서 안내한 대로 표의 실제 컬럼명을 먼저 확인한다.
                # 데이터셋 버전별로 이름이 다를 수 있어 사용자가 직접 선택하도록 구성한다.
                columns = df_accident.columns.tolist()
                default_x = next((i for i, c in enumerate(columns) if "사고유형" in c), 0)
                default_y = next((i for i, c in enumerate(columns) if "발생건수" in c), min(1, len(columns)-1))
                x_col = st.selectbox("사고유형 컬럼", columns, index=default_x)
                y_col = st.selectbox("발생건수 컬럼", columns, index=default_y)
                graph_data = df_accident.copy()
                graph_data[y_col] = pd.to_numeric(graph_data[y_col].astype(str).str.replace(",", ""), errors="coerce")
                graph_data = graph_data.dropna(subset=[y_col])
                if graph_data.empty:
                    st.warning("선택한 발생건수 컬럼을 숫자로 변환할 수 없습니다.")
                else:
                    grouped = graph_data.groupby(x_col, as_index=False)[y_col].sum()
                    fig = px.bar(grouped, x=x_col, y=y_col, color=x_col, title=f"{year}년 사고유형별 발생건수")
                    st.plotly_chart(fig, use_container_width=True)
        except (requests.RequestException, ValueError) as e:
            st.error(f"조회 실패: {e}")
            if 'response' in locals():
                st.code(response.text[:500])
