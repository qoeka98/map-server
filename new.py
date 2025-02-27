import streamlit as st
import folium
from streamlit_folium import st_folium
import joblib
import pandas as pd
import requests
from folium.plugins import HeatMap
from datetime import datetime, timedelta

# ✅ 1. 저장된 모델 불러오기
loaded_rf = joblib.load("earthquake_model.joblib")
loaded_scaler = joblib.load("scaler.joblib")



# ✅ 현재 날짜를 기반으로 실시간 데이터 요청
def get_past_earthquakes(min_magnitude=5.0, days=30, limit=5000):
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")

    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": start_date,
        "endtime": end_date,
        "minmagnitude": min_magnitude,
        "limit": limit,
        "orderby": "time"
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ USGS API 요청 실패: {e}")
        return pd.DataFrame()

    earthquakes = []
    for feature in data.get("features", []):
        properties = feature["properties"]
        geometry = feature["geometry"]
        earthquakes.append({
            "time": properties["time"],
            "magnitude": properties["mag"],
            "lat": geometry["coordinates"][1],
            "lon": geometry["coordinates"][0],
            "depth": geometry["coordinates"][2]
        })
    return pd.DataFrame(earthquakes)

# ✅ 3. 특정 지역이 바다인지 판별하는 함수
def get_ocean_name(lat, lon):
    if -180 <= lon <= -70 and -60 <= lat <= 60:
        return "태평양"
    elif -70 < lon < 20 and -60 <= lat <= 60:
        return "대서양"
    elif 20 <= lon <= 180 and -60 <= lat <= 60:
        return "인도양"
    elif -180 <= lon <= 180 and lat > 60:
        return "북극해"
    elif -180 <= lon <= 180 and lat < -60:
        return "남극해"
    return "해상"

# ✅ 4. Nominatim API를 사용하여 위도, 경도를 나라와 지역명으로 변환
@st.cache_data(ttl=3600)
def get_location_name(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&accept-language=ko"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "address" in data and data["address"]:
            address = data["address"]
            country = address.get("country", "")
            state = address.get("state", "")
            city = address.get("city", address.get("town", address.get("village", "")))
            location = f"{country}, {state} {city}".strip()
            return location if location else get_ocean_name(lat, lon)
    except requests.exceptions.RequestException:
        pass
    
    return get_ocean_name(lat, lon)

# ✅ 5. 지진 발생 확률 예측 함수
def predict_earthquake(lat, lon, depth=10.0):
    input_df = pd.DataFrame([[lat, lon, depth]], columns=['lat', 'lon', 'depth'])
    input_scaled = loaded_scaler.transform(input_df)
    prob = loaded_rf.predict_proba(input_scaled)[0][1]
    return round(prob * 100, 2)

# ✅ 6. 주요 국가 위험도 계산 (위도, 경도 기준)
major_countries = {
    "한국": [37.5665, 126.9780],
    "일본": [35.682839, 139.759455],
    "중국": [39.9042, 116.4074],
    "미국": [38.9072, -77.0369],
    "인도": [28.6139, 77.2090]
}

def get_major_countries_risk():
    country_risks = []
    for country, coords in major_countries.items():
        prob = predict_earthquake(coords[0], coords[1])
        country_risks.append({
            "country": country,
            "location": get_location_name(coords[0], coords[1]),
            "lat": coords[0],
            "lon": coords[1],
            "risk": prob
        })
    return pd.DataFrame(country_risks)

# ✅ 7. Streamlit UI 실행
def run_new():
    st.title("🌍 실시간 지진 예측 시스템")

    # ✅ 8. 실시간 지진 데이터 로드
    with st.spinner("지진 데이터를 불러오는 중..."):
        df_earthquakes = get_past_earthquakes()

    # ✅ 9. 실시간 예측 위험 지역 정리
    df_top_magnitude = df_earthquakes.sort_values(by="magnitude", ascending=False).head(5)
    st.write("### 🔥 실시간 지진 예측 정보 🔥")
    st.info("실시간으로 정보를 확인하는 중이라 잠시 기다려주세요. ")
    for _, row in df_top_magnitude.iterrows():
        location_name = get_location_name(row["lat"], row["lon"])
        risk = predict_earthquake(row["lat"], row["lon"])
        st.write(f"📍 **{location_name} → 예상 지진 확률: {risk}%**")

    

    
    st.write("### 🔍 실시간 지진 예측 지도")
    m1 = folium.Map(location=[20, 0], zoom_start=2, tiles="OpenStreetMap")
    for _, row in df_top_magnitude.iterrows():
         folium.Marker(
            location=[row["lat"], row["lon"]],
             popup=f"📍 {get_location_name(row['lat'], row['lon'])}<br>예상 지진 확률: {predict_earthquake(row['lat'], row['lon'])}%",
            icon=folium.Icon(color="red")
        ).add_to(m1)
    st_folium(m1, height=500, width=600)

    
    # ✅ 10. 주요 국가 위험도 정보 표시
    st.write("### 🏛 주요 국가 지진 위험도")
    major_risk_df = get_major_countries_risk()
    for _, row in major_risk_df.iterrows():
        st.write(f"🌏 **{row['country']} ({row['location']}) → 예상 지진 확률: {row['risk']}%**")

    # ✅ 11. 실시간 예측 지도 & 주요 국가 위험도 히트맵 배치


    st.write("### 🌍 주요 국가 지진 위험도 히트맵")
    m2 = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB Positron")
    heat_data = major_risk_df[['lat', 'lon', 'risk']].values.tolist()
    HeatMap(heat_data, radius=30, blur=10, min_opacity=0.5).add_to(m2)
    st_folium(m2, height=500, width=600)

    # ✅ 12. 과거 1년 지진 히트맵 (다시 추가!)
    st.write("### 📊 과거 1년간 전 세계 지진 히트맵")
    m3 = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB DarkMatter")
    heat_data = df_earthquakes[['lat', 'lon', 'magnitude']].values.tolist()
    HeatMap(heat_data, radius=10, blur=5, min_opacity=0.3).add_to(m3)
    st_folium(m3, height=500, width=900)
