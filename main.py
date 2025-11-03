# 파일명: safetrip_v10_tabbed_final_rate_separated_modified_v3.py
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
        "call_emergency": "📞 긴급전화 걸기",
        "risk_info": "⚠️ 주요 위험 및 유의사항",
        "tips_info": "✅ 대처 요령",
        "recent_issues": "📰 최근 위험 이슈",
        "checklist_section": "🧳 여행 전 필수 점검",
        "record_section": "📜 나의 여행 기록",
        "complete_success": "🎉 모든 준비 완료! 안전한 여행 되세요.",
        "search_link_btn": "구글에서 더 알아보기",
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

# --- 나라/도시 이름 번역 딕셔너리 ---
country_city_translations = {
    "한국": "South Korea", "서울": "Seoul", "부산": "Busan", "제주": "Jeju", "인천": "Incheon", "대구": "Daegu", "광주": "Gwangju", "울산": "Ulsan",
    "일본": "Japan", "도쿄": "Tokyo", "오사카": "Osaka", "후쿠오카": "Fukuoka", "삿포로": "Sapporo", "교토": "Kyoto", "요코하마": "Yokohama", "나고야": "Nagoya",
    "태국": "Thailand", "방콕": "Bangkok", "푸켓": "Phuket", "치앙마이": "Chiang Mai", "파타야": "Pattaya", "끄라비": "Krabi", "코사무이": "Koh Samui",
    "캄보디아": "Cambodia", "프놈펜": "Phnom Penh", "시엠립": "Siem Reap", "시아누크빌": "Sihanoukville", "앙코르": "Angkor", "바탐방": "Battambang",
    "미국": "USA", "뉴욕": "New York", "LA": "LA", "샌프란시스코": "San Francisco", "하와이": "Hawaii", "시카고": "Chicago",
    "영국": "UK", "런던": "London", "맨체스터": "Manchester", "에든버러": "Edinburgh", "리버풀": "Liverpool",
    "호주": "Australia", "시드니": "Sydney", "멜버른": "Melbourne", "브리즈번": "Brisbane", "퍼스": "Perth",
    "베트남": "Vietnam", "하노이": "Hanoi", "호찌민": "Ho Chi Minh", "다낭": "Da Nang", "나트랑": "Nha Trang",
    "인도네시아": "Indonesia", "발리": "Bali", "자카르타": "Jakarta", "롬복": "Lombok", "욕야카르타": "Yogyakarta",
}

