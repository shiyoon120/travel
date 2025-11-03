# 파일명: safetrip_v10_tabbed_final_rate_separated_modified.py
import streamlit as st
import pandas as pd
import datetime
import pydeck as pdk

# --- 다국어 문자열 사전 (V10 기반) ---
translations = {
    "ko": {
        "title": "✈️ SafeTrip",
        "caption": "여행 일정표 · 지도 · 최신 이슈 · 긴급전화 링크 · 확대 국가/도시 정보 포함",
        "lang_select": "언어 선택",
        "travel_schedule": "📆 여행 일정 입력",
        "departure": "출국일",
        "return": "귀국일",
        "duration_prefix": "➡️ 여행 기간: ",
        "days_suffix": "일",
        "country_select": "🌍 국가 선택",
        "city_select": "🏙️ 도시 선택",
        "search_report": "🔍 안전 보고서 보기",
        "emergency_section": "🚨 응급 상황 대처",
        "emergency_select": "상황 선택", # 사용하지 않지만, 기존 코드를 위해 유지
        "emergency_advice_prefix": "🔹 대처 요령: ", # 사용하지 않지만, 기존 코드를 위해 유지
        "call_emergency": "📞 긴급전화 걸기",
        "risk_info": "⚠️ 주요 위험 및 유의사항",
        "tips_info": "✅ 대처 요령",
        "recent_issues": "📰 최근 위험 이슈",
        "checklist_section": "🧳 여행 전 필수 점검",
        "record_section": "📜 나의 여행 기록",
        "complete_success": "🎉 모든 준비 완료! 안전한 여행 되세요.",
        "search_link_btn": "구글에서 더 알아보기", # 새로운 검색 버튼 텍스트
        "exchange_rate": "💱 환율 정보",
        "map_section": "🗺️ 도시 지도",
    },
    "en": {
        "title": "✈️ SafeTrip Full Version (v10) - Tab & Search Integrated",
        "caption": "Travel schedule · Map · Latest issues · Emergency call link · Expanded countries/cities info",
        "lang_select": "Select Language",
        "travel_schedule": "📆 Enter Travel Schedule",
        "departure": "Departure Date",
        "return": "Return Date",
        "duration_prefix": "➡️ Trip Duration: ",
        "days_suffix": " days",
        "country_select": "🌍 Select Country",
        "city_select": "🏙️ Select City",
        "search_report": "🔍 View Safety Report",
        "emergency_section": "🚨 Emergency Response",
        "emergency_select": "Select Situation", # 사용하지 않지만, 기존 코드를 위해 유지
        "emergency_advice_prefix": "🔹 Advice: ", # 사용하지 않지만, 기존 코드를 위해 유지
        "call_emergency": "📞 Make Emergency Call",
        "risk_info": "⚠️ Key Risks & Notices",
        "tips_info": "✅ Response Tips",
        "recent_issues": "📰 Recent Issues",
        "checklist_section": "🧳 Pre‑Travel Checklist",
        "record_section": "📜 My Travel Records",
        "complete_success": "🎉 All set! Have a safe trip.",
        "search_link_btn": "Search on Google",
        "exchange_rate": "💱 Exchange Rate Info",
        "map_section": "🗺️ City Map",
    }
}

# 언어 선택
lang_option = st.selectbox(translations["ko"]["lang_select"], ("한국어", "English"), key="lang_choice")
lang = "ko" if lang_option == "한국어" else "en"
_ = translations[lang] # 선택된 언어의 딕셔너리를 '_' 변수에 할당하여 모든 UI 텍스트에 적용

st.set_page_config(page_title=_["title"], page_icon="✈️", layout="wide")

st.title(_["title"])
st.caption(_["caption"])

st.markdown("---")

