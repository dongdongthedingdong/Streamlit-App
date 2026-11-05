
import streamlit as st


# 페이지 제목
st.title("나의 자기소개서")

# 자기소개
st.header("자기소개")
st.write("안녕하세요! 서울대학교 화학부에서 공부하고 있는 이동재입니다.")
st.write("화학과 프로그래밍을 함께 공부하고 있습니다.")

# 좋아하는 것
st.header("좋아하는 것")
st.write("- 화학 원리 공부하기")
st.write("- 운동하기")

# 앞으로의 목표
st.header("앞으로의 목표")
st.write(".....")

# 링크
st.header("관련 링크")
st.markdown("[서울대학교 홈페이지](https://www.snu.ac.kr)")
st.markdown("[Streamlit 공식 문서](https://docs.streamlit.io)")

# 좋아하는 코드 예시
st.header("좋아하는 코드")
st.code(
    '''for i in range(1, 6):
    print(f"오늘의 공부 목표 {i}번 달성!")''',
    language="python",
)
st.caption("반복문을 사용해 공부 목표 달성 메시지를 다섯 번 출력하는 코드입니다.")

# 수식
st.header("관심 있는 수식")
st.latex(r"E = h\nu")
