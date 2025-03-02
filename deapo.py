import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import folium_static
import urllib.parse
from geopy.distance import geodesic

# ✅ 기존 대피소 API
BASE_URL_1 = "https://www.safetydata.go.kr/V2/api/DSSP-IF-00706"
API_KEY_1 = st.secrets.get("API_KEY_1", "")
encoded_key_1 = urllib.parse.quote(API_KEY_1)  # API Key 인코딩

# ✅ 신규 통합대피소 API
BASE_URL_2 = "https://www.safetydata.go.kr/V2/api/DSSP-IF-10941"
API_KEY_2 = st.secrets.get("API_KEY_2", "")
encoded_key_2 = urllib.parse.quote(API_KEY_2)  # API Key 인코딩

# ✅ 주요 도시 좌표 (시 단위 검색)
CITY_COORDINATES = {
    "서울특별시": (37.5665, 126.9780),
    "부산광역시": (35.1796, 129.0756),
    "대구광역시": (35.8714, 128.6014),
    "인천광역시": (37.4563, 126.7052),
    "광주광역시": (35.1595, 126.8526),
    "대전광역시": (36.3504, 127.3845),
    "울산광역시": (35.5384, 129.3114),
    "세종특별자치시": (36.4801, 127.2890),
    "경기도 수원시": (37.2636, 127.0286),
    "경기도 성남시": (37.4202, 127.1267),
    "경기도 용인시": (37.2411, 127.1776),
    "강원특별자치도 춘천시": (37.8813, 127.7298),
    "충청북도 청주시": (36.6424, 127.4891),
    "충청남도 천안시": (36.8151, 127.1139),
    "전라북도 전주시": (35.8242, 127.1475),
    "전라남도 목포시": (34.8118, 126.3922),
    "경상북도 포항시": (36.0190, 129.3435),
    "경상남도 창원시": (35.2285, 128.6811),
    "제주특별자치도 제주시": (33.4996, 126.5312),
}

@st.cache_data
def get_shelters(api_url, encoded_key):
    """
    API에서 대피소 데이터를 가져오는 함수 (두 개의 API 공통 사용)
    """
    params = {
        "serviceKey": encoded_key,
        "returnType": "json",
        "pageNo": "1",
        "numOfRows": "5000"
    }

    try:
        response = requests.get(api_url, params=params, timeout=5, verify=False)
        st.write(f"API 호출 URL: {response.url}")  # API URL 디버깅
        st.write(f"응답 상태 코드: {response.status_code}")
        st.write(f"응답 내용: {response.text[:500]}")  # 응답 내용 일부 출력
        
        response.raise_for_status()
        data = response.json()

        if data.get("header", {}).get("resultCode") != "00":
            st.error(f"⚠️ API 오류: {data.get('header', {}).get('resultMsg')}")
            return []

        return data.get("body", [])

    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ API 요청 중 오류 발생: {e}")
        return []

def run_deapi():
    st.title("🏠 전국 대피소 검색")

    # ✅ 두 개의 API에서 데이터 가져오기
    shelters_1 = get_shelters(BASE_URL_1, encoded_key_1)
    shelters_2 = get_shelters(BASE_URL_2, encoded_key_2)

    all_shelters = shelters_1 + shelters_2

    if not all_shelters:
        st.warning("⚠️ 전국 대피소 데이터를 불러올 수 없습니다.")
        return

    df = pd.DataFrame(all_shelters)

    df.rename(columns={"LAT": "latitude", "LOT": "longitude", "SHLT_NM": "쉘터이름"}, inplace=True)

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    df["주소"] = df["RONA_DADDR"].fillna(df["ADDR"]).fillna("주소 없음")
    df["쉘터이름"] = df["쉘터이름"].fillna("주소를 참고하세요").astype(str)

    df = df.dropna(subset=["latitude", "longitude"])

    st.subheader("🗺️ 전국 대피소 지도")

    st.info("📍 원하는 도시를 선택하면 해당 지역의 가장 가까운 대피소 10개를 검색합니다.")

    selected_region = st.selectbox("📌 도시 선택", list(CITY_COORDINATES.keys()), index=0)

    if st.button("🔍 검색"):
        user_lat, user_lon = CITY_COORDINATES[selected_region]

        df["거리"] = df.apply(lambda row: geodesic((user_lat, user_lon), (row["latitude"], row["longitude"])).km, axis=1)
        closest_df = df.nsmallest(10, "거리")

        st.subheader(f"📍 {selected_region} 인근 대피소 10개")
        search_map = folium.Map(location=[user_lat, user_lon], zoom_start=12)

        for _, row in closest_df.iterrows():
            folium.Marker(
                [row["latitude"], row["longitude"]],
                popup=f"<b>{row['쉘터이름']}</b><br>📍 {row['주소']}<br>📏 {round(row['거리'], 2)}km 거리",
                tooltip=row["주소"],
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(search_map)

        folium_static(search_map)

        st.subheader("📋 가장 가까운 대피소 10개")
        st.data_editor(
            closest_df[["쉘터이름", "주소", "거리"]].set_index("쉘터이름"),
            use_container_width=True,
            hide_index=False,
        )

if __name__ == "__main__":
    run_deapi()