# --- 기본 데이터 확장 (V10 코드의 데이터 그대로 사용) ---
safety_data = {
    "한국": {
        "도시": ["서울", "부산", "제주", "인천", "대구", "광주", "울산"],
        "위험 정보": ["대체로 안전", "교통 혼잡 시간 주의"],
        "대처 요령": ["대중교통 이용 권장"],
        "현지 연락처": {"긴급 전화": "112 / 119"},
        "추가 이슈": ["최근 소매치기 증가 보고됨"]
    },
    "일본": {
        "도시": ["도쿄", "오사카", "후쿠오카", "삿포로", "교토", "요코하마", "나고야"],
        "위험 정보": ["지진 가능성", "유흥가 호객행위 주의"],
        "대처 요령": ["지진 발생 시 DROP, COVER, HOLD ON"],
        "현지 연락처": {"긴급 전화": "110 / 119"},
        "추가 이슈": ["외국인 대상 유흥가 사기 사례 증가"]
    },
    "태국": {
        "도시": ["방콕", "푸켓", "치앙마이", "파타야", "끄라비", "코사무이"],
        "위험 정보": ["관광지 소매치기 주의", "툭툭 이용 시 가격 흥정 필수"],
        "대처 요령": ["공인된 택시 앱 사용"],
        "현지 연락처": {"긴급 전화": "191 / 1669"},
        "추가 이슈": ["밤늦은 루프탑 바에서 음료 음용 주의"]
    },
    "캄보디아": {
        "도시": ["프놈펜", "시엠립", "시아누크빌", "앙코르", "바탐방"],
        "위험 정보": ["절도 발생 증가", "모기 매개 질병(뎅기열) 주의", "외국인 납치·사기 사례 보고됨"],
        "대처 요령": ["야간 외출 시 택시 이용 권장", "현금 보관 주의"],
        "현지 연락처": {"긴급 전화": "117 / 119"},
        "추가 이슈": ["한국인 대상 유사 납치·사기 경고"]
    },
    "미국": {
        "도시": ["뉴욕", "LA", "샌프란시스코", "하와이", "시카고"],
        "위험 정보": ["도심 일부 지역 범죄율 높음", "법규: 총기 사고 주의"],
        "대처 요령": ["야간에는 인적이 드문 곳 피하기"],
        "현지 연락처": {"긴급 전화": "911"},
        "추가 이슈": ["특정 도시 관광객 대상 범죄 증가 보고됨"]
    },
    "영국": {
        "도시": ["런던", "맨체스터", "에든버러", "리버풀"],
        "위험 정보": ["기차·지하철 지연 가능성", "도심 소매치기 주의"],
        "대처 요령": ["혼잡 시간대 대비", "귀중품 주의"],
        "현지 연락처": {"긴급 전화": "999"},
        "추가 이슈": ["런던 중심가에서 관광객 대상 사기 사례 증가"]
    },
    "호주": {
        "도시": ["시드니", "멜버른", "브리즈번", "퍼스"],
        "위험 정보": ["산불 및 폭우 주의", "환경: 독성 생물 주의"],
        "대처 요령": ["야생동물과의 접촉 자제"],
        "현지 연락처": {"긴급 전화": "000"},
        "추가 이슈": ["해변 이용 시 파도·조류 주의 경고"]
    },
    "베트남": {
        "도시": ["하노이", "호찌민", "다낭", "나트랑"],
        "위험 정보": ["오토바이 교통량 매우 많음", "핸드폰 날치기 주의"],
        "대처 요령": ["길거리 걸을 때 소지품 보호 철저"],
        "현지 연락처": {"긴급 전화": "113 / 115"},
        "추가 이슈": ["관광지 밤거리 안전 주의"]
    },
    "인도네시아": {
        "도시": ["발리", "자카르타", "롬복", "욕야카르타"],
        "위험 정보": ["자연재해: 화산 활동 및 쓰나미 가능성", "교통: 무면허 운전 위험"],
        "대처 요령": ["현지 택시 대신 검증된 교통수단 이용"],
        "현지 연락처": {"긴급 전화": "110 / 118"},
        "추가 이슈": ["외국인 대상 교통사고 증가 보고됨"]
    },
}

# --- 고정 환율 데이터 (V10 코드의 데이터 그대로 사용) ---
exchange_rates = {
    "한국": ("KRW", 1, "1원 = 1원"),
    "일본": ("JPY", 0.106, "1원 ≈ 0.106엔"),
    "태국": ("THB", 0.0228, "1원 ≈ 0.0228바트"),
    "캄보디아": ("KHR", 2.83, "1원 ≈ 2.83리엘"),
    "미국": ("USD", 1/1420, "1원 ≈ 0.00070달러"),
    "영국": ("GBP", 1/1800, "1원 ≈ 0.00056파운드"),
    "호주": ("AUD", 1/930, "1원 ≈ 0.00108호주달러"),
    "베트남": ("VND", 18.86, "1원 ≈ 18.86동"),
    "인도네시아": ("IDR", 11.56, "1원 ≈ 11.56루피아"),
}

