import streamlit as st
import requests
import re
from datetime import datetime
import pytz  # ✅ 올바른 timezone 사용
from bs4 import BeautifulSoup
import feedparser

# ✅ 한국 시간대 설정 (UTC → KST 변환)
KST = pytz.timezone('Asia/Seoul')
UTC = pytz.utc  # ✅ UTC 정의

def clean_html_tags(text):
    """HTML 태그 및 특수문자 제거"""
    text = re.sub(r"<[^>]*>", "", text)  # <b> 같은 HTML 태그 제거
    text = text.replace("&quot;", '"').replace("&amp;", "&")  # 특수문자 처리
    return text.strip()

def format_date_korean(date_str):
    """네이버 뉴스 날짜를 'YYYY년 M월 D일' 형식으로 변환 및 datetime 객체 반환"""
    try:
        date_obj = datetime.strptime(date_str.replace(".", "-").strip(), "%Y-%m-%d")
        return date_obj, f"{date_obj.year}년 {date_obj.month}월 {date_obj.day}일"
    except ValueError:
        return None, date_str  # 변환 실패 시 원래 문자열 유지

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
    news_items = soup.select("div.news_area")

    for item in news_items[:15]:  
        title = item.select_one("a.news_tit").text
        link = item.select_one("a.news_tit")["href"]
        source = item.select_one("a.info.press").text.strip()
        pub_date = item.select_one("span.info").text.strip()
        
        date_obj, pub_date_korean = format_date_korean(pub_date)

        if date_obj:
            news_list.append({
                "title": title,
                "source": source,
                "link": link,
                "pub_date": pub_date_korean,
                "date_obj": date_obj  # ✅ datetime 객체 저장
            })

    return news_list

def get_google_earthquake_news():
    """구글 뉴스 RSS에서 최신 지진 관련 뉴스 가져오기"""
    rss_url = "https://news.google.com/rss/search?q=지진&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)

    news_list = []
    for entry in feed.entries[:15]:  
        pub_date_obj = datetime(*entry.published_parsed[:6])
        pub_date_obj = UTC.localize(pub_date_obj).astimezone(KST)
        pub_date_korean = f"{pub_date_obj.year}년 {pub_date_obj.month}월 {pub_date_obj.day}일"

        news_list.append({
            "title": entry.title,
            "link": entry.link,
            "pub_date": pub_date_korean,
            "date_obj": pub_date_obj  # ✅ datetime 객체 저장
        })
    
    return news_list

def run_news():
    st.title("🌍 실시간 지진 뉴스")

    if st.button("🔄 최신 뉴스 불러오기"):
        st.rerun()

    st.write(f"### 📰 2025년 최신 지진 뉴스")

    naver_news = get_naver_earthquake_news()
    google_news = get_google_earthquake_news()
    
    news_articles = sorted(naver_news + google_news, key=lambda x: x['date_obj'], reverse=True)
    
    if not news_articles:
        st.write("❌ 관련 지진 뉴스가 없습니다. (최신 데이터를 다시 확인해 주세요.)")
    else:
        for news in news_articles:
            with st.expander(f"📰 [{news.get('pub_date', '날짜 없음')}] {news['title']}"):
                st.write(f"🔗 [기사 원문 보기]({news['link']})")

if __name__ == "__main__":
    run_news()