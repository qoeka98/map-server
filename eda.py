import streamlit as st
import folium
from streamlit_folium import st_folium
import joblib
import pandas as pd
import requests
from folium.plugins import HeatMap

model_path = "earthquake_model.joblib"
scaler_path = "scaler.joblib"

# Load the scaler and model
loaded_scaler = joblib.load(scaler_path)
loaded_rf = joblib.load(model_path)

# ✅ 1. 과거 지진 데이터를 USGS API에서 가져오기
@st.cache_data(ttl=3600)
def get_past_earthquakes(min_magnitude=4.5, start_date="2023-01-01", end_date="2024-01-01", limit=1000):
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
        response = requests.get(url, params=params, timeout=5)
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
            "time": properties.get("time"),
            "magnitude": properties.get("mag"),
            "lat": geometry["coordinates"][1],
            "lon": geometry["coordinates"][0],
            "depth": geometry["coordinates"][2]
        })
    return pd.DataFrame(earthquakes)

# ✅ 1년간 규모 4.5 이상의 지진 데이터 가져오기
df_earthquakes = get_past_earthquakes()

# ✅ 2. 주소를 위도, 경도로 변환하는 함수
@st.cache_data(ttl=3600)
def get_lat_lon_from_address(address, retries=3):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={address}&limit=1&accept-language=ko"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
        except requests.exceptions.RequestException:
            return None, None
    return None, None

# ✅ 3. 지진 발생 확률 예측 함수
def predict_earthquake(lat, lon, depth=10.0):
    input_df = pd.DataFrame([[lat, lon, depth]], columns=['lat', 'lon', 'depth'])
    input_scaled = loaded_scaler.transform(input_df)  # Scale the input data using the loaded scaler
    prob = loaded_rf.predict_proba(input_scaled)[0][1]  # Get the probability for class 1 (earthquake)
    return round(prob * 100, 2)

# ✅ 4. 위험 등급 판별 함수
def get_risk_level(prob):
    if prob < 10:
        return "🟢 매우 낮음 (Very Low Risk)", "일반적인 생활을 유지하세요."
    elif prob < 40:
        return "🟢 낮음 (Low Risk)", "긴급 대비책을 점검하세요."
    elif prob < 50:
        return "🟡 보통 (Moderate Risk)", "비상 물품을 준비하고 대피 경로를 확인하세요."
    elif prob < 70:
        return "🟠 높음 (High Risk)", "내진 안전 가구를 점검하고 가족과 연락망을 정리하세요."
    elif prob < 90:
        return "🟠 매우 높음 (Very High Risk)", "대피소 위치를 파악하고 즉시 대피할 준비를 하세요."
    else:
        return "🔴 위험 (Severe Risk)", "즉시 대피소로 이동하고 비상 물품을 챙기세요."

def run_eda():
    # ✅ Streamlit UI 설정
    st.title("🌍 실시간 지진 예측 시스템")

    # ✅ 5. 주소 입력 필드
    address = st.text_input("📍 주소를 입력하세요 (예: 서울특별시 강남구)")

    # 기본 좌표 (한국 중앙)
    if 'lat' not in st.session_state or 'lon' not in st.session_state:
        st.session_state.lat, st.session_state.lon = 36.5, 127.8  # 한국의 중앙 위치

    lat, lon = st.session_state.lat, st.session_state.lon  # 기본 좌표

    prob = None  # 예측 결과 기본값
    risk_level, advice = None, None  # 기본 위험 정보

    # 기본 지도 표시
    real_time_map = folium.Map(location=[lat, lon], zoom_start=6, tiles="OpenStreetMap")

    # ✅ 지진 데이터를 지도에 HeatMap으로 추가
    if not df_earthquakes.empty:
        heat_data = df_earthquakes[['lat', 'lon', 'magnitude']].values.tolist()  # [위도, 경도, 규모]
        if heat_data:  # 데이터가 비어있지 않은지 확인
            HeatMap(heat_data, radius=12, blur=6, min_opacity=0.4).add_to(real_time_map)

    # 지도 표시
    st_folium(real_time_map, height=500, width=700)

    if address:
        lat, lon = get_lat_lon_from_address(address)

        # 좌표가 정상적으로 반환되지 않으면 기본 좌표 사용
        if lat is None or lon is None:
            st.error("❌ 주소를 찾을 수 없습니다. 올바른 주소를 입력하세요.")
            lat, lon = 36.5, 127.8  # 기본 좌표 유지 (에러 방지)
        else:
            prob = predict_earthquake(lat, lon)  # 예측 실행
            risk_level, advice = get_risk_level(prob)

            # 사용자 위치 마커 추가
            folium.Marker([lat, lon], popup=f"📍 {address}", icon=folium.Icon(color="red")).add_to(real_time_map)

            # 지도 위치 변경
            real_time_map.location = [lat, lon]  # 입력한 주소로 지도의 위치를 변경
            real_time_map.zoom_start = 10  # 지도 확대

            # 세션 상태에 저장
            st.session_state.lat = lat
            st.session_state.lon = lon

        # 예측 결과
        st.write("### 📊 예측 결과")
        if prob is not None:
            st.write(f"### 🔥 예상 지진 발생 확률: `{prob}%`")
            st.write(f"### ⚡ 위험 등급: `{risk_level}`")
            st.write(f"### 📢 유의사항: {advice}")
        else:
            st.write("🔍 위치를 입력하면 자동으로 예측이 실행됩니다.")

        # 최종 업데이트된 지도 표시
        st_folium(real_time_map, height=500, width=700)
    else:
        st.write("🔍 위치를 입력하면 자동으로 예측이 실행됩니다.")