# 지도 좌표 (V10 코드의 데이터 그대로 사용)
coords = {
    "서울": (37.5665, 126.9780), "부산": (35.1796, 129.0756), "제주": (33.4996, 126.5312),
    "인천": (37.4563, 126.7052), "대구": (35.8714, 128.6014), "광주": (35.1595, 126.8526),
    "울산": (35.5384, 129.3160), "도쿄": (35.6895, 139.6917), "오사카": (34.6937, 135.5023),
    "후쿠오카": (33.5904, 130.4017), "삿포로": (43.0618, 141.3545), "교토": (35.0116, 135.7681),
    "요코하마": (35.4437, 139.6380), "나고야": (35.1815, 136.9066), "방콕": (13.7563, 100.5018),
    "푸켓": (7.9519, 98.3381), "치앙마이": (18.7883, 98.9853), "파타야": (12.9236, 100.8825),
    "끄라비": (8.0350, 98.9063), "코사무이": (9.5120, 100.0134), "프놈펜": (11.5564, 104.9282),
    "시엠립": (13.3633, 103.8618), "시아누크빌": (10.6260, 103.5130), "앙코르": (13.4125, 103.8667),
    "바탐방": (13.1000, 103.2000), "뉴욕": (40.7128, -74.0060), "LA": (34.0522, -118.2437),
    "샌프란시스코": (37.7749, -122.4194), "하와이": (21.3069, -157.8583), "시카고": (41.8781, -87.6298),
    "런던": (51.5074, -0.1278), "맨체스터": (53.4808, -2.2426), "에든버러": (55.9533, -3.1883),
    "리버풀": (53.4084, -2.9916), "시드니": (33.8688, 151.2093), "멜버른": (37.8136, 144.9631),
    "브리즈번": (-27.4698, 153.0251), "퍼스": (-31.9505, 115.8605), "하노이": (21.0278, 105.8342),
    "호찌민": (10.8231, 106.6297), "다낭": (16.0544, 108.2022), "나트랑": (12.2388, 109.1967),
    "발리": (-8.3405, 115.0920), "자카르타": (-6.2088, 106.8456), "롬복": (-8.4095, 116.1572),
    "욕야카르타": (-7.7956, 110.3695),
}

# --- Google 검색 링크 생성 함수 ---
def create_google_search_link(query):
    base_url = "https://www.google.com/search?q="
    return base_url + query.replace(" ", "+")

# --- 여행 일정표 입력 기능 (V10 코드 그대로) ---
st.subheader(_["travel_schedule"])
departure = st.date_input(_["departure"], datetime.date.today())
return_date = st.date_input(_["return"], datetime.date.today() + datetime.timedelta(days=7))

if return_date < departure:
    st.error("⚠️ " + _["return"] + "이/가 " + _["departure"] + "보다 앞설 수 없습니다.")
else:
    duration = (return_date - departure).days
    st.write(_["duration_prefix"] + f"{duration}" + _["days_suffix"])

st.markdown("---")

# --- 세션 상태 초기화 및 관리 (V10 기반) ---
# V10의 체크리스트 항목을 여기에 정의
v10_checklist_items = ["여권/비자 확인", "보험 가입", "비상연락망 저장", "신용카드 분실 신고처 메모"]

if "travel_history" not in st.session_state:
    st.session_state.travel_history = []
if "checklist" not in st.session_state:
    st.session_state.checklist = {} # 국가별 체크리스트 상태 저장
if "report_on" not in st.session_state:
    st.session_state.report_on = False
if "selected_country" not in st.session_state:
    st.session_state.selected_country = list(safety_data.keys())[0]
if "selected_city" not in st.session_state:
    st.session_state.selected_city = safety_data[st.session_state.selected_country]["도시"][0]


# --- 국가/도시 선택 ---
col_country, col_city = st.columns(2)
with col_country:
    country = st.selectbox(_["country_select"], list(safety_data.keys()), key="country_select_box")