# --- 기본 데이터 확장 및 다국어 지원 추가 ---
# 데이터 구조를 변경하여 한국어(ko_data)와 영어(en_data)를 모두 포함
safety_data = {
    "한국": {
        "도시": ["서울", "부산", "제주", "인천", "대구", "광주", "울산"],
        "현지 연락처": {"긴급 전화": "112 / 119"},
        "ko_data": {
            "위험 정보": ["대체로 안전", "교통 혼잡 시간 주의"],
            "대처 요령": ["대중교통 이용 권장"],
            "추가 이슈": ["최근 소매치기 증가 보고됨"]
        },
        "en_data": {
            "위험 정보": ["Generally safe", "Be cautious during traffic congestion"],
            "대처 요령": ["Recommended to use public transportation"],
            "추가 이슈": ["Recent increase in pickpocketing reported"]
        }
    },
    "일본": {
        "도시": ["도쿄", "오사카", "후쿠오카", "삿포로", "교토", "요코하마", "나고야"],
        "현지 연락처": {"긴급 전화": "110 / 119"},
        "ko_data": {
            "위험 정보": ["지진 가능성", "유흥가 호객행위 주의"],
            "대처 요령": ["지진 발생 시 DROP, COVER, HOLD ON"],
            "추가 이슈": ["외국인 대상 유흥가 사기 사례 증가"]
        },
        "en_data": {
            "위험 정보": ["Possibility of earthquakes", "Caution against soliciting in entertainment districts"],
            "대처 요령": ["In case of earthquake: DROP, COVER, HOLD ON"],
            "추가 이슈": ["Increase in scam cases targeting foreigners in entertainment districts"]
        }
    },
    "태국": {
        "도시": ["방콕", "푸켓", "치앙마이", "파타야", "끄라비", "코사무이"],
        "현지 연락처": {"긴급 전화": "191 / 1669"},
        "ko_data": {
            "위험 정보": ["관광지 소매치기 주의", "툭툭 이용 시 가격 흥정 필수"],
            "대처 요령": ["공인된 택시 앱 사용"],
            "추가 이슈": ["밤늦은 루프탑 바에서 음료 음용 주의"]
        },
        "en_data": {
            "위험 정보": ["Beware of pickpocketing in tourist areas", "Mandatory price negotiation when using Tuktuk"],
            "대처 요령": ["Use certified taxi apps"],
            "추가 이슈": ["Caution when consuming beverages at late-night rooftop bars"]
        }
    },
    "캄보디아": {
        "도시": ["프놈펜", "시엠립", "시아누크빌", "앙코르", "바탐방"],
        "현지 연락처": {"긴급 전화": "117 / 119"},
        "ko_data": {
            "위험 정보": ["절도 발생 증가", "모기 매개 질병(뎅기열) 주의", "외국인 납치·사기 사례 보고됨"],
            "대처 요령": ["야간 외출 시 택시 이용 권장", "현금 보관 주의"],
            "추가 이슈": ["한국인 대상 유사 납치·사기 경고"]
        },
        "en_data": {
            "위험 정보": ["Increase in theft incidents", "Caution regarding mosquito-borne diseases (Dengue fever)", "Foreigner kidnapping/scam cases reported"],
            "대처 요령": ["Recommended to use taxis for night outings", "Be careful with cash storage"],
            "추가 이슈": ["Warning against attempted kidnapping and scams targeting South Koreans"]
        }
    },
    "미국": {
        "도시": ["뉴욕", "LA", "샌프란시스코", "하와이", "시카고"],
        "현지 연락처": {"긴급 전화": "911"},
        "ko_data": {
            "위험 정보": ["도심 일부 지역 범죄율 높음", "법규: 총기 사고 주의"],
            "대처 요령": ["야간에는 인적이 드문 곳 피하기"],
            "추가 이슈": ["특정 도시 관광객 대상 범죄 증가 보고됨"]
        },
        "en_data": {
            "위험 정보": ["High crime rate in some urban areas", "Law: Beware of gun incidents"],
            "대처 요령": ["Avoid sparsely populated areas at night"],
            "추가 이슈": ["Increase in crime targeting tourists in specific cities reported"]
        }
    },
    "영국": {
        "도시": ["런던", "맨체스터", "에든버러", "리버풀"],
        "현지 연락처": {"긴급 전화": "999"},
        "ko_data": {
            "위험 정보": ["기차·지하철 지연 가능성", "도심 소매치기 주의"],
            "대처 요령": ["혼잡 시간대 대비", "귀중품 주의"],
            "추가 이슈": ["런던 중심가에서 관광객 대상 사기 사례 증가"]
        },
        "en_data": {
            "위험 정보": ["Possibility of train/subway delays", "Beware of pickpocketing in city centers"],
            "대처 요령": ["Prepare for rush hours", "Guard valuables carefully"],
            "추가 이슈": ["Increase in scam cases targeting tourists in central London"]
        }
    },
    "호주": {
        "도시": ["시드니", "멜버른", "브리즈번", "퍼스"],
        "현지 연락처": {"긴급 전화": "000"},
        "ko_data": {
            "위험 정보": ["산불 및 폭우 주의", "환경: 독성 생물 주의"],
            "대처 요령": ["야생동물과의 접촉 자제"],
            "추가 이슈": ["해변 이용 시 파도·조류 주의 경고"]
        },
        "en_data": {
            "위험 정보": ["Caution for bushfires and heavy rain", "Environment: Beware of venomous wildlife"],
            "대처 요령": ["Refrain from contacting wild animals"],
            "추가 이슈": ["Warning about waves and currents when using beaches"]
        }
    },
    "베트남": {
        "도시": ["하노이", "호찌민", "다낭", "나트랑"],
        "현지 연락처": {"긴급 전화": "113 / 115"},
        "ko_data": {
            "위험 정보": ["오토바이 교통량 매우 많음", "핸드폰 날치기 주의"],
            "대처 요령": ["길거리 걸을 때 소지품 보호 철저"],
            "추가 이슈": ["관광지 밤거리 안전 주의"]
        },
        "en_data": {
            "위험 정보": ["Very high motorcycle traffic", "Beware of mobile phone snatching"],
            "대처 요령": ["Protect your belongings carefully when walking on the street"],
            "추가 이슈": ["Caution for safety in tourist night areas"]
        }
    },
    "인도네시아": {
        "도시": ["발리", "자카르타", "롬복", "욕야카르타"],
        "현지 연락처": {"긴급 전화": "110 / 118"},
        "ko_data": {
            "위험 정보": ["자연재해: 화산 활동 및 쓰나미 가능성", "교통: 무면허 운전 위험"],
            "대처 요령": ["현지 택시 대신 검증된 교통수단 이용"],
            "추가 이슈": ["외국인 대상 교통사고 증가 보고됨"]
        },
        "en_data": {
            "위험 정보": ["Natural Disasters: Possibility of volcanic activity and tsunamis", "Traffic: Risk of unlicensed driving"],
            "대처 요령": ["Use verified transport methods instead of local taxis"],
            "추가 이슈": ["Increase in traffic accidents involving foreigners reported"]
        }
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

# --- 다국어 처리 함수 ---

def translate_name(name, lang):
    """나라/도시 이름을 선택된 언어로 번역합니다."""
    if lang == "en":
        return country_city_translations.get(name, name)
    return name

def get_country_name_list(lang):
    """현재 언어에 맞는 국가 이름 리스트를 반환합니다."""
    if lang == "en":
        return [translate_name(c, lang) for c in safety_data.keys()]
    return list(safety_data.keys())

def get_city_name_list(country_ko, lang):
    """한국어 국가 이름에 해당하는 도시 리스트를 현재 언어에 맞게 반환합니다."""
    cities_ko = safety_data.get(country_ko, {}).get("도시", [])
    if lang == "en":
        return [translate_name(city, lang) for city in cities_ko]
    return cities_ko

def get_country_ko_name(country_display_name, lang):
    """표시되는 국가 이름을 한국어 이름으로 역변환합니다."""
    if lang == "ko":
        return country_display_name
    
    for ko_name, en_name in country_city_translations.items():
        if en_name == country_display_name and ko_name in safety_data.keys():
            return ko_name
    return country_display_name 

def get_translated_data(country_ko, data_key, lang):
    """선택된 언어에 맞는 위험 정보를 가져옵니다."""
    info = safety_data.get(country_ko, {})
    data_source = info.get(f"{lang}_data", info.get("ko_data", {})) # ko_data를 기본값으로 사용
    
    # 데이터 키를 한국어로 통일하여 접근 (데이터 딕셔너리 내부 키)
    ko_key = {
        "risk_info": "위험 정보",
        "tips_info": "대처 요령",
        "recent_issues": "추가 이슈"
    }.get(data_key)
    
    # 이제 데이터 딕셔너리에서 직접 정보를 가져옵니다.
    return data_source.get(ko_key, ["정보 없음" if lang == "ko" else "No information available"])


# --- Google 검색 링크 생성 함수 ---
def create_google_search_link(query):
    base_url = "https://www.google.com/search?q="
    return base_url + query.replace(" ", "+")


# ------------------------------------------------------------------------------------------------------
# --- Streamlit UI 시작 ---
# ------------------------------------------------------------------------------------------------------

# 언어 선택
lang_option = st.selectbox(translations["ko"]["lang_select"], ("한국어", "English"), key="lang_choice")
lang = "ko" if lang_option == "한국어" else "en"
_ = translations[lang]

st.set_page_config(page_title=_["title"], page_icon="✈️", layout="wide")

st.title(_["title"])
st.caption(_["caption"])

st.markdown("---")

# --- 여행 일정표 입력 기능 ---
st.subheader(_["travel_schedule"])
departure = st.date_input(_["departure"], datetime.date.today())
return_date = st.date_input(_["return"], datetime.date.today() + datetime.timedelta(days=7))

if return_date < departure:
    st.error("⚠️ " + _["return"] + "이/가 " + _["departure"] + "보다 앞설 수 없습니다." if lang=="ko" else "⚠️ " + _["return"] + " cannot be earlier than " + _["departure"] + ".")
else:
    duration = (return_date - departure).days
    st.write(_["duration_prefix"] + f"{duration}" + _["days_suffix"])

st.markdown("---")

# --- 세션 상태 초기화 및 관리 ---
v10_checklist_items = ["여권/비자 확인", "보험 가입", "비상연락망 저장", "신용카드 분실 신고처 메모"]
if lang == "en":
    v10_checklist_items = ["Passport/Visa Check", "Insurance Enrollment", "Save Emergency Contacts", "Note Credit Card Loss Reporting"]

if "travel_history" not in st.session_state:
    st.session_state.travel_history = []
if "checklist" not in st.session_state:
    st.session_state.checklist = {} 
if "report_on" not in st.session_state:
    st.session_state.report_on = False

# 선택된 국가/도시는 한국어 이름으로 저장합니다.
if "selected_country_ko" not in st.session_state:
    st.session_state.selected_country_ko = list(safety_data.keys())[0]
if "selected_city_ko" not in st.session_state:
    st.session_state.selected_city_ko = safety_data[st.session_state.selected_country_ko]["도시"][0]


# --- 국가/도시 선택 ---
col_country, col_city = st.columns(2)

country_names = get_country_name_list(lang)
default_country_display = translate_name(st.session_state.selected_country_ko, lang)
default_country_index = country_names.index(default_country_display) if default_country_display in country_names else 0

with col_country:
    country_display_name = st.selectbox(_["country_select"], country_names, index=default_country_index, key="country_select_box")
country_ko = get_country_ko_name(country_display_name, lang) 

city_names = get_city_name_list(country_ko, lang)
default_city_display = translate_name(st.session_state.selected_city_ko, lang)
default_city_index = city_names.index(default_city_display) if default_city_display in city_names else 0

with col_city:
    city_display_name = st.selectbox(_["city_select"], city_names, index=default_city_index, key="city_select_box")
city_ko = get_country_ko_name(city_display_name, lang) 


if st.button(_["search_report"], type="primary"):
    # 여행 기록은 한국어 이름으로 저장
    st.session_state.travel_history.append({
        "국가": country_ko,
        "도시": city_ko,
        "출국일": departure,
        "귀국일": return_date
    })
    # 체크리스트 항목은 한국어로 저장 (영어 전환 시 번역을 위해)
    checklist_items_ko = ["여권/비자 확인", "보험 가입", "비상연락망 저장", "신용카드 분실 신고처 메모"]
    if country_ko not in st.session_state.checklist:
        st.session_state.checklist[country_ko] = {
            item: False for item in checklist_items_ko
        }
    st.session_state.selected_country_ko = country_ko
    st.session_state.selected_city_ko = city_ko
    st.session_state.report_on = True
    st.rerun()

# --- 보고서 표시 (st.tabs 사용) ---
if st.session_state.report_on:
    sel_country_ko = st.session_state.selected_country_ko
    sel_city_ko = st.session_state.selected_city_ko
    
    sel_country_display = translate_name(sel_country_ko, lang)
    sel_city_display = translate_name(sel_city_ko, lang)
    
    info = safety_data.get(sel_country_ko, {})

    if not info:
        st.error(f"❌ **{sel_country_display}**에 대한 상세 정보가 없습니다. 목록에서 다른 국가를 선택해 주세요." if lang=="ko" else f"❌ No detailed information available for **{sel_country_display}**. Please select another country from the list.")
        st.stop() 

    st.header(f"📋 {sel_country_display} – {sel_city_display}")
    
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
        risks = get_translated_data(sel_country_ko, "risk_info", lang)
        for r in risks:
            st.warning(r)

        st.markdown("---")
        search_query = f"{sel_country_display} {sel_city_display} 여행 위험"
        st.link_button(
            f"⚠️ {sel_city_display} 여행 위험: {_['search_link_btn']}", 
            create_google_search_link(search_query),
            use_container_width=True
        )

    # 2. 대처 요령 (tab2)
    with tab2:
        st.subheader(_["tips_info"])
        tips = get_translated_data(sel_country_ko, "tips_info", lang)
        for t in tips:
            st.success(t)
        
        st.markdown("---")
        col_call = st.columns(1)[0]
        with col_call:
            phone_raw = info["현지 연락처"]["긴급 전화"]
            phone = phone_raw.split(" / ")[0]
            st.markdown(f"**{_["call_emergency"].split(" ")[-2]}:** `{phone_raw}`" if lang=="ko" else f"**Emergency Phone Number:** `{phone_raw}`")
            st.markdown(f"[{_['call_emergency']}](tel:{phone})")
        
        st.markdown("---")
        search_query = f"{sel_country_display} 여행 대처 요령"
        st.link_button(
            f"✅ {sel_country_display} 안전 수칙: {_['search_link_btn']}", 
            create_google_search_link(search_query),
            use_container_width=True
        )

    # 3. 최근 위험 이슈 (tab3)
    with tab3:
        st.subheader(_["recent_issues"])
        issues = get_translated_data(sel_country_ko, "recent_issues", lang)
        for issue in issues:
            st.info(issue)
        
        st.markdown("---")
        search_query = f"{sel_country_display} {sel_city_display} 최근 이슈"
        st.link_button(
            f"📰 {sel_city_display} 최근 이슈: {_['search_link_btn']}", 
            create_google_search_link(search_query),
            use_container_width=True
        )

    # 4. 응급 상황 대처 (tab4)
    with tab4:
        st.subheader(_["emergency_section"])

        phone_raw = info["현지 연락처"]["긴급 전화"]
        phone = phone_raw.split(" / ")[0]

        st.markdown("### 🚨 " + (_["emergency_section"].split(" ")[-1] if lang=="ko" else "Local Emergency Number"))
        st.error(f"**{phone_raw}**")

        st.markdown(f"[{_['call_emergency']} ({_["call_emergency"].split(" ")[-1] if lang=="ko" else "Connect to Primary Number"})](tel:{phone})")

        st.markdown("---")
        info_text = "💡 **국가별 맞춤 대처 정보:** 긴급 전화는 **1차적인 연결** 수단입니다. 상황별 상세 대처법은 아래 검색을 통해 확인하세요."
        if lang == "en":
            info_text = "💡 **Country-specific Response Info:** Emergency call is the **primary connection** method. Check detailed response tips below."
        st.info(info_text)
        
        st.markdown("#### ⚠️ " + (_["risk_info"].split(" ")[-2] if lang=="ko" else "Key Risks Reference"))
        for r in risks: # 이미 가져온 번역된 위험 정보 사용
            st.warning(f"• {r}")
            
        st.markdown("---")
        current_search_query = f"{sel_country_display} 여행 긴급 상황 대처"
        st.link_button(
            f"🚨 **{sel_country_display}** " + (_["emergency_section"].split(" ")[-1] if lang=="ko" else "Detailed Emergency Response") + f": {_['search_link_btn']}",
            create_google_search_link(current_search_query),
            use_container_width=True
        )

    # 5. 여행 전 필수 점검 (tab5)
    with tab5:
        st.subheader(_["checklist_section"])
        checklist = st.session_state.checklist[sel_country_ko]
        
        new_checklist_status = {}
        for ko_item in checklist.keys():
            # 체크리스트 항목을 현재 언어에 맞게 표시
            display_item = ko_item if lang == "ko" else v10_checklist_items[checklist_items_ko.index(ko_item)]
            is_checked = st.checkbox(display_item, checklist[ko_item], key=f"{sel_country_ko}_{ko_item}")
            new_checklist_status[ko_item] = is_checked
        
        st.session_state.checklist[sel_country_ko] = new_checklist_status
        
        done = sum(new_checklist_status.values())
        total = len(new_checklist_status)
        
        st.markdown("---")
        if done < total:
            st.warning(f"⚠️ {done}/{total} {_["checklist_section"]}")
        else:
            st.success(_["complete_success"])
            
        st.markdown("---")
        search_query = f"{sel_country_display} 여행 준비물 체크리스트"
        st.link_button(
            f"🧳 " + (_["checklist_section"].split(" ")[-1] if lang=="ko" else "Check Travel Essentials") + f": {_['search_link_btn']}",
            create_google_search_link(search_query),
            use_container_width=True
        )


    # --- 환율 정보 섹션 (탭 외부로 분리) ---
    st.markdown("---")
    st.subheader(_["exchange_rate"])
    if sel_country_ko in exchange_rates:
        code, rate, text = exchange_rates[sel_country_ko]
        st.metric(f"{sel_country_display} ({code}) {_["exchange_rate"].split(" ")[-2] if lang=="ko" else "Exchange Rate Info"}", text if lang=="ko" else f"1 KRW ≈ {rate:,.4f} {code}")
    else:
        st.info("해당 국가의 환율 정보가 없습니다." if lang=="ko" else "No exchange rate information for this country.")
    st.markdown("---")

    # --- 지도 섹션 (탭 외부) ---
    st.subheader(_["map_section"])
    lat, lon = coords.get(sel_city_ko, (0, 0))
    st.map(pd.DataFrame({"lat":[lat],"lon":[lon]}))

    # --- 여행 기록 테이블 ---
    def clear_travel_history():
        st.session_state.travel_history = []
        st.rerun()

    col_rec_title, col_rec_button = st.columns([0.7, 0.3])
    with col_rec_title:
        st.subheader(_["record_section"])
    with col_rec_button:
        button_text = "🗑️ 나의 여행 기록 초기화" if lang == "ko" else "🗑️ Clear My Travel Records"
        help_text = "저장된 모든 여행 기록을 삭제합니다." if lang == "ko" else "Deletes all saved travel records."
        st.button(button_text, on_click=clear_travel_history, help=help_text)

    record_label = _["record_section"]
    if st.session_state.travel_history:
        df_history = pd.DataFrame(st.session_state.travel_history)
        
        # 데이터프레임의 내용을 현재 언어에 맞게 변환
        if lang == "en":
             df_history.columns = ["Country", "City", "Departure Date", "Return Date"]
             df_history["Country"] = df_history["Country"].apply(lambda x: translate_name(x, 'en'))
             df_history["City"] = df_history["City"].apply(lambda x: translate_name(x, 'en'))

        st.dataframe(df_history)
    else:
        st.info(f"{record_label}가/이 없습니다." if lang=="ko" else f"No {record_label.lower()} found.")

st.markdown("—")
st.markdown("© 2025 SafeTrip Assistant")
