# 여기에 작성한다. (streamlit run app.py 로 실행해서 확인한다)
import os
import re
import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd

API_KEY = "9e118a8d110b82f4525d2e7b5292e748cfa5e0e96ae29f0d9aa8faa5d5ea922c"
API_URL = "https://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev"

st.title("아파트 매매 실거래가 조회")
region_code = st.text_input("지역코드", "11110")
contract_month = st.text_input("계약년월", "202005")

if st.button("조회하기"):
    if not re.fullmatch(r"\d{5}", region_code):
        st.error("지역코드는 숫자 5자리여야 합니다.")
    elif not re.fullmatch(r"\d{6}", contract_month) or not 1 <= int(contract_month[4:]) <= 12:
        st.error("계약년월은 YYYYMM 형식이어야 합니다. 예: 202005")
    elif API_KEY == "본인의_공공데이터_API_인증키":
        st.error("공공데이터포털 인증키를 API_KEY에 입력하거나 환경변수에 설정하세요.")
    else:
        params = {"serviceKey": API_KEY, "LAWD_CD": region_code, "DEAL_YMD": contract_month, "numOfRows": 1000, "pageNo": 1}
        try:
            with st.spinner("데이터 조회 중..."):
                response = requests.get(API_URL, params=params, timeout=20)
                response.raise_for_status()
                root = ET.fromstring(response.content)
                result_code = root.findtext(".//resultCode")
                if result_code and result_code not in ("00", "000"):
                    raise ValueError(root.findtext(".//resultMsg", "API 오류"))
                total = int(root.findtext(".//totalCount", "0"))
                records = []
                for item in root.findall(".//item"):
                    records.append({child.tag: (child.text or "").strip() for child in item})
                # 1000건을 초과하는 경우 나머지 페이지도 조회
                for page in range(2, (total - 1) // 1000 + 2):
                    params["pageNo"] = page
                    more = requests.get(API_URL, params=params, timeout=20)
                    more.raise_for_status()
                    more_root = ET.fromstring(more.content)
                    for item in more_root.findall(".//item"):
                        records.append({child.tag: (child.text or "").strip() for child in item})
            df = pd.DataFrame(records)
            st.write(f"조회된 거래 건수: **{len(df):,}건**")
            if df.empty:
                st.warning("해당 조건의 거래 내역이 없습니다.")
            else:
                st.dataframe(df, use_container_width=True)
        except (requests.RequestException, ET.ParseError, ValueError) as exc:
            st.error(f"조회 실패: {exc}")