with col_city:
    city = st.selectbox(_["city_select"], safety_data[country]["도시"], key="city_select_box")

if st.button(_["search_report"], type="primary"):
    st.session_state.travel_history.append({
        "국가": country,
        "도시": city,
        "출국일": departure,
        "귀국일": return_date
    })
    # V10 체크리스트 항목으로 초기화
    if country not in st.session_state.checklist:
        st.session_state.checklist[country] = {
            item: False for item in v10_checklist_items
        }
    st.session_state.selected_country = country
    st.session_state.selected_city = city
    st.session_state.report_on = True
    st.rerun()

# --- 보고서 표시 (st.tabs 사용) ---
if st.session_state.report_on:
    sel_country = st.session_state.selected_country
    sel_city = st.session_state.selected_city
    info = safety_data.get(sel_country, {})

    if not info:
        st.error(f"❌ **{sel_country}**에 대한 상세 정보가 없습니다. 목록에서 다른 국가를 선택해 주세요.")
        st.stop() # 정보가 없으면 여기서 중단

    st.header(f"📋 {sel_country} – {sel_city}")
    
    # 탭 구성 (V8의 탭 구성을 차용하되, V10의 내용으로 채움)
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        _["risk_info"], 
        _["tips_info"], 
        _["recent_issues"], 
        _["emergency_section"], 
        _["checklist_section"]
    ])

    # 1. 주요 위험 및 유의사항 (tab1)
    with tab1:
        st.subheader(_["risk_info"])
        for r in info.get("위험 정보", ["정보 없음"]):
            st.warning(r)

        st.markdown("---")
        search_query = f"{sel_country} {sel_city} 여행 위험"
        st.link_button(
            f"⚠️ {sel_city} 여행 위험: {_['search_link_btn']}", 
            create_google_search_link(search_query),
            use_container_width=True
        )

    # 2. 대처 요령 (tab2)
    with tab2:
        st.subheader(_["tips_info"])
        for t in info.get("대처 요령", ["정보 없음"]):
            st.success(t)
        
        # 긴급 전화 정보만 유지
        st.markdown("---")
        col_call = st.columns(1)[0] # 환율 정보 제거 후 1컬럼으로 변경
        with col_call:
            phone_raw = info["현지 연락처"]["긴급 전화"]
            phone = phone_raw.split(" / ")[0]
            st.markdown(f"**{_["call_emergency"].split(" ")[-2]}:** `{phone_raw}`") # 긴급전화 번호 (한국어/영어)
            st.markdown(f"[{_['call_emergency']}](tel:{phone})")
        
        st.markdown("---")
        search_query = f"{sel_country} 여행 대처 요령"
        st.link_button(
            f"✅ {sel_country} 안전 수칙: {_['search_link_btn']}", 
            create_google_search_link(search_query),
            use_container_width=True
        )

    # 3. 최근 위험 이슈 (tab3)
    with tab3:
        st.subheader(_["recent_issues"])
        for issue in info.get("추가 이슈", ["최근 특이 이슈 보고된 바 없음"]):
            st.info(issue)
        
        st.markdown("---")
        search_query = f"{sel_country} {sel_city} 최근 이슈"
        st.link_button(
            f"📰 {sel_city} 최근 이슈: {_['search_link_btn']}", 
            create_google_search_link(search_query),
            use_container_width=True
        )

    # 4. 응급 상황 대처 (tab4) **<-- 수정된 부분**
    with tab4:
        st.subheader(_["emergency_section"])

        phone_raw = info["현지 연락처"]["긴급 전화"]
        phone = phone_raw.split(" / ")[0]

        st.markdown("### 🚨 " + (_["emergency_section"].split(" ")[-1] if lang=="ko" else "Local Emergency Number")) # 현지 긴급 전화 번호 
        st.error(f"**{phone_raw}**") # 긴급 전화 번호 강조

        st.markdown(f"[{_['call_emergency']} ({_["call_emergency"].split(" ")[-1] if lang=="ko" else "Connect to Primary Number"})](tel:{phone})")

        st.markdown("---")
        st.info("💡 " + (_["country_select"].split(" ")[-1] if lang=="ko" else "Country-specific Response Info:") + " 긴급 전화는 **1차적인 연결** 수단입니다. 상황별 상세 대처법은 아래 검색을 통해 확인하세요.")
        
        # 기존의 위험 정보를 참고로 보여줌
        st.markdown("#### ⚠️ " + (_["risk_info"].split(" ")[-2] if lang=="ko" else "Key Risks Reference"))
        for r in info.get("위험 정보", ["정보 없음"]):
            st.warning(f"• {r}")
            
        # Emergency Google Search Link
        st.markdown("---")
        current_search_query = f"{sel_country} 여행 긴급 상황 대처"
        st.link_button(
            f"🚨 **{sel_country}** " + (_["emergency_section"].split(" ")[-1] if lang=="ko" else "Detailed Emergency Response") + f": {_['search_link_btn']}",
            create_google_search_link(current_search_query),
            use_container_width=True
        )

    # 5. 여행 전 필수 점검 (tab5)
    with tab5:
        st.subheader(_["checklist_section"])
        checklist = st.session_state.checklist[sel_country]
        
        new_checklist_status = {}
        for item in checklist.keys():
            # 체크리스트 상태 업데이트
            is_checked = st.checkbox(item, checklist[item], key=f"{sel_country}_{item}")
            new_checklist_status[item] = is_checked
        
        st.session_state.checklist[sel_country] = new_checklist_status
        
        done = sum(new_checklist_status.values())
        total = len(new_checklist_status)
        
        st.markdown("---")
        if done < total:
            st.warning(f"⚠️ {done}/{total} {_["checklist_section"]}")
        else:
            st.success(_["complete_success"])
            
        st.markdown("---")
        search_query = f"{sel_country} 여행 준비물 체크리스트"
        st.link_button(
            f"🧳 " + (_["checklist_section"].split(" ")[-1] if lang=="ko" else "Check Travel Essentials") + f": {_['search_link_btn']}",
            create_google_search_link(search_query),
            use_container_width=True
        )


    # --- 환율 정보 섹션 (탭 외부로 분리) ---
    st.markdown("---")
    st.subheader(_["exchange_rate"])
    if sel_country in exchange_rates:
        code, rate, text = exchange_rates[sel_country]
        st.metric(f"{sel_country} ({code}) {_["exchange_rate"].split(" ")[-2] if lang=="ko" else "Exchange Rate Info"}", text if lang=="ko" else f"1 KRW ≈ {rate:,.4f} {code}")
    else:
        st.info("해당 국가의 환율 정보가 없습니다." if lang=="ko" else "No exchange rate information for this country.")
    st.markdown("---")

    # --- 지도 섹션 (탭 외부, V10 코드 기반 - 원래 위치로 복원) ---
    st.subheader(_["map_section"])
    lat, lon = coords.get(sel_city, (0, 0))
    st.map(pd.DataFrame({"lat":[lat],"lon":[lon]}))

    # --- 여행 기록 테이블 (V10 코드 그대로) ---
    
    # **<-- 수정된 부분: 초기화 버튼 추가 -->**
    def clear_travel_history():
        st.session_state.travel_history = []
        st.rerun()

    col_rec_title, col_rec_button = st.columns([0.7, 0.3])
    with col_rec_title:
        st.subheader(_["record_section"])
    with col_rec_button:
        # 영어일 경우 텍스트를 "Clear My Travel Records" 등으로 변경
        button_text = "🗑️ 나의 여행 기록 초기화" if lang == "ko" else "🗑️ Clear My Travel Records"
        help_text = "저장된 모든 여행 기록을 삭제합니다." if lang == "ko" else "Deletes all saved travel records."
        st.button(button_text, on_click=clear_travel_history, help=help_text)
    # **<-- 수정된 부분 끝 -->**

    record_label = _["record_section"]
    if st.session_state.travel_history:
        # 데이터프레임의 컬럼 이름도 선택된 언어에 따라 변경되도록 수정
        df_history = pd.DataFrame(st.session_state.travel_history)
        if lang == "en":
             df_history.columns = ["Country", "City", "Departure Date", "Return Date"]
        
        st.dataframe(df_history)
    else:
        st.info(f"{record_label}가/이 없습니다." if lang=="ko" else f"No {record_label.lower()} found.")

st.markdown("—")
st.markdown("© 2025 SafeTrip Assistant")
