import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import folium_static
import urllib.parse

# ✅ 공공데이터포털에서 올바른 API 기본 도메인 확인 후 변경 필요
BASE_URL = "https://apis.data.go.kr/V2/api/DSSP-IF-10941"
API_KEY = "L6GN1MCZW142W4GF"  # 실제 API 키 사용


# API 호출 함수
def get_shelters(region):
    """
    입력된 지역명을 기반으로 API에서 대피소 정보를 가져온다.
    """
    region_encoded = urllib.parse.quote(region)  # 한글 URL 인코딩
    url = f"{BASE_URL}?serviceKey={API_KEY}&region={region_encoded}&type=json"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

        data = response.json()
        if "shelters" in data:
            return data["shelters"]

    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ API 요청 중 오류 발생: {e}")

    return []

# Streamlit UI
def run_deapi():
    st.title("🏠 지역별 대피소 검색")
    st.info("📍 원하는 지역을 입력하면 해당 지역의 대피소 위치를 확인할 수 있습니다.")

    # 기본 지도 표시 (대한민국 중심)
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)
    folium_static(m)

    # 사용자 입력
    region = st.text_input("🔍 검색할 지역명을 입력하세요 (예: 서울, 부산 등):")

    if st.button("검색"):
        if region:
            shelters = get_shelters(region)

            if shelters:
                df = pd.DataFrame(shelters)

                # 위도/경도 평균값으로 지도 중심 설정
                map_center = [df["latitude"].astype(float).mean(), df["longitude"].astype(float).mean()]
                shelter_map = folium.Map(location=map_center, zoom_start=12)

                # 대피소 위치 마커 추가
                for _, row in df.iterrows():
                    folium.Marker(
                        [row["latitude"], row["longitude"]],
                        popup=f"{row['shelterName']} ({row['address']})",
                        tooltip=row["shelterName"]
                    ).add_to(shelter_map)

                # 지도 출력
                folium_static(shelter_map)

                # 대피소 목록 출력
                st.subheader("📋 대피소 목록")
                st.dataframe(df[["shelterName", "address"]])

            else:
                st.warning(f"⚠️ '{region}' 지역에 대한 대피소 정보를 찾을 수 없습니다.")
        else:
            st.error("❌ 지역명을 입력하세요.")

# 실행
if __name__ == "__main__":
    run_deapi()
