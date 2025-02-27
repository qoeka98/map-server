import streamlit as st
import joblib
import requests
import re

# ✅ 1. API 키 보호 (환경 변수 사용)
CLIENT_ID = st.secrets["YOUR_CLIENT_ID"]
CLIENT_SECRET = st.secrets["YOUR_CLIENT_SECRET"]

# ✅ 2. 대표 지진 관련 키워드
EARTHQUAKE_KEYWORDS = ["지진", "강진", "진도", "여진", "해일", "쓰나미", "earthquake", "seismic"]

def clean_html_tags(text):
    """HTML 태그 및 특수문자 제거"""
    text = re.sub(r"<[^>]*>", "", text)  # <b> 같은 HTML 태그 제거
    text = text.replace("&quot;", '"').replace("&amp;", "&")  # 특수문자 처리
    return text.strip()

def get_earthquake_news():
    """네이버 뉴스 API에서 지진 관련 기사 가져오기"""
    
    # ✅ "지진" 키워드로 검색 (API가 OR 검색을 지원하지 않기 때문)
    query = ["지진","여진","쓰나미","해일","강진"]
    url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=10&sort=date"
    
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        # ✅ API 응답 상태 확인 (디버깅용)
        if response.status_code != 200:
            st.write(f"❌ API 오류 (상태 코드: {response.status_code})")
            return [{"title": "❌ 뉴스 데이터를 불러올 수 없습니다.",
                     "description": f"API 오류 (상태 코드: {response.status_code})",
                     "link": ""}]

        response.raise_for_status()
        news_data = response.json()
        
       

        # ✅ 3. 지진 관련 뉴스 필터링 (제목 또는 본문에 반드시 키워드 포함)
        filtered_news = []
        for item in news_data.get("items", []):
            title = clean_html_tags(item["title"])
            description = clean_html_tags(item["description"])
            link = item["originallink"]

            # ✅ 필터링 기준 완화 (title 또는 description에 키워드가 하나라도 포함되면 허용)
            if any(kw in title or kw in description for kw in EARTHQUAKE_KEYWORDS):
                filtered_news.append({
                    "title": title,
                    "description": description,
                    "link": link
                })
        
        # ✅ 4. 관련 뉴스가 없을 경우 메시지 반환
        if not filtered_news:
            return [{"title": "❌ 관련 뉴스가 없습니다.", "description": "현재 지진 관련 뉴스가 없습니다.", "link": ""}]

        return filtered_news[:5]  # ✅ 최대 5개 뉴스만 반환

    except requests.exceptions.RequestException as e:
        return [{"title": "❌ 뉴스 데이터를 불러올 수 없습니다.",
                 "description": f"네트워크 오류 또는 API 키 문제 ({str(e)})",
                 "link": ""}]


# ✅ 5. 저장된 모델 불러오기
loaded_rf = joblib.load("earthquake_model.joblib")
loaded_scaler = joblib.load("scaler.joblib")


# ✅ 6. Streamlit UI 설정
def run_news():
    st.title("🌍 실시간 지진 예측 시스템")

    # ✅ 7. 실시간 지진 뉴스 표시
    st.write("### 📰 최근 7일간 전 세계 지진 뉴스")

    news_articles = get_earthquake_news()
    
    for news in news_articles:
        with st.expander(f"📰 {news['title']}"):
            st.write(f"📌 **기사 내용:**\n{news['description']}")
            if news["link"]:
                st.write(f"🔗 [원문 보기]({news['link']})")
