
# 사용 API: Open-Meteo Weather Forecast API
# 출처: https://open-meteo.com/en/docs

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(
    page_title="전국 날씨 예보 대시보드",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ 전국 날씨 예보 대시보드")
st.write("도시와 예보 기간, 날씨 항목을 선택하면 시간별 날씨 예보를 보여줍니다.")

# 도시별 위도와 경도
cities = {
    "서울": (37.5665, 126.9780),
    "부산": (35.1796, 129.0756),
    "대구": (35.8714, 128.6014),
    "인천": (37.4563, 126.7052),
    "광주": (35.1595, 126.8526),
    "대전": (36.3504, 127.3845),
    "제주": (33.4996, 126.5312),
}

# 날씨 항목: (API 변수명, 단위)
weather_items = {
    "기온": ("temperature_2m", "°C"),
    "상대습도": ("relative_humidity_2m", "%"),
    "강수량": ("precipitation", "mm"),
    "풍속": ("wind_speed_10m", "km/h"),
}

# 1. 사용자 조건 입력
st.subheader("1. 조회 조건 입력")

col1, col2, col3 = st.columns(3)

with col1:
    city = st.selectbox("도시 선택", list(cities.keys()))

with col2:
    days = st.slider("예보 기간 (일)", 1, 7, 3)

with col3:
    item = st.selectbox("날씨 항목", list(weather_items.keys()))

lat, lon = cities[city]
variable, unit = weather_items[item]


# 2. API 호출 함수
@st.cache_data(ttl=600)
def get_weather(latitude, longitude, forecast_days, hourly_variable):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": hourly_variable,
        "forecast_days": forecast_days,
        "timezone": "Asia/Seoul",
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()

    if "hourly" not in data or hourly_variable not in data["hourly"]:
        raise ValueError("날씨 데이터를 찾을 수 없습니다.")

    return data["hourly"]


# 3. API 데이터 처리 및 결과 출력
try:
    with st.spinner("날씨 데이터를 불러오는 중입니다..."):
        hourly = get_weather(lat, lon, days, variable)

    df = pd.DataFrame({
        "시간": pd.to_datetime(hourly["time"]),
        item: hourly[variable],
    })

    df[item] = pd.to_numeric(df[item], errors="coerce")

    st.subheader("2. 조회 결과 요약")

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric("조회 도시", city)
    metric2.metric("예보 기간", f"{days}일")
    metric3.metric(
        f"평균 {item}",
        f"{df[item].mean():.1f} {unit}"
    )

    # 4. 데이터 표 출력
    st.subheader("3. 시간별 날씨 데이터")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # 5. 그래프 시각화
    st.subheader("4. 날씨 변화 그래프")

    if item == "강수량":
        fig = px.bar(
            df,
            x="시간",
            y=item,
            title=f"{city}의 시간별 {item}"
        )
    else:
        fig = px.line(
            df,
            x="시간",
            y=item,
            markers=True,
            title=f"{city}의 시간별 {item}"
        )

    fig.update_layout(
        xaxis_title="시간",
        yaxis_title=f"{item} ({unit})"
    )

    st.plotly_chart(fig, use_container_width=True)

    # API 출처
    st.caption("데이터 제공: Open-Meteo Weather Forecast API")
    st.link_button(
        "API 공식 문서",
        "https://open-meteo.com/en/docs"
    )

except (requests.RequestException, ValueError, KeyError) as error:
    st.error(f"날씨 데이터를 불러오지 못했습니다: {error}")
    st.info("인터넷 연결을 확인한 뒤 다시 시도해주세요.")
