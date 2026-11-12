
import streamlit as st
import sklearn

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

def cars_predict(df):
    st.header("자동차 연비 예측")
    st.write("선형회귀(Linear Regression) 모델을 활용하여 자동차의 연비(mpg)를 예측합니다.")

    # 입력 변수(X)와 목표 변수(y) 설정
    X = df[["cylinders", "cubicinches", "hp", "weightlbs", "time-to-60"]]
    y = df["mpg"]

    # 학습 데이터와 테스트 데이터 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 모델 학습
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 예측 성능 표시
    y_pred = model.predict(X_test)
    score = r2_score(y_test, y_pred)
    st.write(f"모델 성능 (R2): **{score:.3f}**")

    # 사용자 입력
    st.subheader("자동차 정보 입력")
    cylinders = st.slider("실린더 수 (cylinders)", 3, 12, 6)
    cubicinches = st.slider("배기량 (cubicinches)", 60, 500, 200)
    hp = st.slider("마력 (horsepower)", 50, 400, 150)
    weightlbs = st.slider("무게 (weightlbs)", 1500, 6000, 3000)
    time_to_60 = st.slider("시속 60마일 도달 시간 (초)", 4.0, 20.0, 10.0)

    # 입력값으로 예측 수행
    input_data = pd.DataFrame({
        "cylinders": [cylinders],
        "cubicinches": [cubicinches],
        "hp": [hp],
        "weightlbs": [weightlbs],
        "time-to-60": [time_to_60]
    })

    mpg_pred = model.predict(input_data)[0]
    st.success(f"예상 연비: **{mpg_pred:.2f} mpg**")
