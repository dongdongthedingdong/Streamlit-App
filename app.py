# 여기에 작성한다. (streamlit run app.py 로 실행해서 확인한다)
import os
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

if API_KEY2 == "9e118a8d110b82f4525d2e7b5292e748cfa5e0e96ae29f0d9aa8faa5d5ea922c":
    st.warning("API_KEY2에 인증키를 입력하거나 환경변수 DATA_GO_KR_API_KEY2를 설정하세요.")
else:
    url = f"https://api.odcloud.kr/api/15070282/v1/uddi:dce2549b-efb3-4920-b611-c9548590b6f0/{year_to_uddi[year]}"
    try:
        response = requests.get(url, params={"serviceKey": API_KEY2, "returnType": "JSON", "page": 1, "perPage": 1000}, timeout=20)
        response.raise_for_status()
        result = response.json()
        if "data" not in result:
            raise ValueError(f"응답에 data가 없습니다: {str(result)[:250]}")
        df = pd.DataFrame(result["data"])
        st.write(f"{year}년 데이터: **{len(df)}행** (첫 1000행 이내)")
        st.dataframe(df, use_container_width=True)
        if df.empty:
            st.warning("조회된 데이터가 없습니다.")
        else:
            st.caption("반환된 데이터의 실제 컬럼명을 선택하세요.")
            columns = list(df.columns)
            label_candidates = [c for c in columns if any(t in c for t in ("사고유형", "사고 유형", "유형"))]
            count_candidates = [c for c in columns if any(t in c for t in ("발생건수", "사고건수", "발생건", "건수"))]
            type_col = st.selectbox("사고유형 컬럼", columns, index=columns.index(label_candidates[0]) if label_candidates else 0)
            count_col = st.selectbox("발생건수 컬럼", columns, index=columns.index(count_candidates[0]) if count_candidates else min(1, len(columns)-1))
            chart_df = df[[type_col, count_col]].copy()
            chart_df[count_col] = pd.to_numeric(chart_df[count_col].astype(str).str.replace(",", "", regex=False), errors="coerce")
            chart_df = chart_df.dropna(subset=[count_col])
            if chart_df.empty:
                st.warning("선택한 발생건수 컬럼에서 숫자를 찾을 수 없습니다. 컬럼을 다시 선택하세요.")
            else:
                chart_df = chart_df.groupby(type_col, as_index=False)[count_col].sum()
                fig = px.bar(chart_df, x=type_col, y=count_col, title=f"{year}년 사고유형별 발생건수")
                st.plotly_chart(fig, use_container_width=True)
    except (requests.RequestException, ValueError) as exc:
        st.error(f"API 조회 또는 데이터 처리 중 오류: {exc}")
