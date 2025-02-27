import streamlit as st
import requests
import re
from datetime import datetime, timedelta, timezone
from pytz import timezone
from bs4 import BeautifulSoup
import feedparser

# ✅ 한국 시간대 설정 (UTC → KST 변환)
KST = timezone('Asia/Seoul')

def clean_html_tags(text):
    """HTML 태그 및 특수문자 제거"""
    text = re.sub(r"<[^>]*>", "", text)  # <b> 같은 HTML 태그 제거
    text = text.replace("&quot;", '"').replace("&amp;", "&")  # 특수문자 처리
    return text.strip()

def get_naver_earthquake_news():
    """네이버 뉴스 검색 결과에서 최신 지진 관련 뉴스 크롤링"""
    query = "지진 OR 강진 OR 여진 OR 쓰나미 OR 해일 OR 규모 OR 진앙 OR 피해"
    url = f"https://search.naver.com/search.naver?where=news&query={query}&sort=1"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news_list = []
    news_items = soup.select("div.news_area")  # 네이버 뉴스 기사 영역

    today = datetime.now(KST).strftime('%Y')  # ✅ 현재 연도 필터링

    for item in news_items[:10]:  # ✅ 최신 뉴스 10개 가져오기
        title = item.select_one("a.news_tit").text
        link = item.select_one("a.news_tit")["href"]
        source = item.select_one("a.info.press").text.strip()
        pub_date = item.select_one("span.info").text.strip()
        
        # ✅ 연도 필터링: 2025년 기사만 포함
        if today in pub_date and any(keyword in title for keyword in ["지진", "강진", "여진", "쓰나미", "해일", "규모", "진앙", "피해"]):
            news_list.append({
                "title": title,
                "source": source,
                "link": link,
                "pub_date": pub_date
            })

    return news_list

def get_google_earthquake_news():
    """구글 뉴스 RSS에서 최신 지진 관련 뉴스 가져오기"""
    rss_url = "https://news.google.com/rss/search?q=지진&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)

    news_list = []
    for entry in feed.entries[:5]:  # ✅ 최신 뉴스 5개 가져오기
        news_list.append({
            "title": entry.title,
            "link": entry.link,
            "pub_date": entry.published
        })
    
    return news_list

# ✅ 4. Streamlit UI 설정
def run_news():
    st.title("🌍 실시간 지진 예측 시스템")

    # ✅ 5. "새로고침" 버튼 추가
    if st.button("🔄 최신 뉴스 불러오기"):
        st.rerun()

    # ✅ 6. 최근 뉴스 표시
    st.write(f"### 📰 2025년 최신 지진 뉴스 (네이버 & 구글)")

    naver_news = get_naver_earthquake_news()
    google_news = get_google_earthquake_news()
    
    news_articles = naver_news + google_news
    
    if not news_articles:
        st.write("❌ 관련 지진 뉴스가 없습니다. (최신 데이터를 다시 확인해 주세요.)")
    else:
        for news in news_articles:
            with st.expander(f"📰 [{news.get('pub_date', '날짜 없음')}] {news['title']}"):
                st.write(f"🔗 [원문 보기]({news['link']})")
