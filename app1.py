
import streamlit as st
import pandas as pd

st.title("나의 수업시간표")

# 과목별 정보
courses = [
    {
        "과목명": "화학 2",
        "학점": 3,
        "요일": ["월요일", "수요일"],
        "시간": "09:00~10:30",
    },
    {
        "과목명": "수학 2",
        "학점": 3,
        "요일": ["월요일", "수요일"],
        "시간": "10:30~12:00",
    },
    {
        "과목명": "컴퓨팅 실습",
        "학점": 3,
        "요일": ["화요일", "목요일"],
        "시간": "13:00~14:30",
    },
    {
        "과목명": "대학영어",
        "학점": 3,
        "요일": ["화요일", "목요일"],
        "시간": "14:30~16:00",
    },
]

# 시간표의 행과 열
times = ["09:00~10:30", "10:30~12:00", "13:00~14:30", "14:30~16:00"]
days = ["월요일", "화요일", "수요일", "목요일", "금요일"]

# 모든 칸을 "-"로 채운 시간표 생성
timetable = pd.DataFrame("-", index=times, columns=days)
timetable.index.name = "시간"

# 수업이 있는 칸에 과목명 입력
for course in courses:
    for day in course["요일"]:
        timetable.loc[course["시간"], day] = course["과목명"]

# 정적 시간표 출력
st.header("주간 시간표")
st.table(timetable)

# 수업 정보를 JSON 형식으로 출력
st.header("수업 정보")
st.json(courses)

# 수강 과목 수와 총학점 계산
st.header("이번 학기 요약")

course_count = len(courses)
total_credits = sum(course["학점"] for course in courses)

st.metric(label="수강 과목 수", value=f"{course_count}개")
st.metric(label="총학점", value=f"{total_credits}학점")
