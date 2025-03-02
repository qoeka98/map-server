# map-server

# 🌍 실시간 지진 예측 및 대비 시스템

🖼️ 주소 : https://map-server-nhsbkeeeqvtfksaqee9d65.streamlit.app/

## 📑 프로젝트 개요
본 프로젝트는 **실시간 지진 예측 및 대비 시스템**을 구축하여 사용자가 지진 위험에 대비할 수 있도록 지원합니다. 실시간으로 지진 데이터를 수집하고, 예측 모델을 통해 지진 발생 가능성을 평가하며, 안전한 대피소를 안내하는 것을 목표로 합니다.

---

## 🚀 주요 기능

### 1. 📊 실시간 지진 예측 시스템 (eda.py, new.py)

- 지진 발생 가능성 예측: 사용자가 입력한 위치의 지진 발생 가능성을 실시간으로 예측합니다.

- 데이터 수집: USGS API를 통해 실시간 지진 데이터를 수집하며, 과거 1년간의 데이터를 결합하여 위험 지역을 시각화합니다.

- 모델 활용: Random Forest 모델을 사용하여 지진 발생 확률을 예측합니다.

- 시각화 기능: folium을 이용하여 위험 지역을 HeatMap으로 표시하고, 주요 국가의 지진 위험도를 시각화하여 글로벌 위험도를 제공합니다.

## 2. 🛠️ 지진 대비 대피소 안내 시스템 (deapo.py, deabi.py)

- 복수 API 활용: 두 개의 대피소 API (DSSP-IF-00706, DSSP-IF-10941)를 사용하여 기존 대피소 정보와 신규 대피소 정보를 모두 제공합니다.

- 사용자 위치 기반 추천: geopy를 사용해 사용자의 위치와 대피소 간의 거리를 계산하여 최적의 대피소를 추천합니다.

- 지도 및 목록 표시: folium을 사용해 지도에 대피소 위치를 마커로 표시하고, st.data_editor를 통해 대피소 목록을 테이블 형태로 제공합니다.

- 상세 정보 제공: 대피소의 이름, 주소, 거리 정보를 상세하게 제공하여 사용자가 신속하게 대피소를 찾을 수 있도록 지원합니다.

## 3. 💬 AI 기반 지진 대비 상담 챗봇 (snagdam.py)

- AI 모델 사용: Hugging Face의 google/gemma-2-9b-it 모델을 사용하여 AI 챗봇을 구현.

- 자연어 처리(NLP): 사용자가 지진 대비, 대피 요령, 내진 설계, 지진 예측 기술 등에 대한 질문을 하면 최적의 답변을 제공합니다.

- 입력 처리: clean_input, is_earthquake_related 함수를 통해 사용자 입력을 필터링하며, st.session_state를 사용해 채팅 기록을 유지합니다.

## 4. 📰 실시간 지진 뉴스 제공 시스템 (news.py)

- 다중 뉴스 소스 통합: 네이버 뉴스 검색 및 구글 뉴스 RSS 피드를 활용하여 최신 지진 뉴스를 실시간으로 제공합니다.

- 데이터 처리: BeautifulSoup을 사용하여 네이버 뉴스에서 HTML 데이터를 크롤링하고, feedparser를 통해 구글 뉴스의 RSS 데이터를 가공합니다.

- 최신 뉴스 정렬: datetime 모듈을 사용해 날짜를 변환하고, 최신 순으로 정렬하여 사용자에게 제공합니다.

오류 처리: API 요청 실패 시 사용자에게 명확한 오류 메시지를 표시합니다.
---

## 📊 머신러닝 모델 학습 및 성능 비교
### 1. 초기 KNN 모델 학습
- **정확도:** 0.9218
- **작은 지진 재현율 (Recall):** 0.46
- **혼동 행렬 분석:** 작은 지진을 큰 지진으로 잘못 예측한 사례가 15개 발생

```
✅ KNN 모델 정확도: 0.9218

📊 분류 보고서:
              precision    recall  f1-score   support

           0       0.76      0.46      0.58        28
           1       0.93      0.98      0.96       215

    accuracy                           0.92       243
   macro avg       0.85      0.72      0.77       243
weighted avg       0.91      0.92      0.91       243

🧮 혼동 행렬:
[[ 13  15]
 [  4 211]]
```

### 2. Oversampling 모델 성능
- **정확도:** 0.5609
- 데이터 불균형을 해소했지만 모델의 전체 성능은 저하됨

```
✅ Oversampling 모델 정확도: 0.5609

📊 분류 보고서:
              precision    recall  f1-score   support

           0       0.55      0.71      0.62       136
           1       0.58      0.41      0.48       135

    accuracy                           0.56       271
   macro avg       0.57      0.56      0.55       271
weighted avg       0.57      0.56      0.55       271

🧮 혼동 행렬:
[[96 40]
 [79 56]]
```

### 3. Random Forest 최종 모델
- **정확도:** 0.8044
- 작은 지진과 큰 지진을 모두 안정적으로 예측

```
✅ Random Forest 모델 정확도: 0.8044

📊 분류 보고서:
              precision    recall  f1-score   support

           0       0.83      0.77      0.80       136
           1       0.78      0.84      0.81       135

    accuracy                           0.80       271
   macro avg       0.81      0.80      0.80       271
weighted avg       0.81      0.80      0.80       271

🧮 혼동 행렬:
[[105  31]
 [ 22 113]]
```

- 학습된 모델은 `earthquake_model.joblib`으로 저장되어 Streamlit 앱에서 실시간 예측에 활용되었습니다.

---

🛠️ 설치 및 실행 방법

1. 환경 설정

# 필요한 패키지 설치
pip install -r requirements.txt

2. Streamlit 앱 실행

streamlit run app.py

3. 웹 브라우저에서 접속

http://localhost:8501

📂 파일 및 디렉터리 구조
```bash
📦 map-server
├─ .streamlit/
│   └─ secrets.toml          # API 키 및 보안 설정 관리
├─ app.py                    # 메인 앱 실행 및 메뉴 구성
├─ eda.py                    # 지진 예측 및 위험 지역 분석
├─ new.py                    # 실시간 데이터 활용 예측 기능
├─ deapo.py                  # 대피소 정보 수집 및 지도 표시
├─ deabi.py                  # 지진 대비 시스템 기능
├─ snagdam.py                # AI 챗봇 기능 구현
├─ news.py                   # 실시간 지진 뉴스 크롤링
├─ requirements.txt          # 필요한 Python 라이브러리 목록
└─ earthquake_model.joblib   # 학습된 머신러닝 모델 파일


```

🔒 보안 및 최적화

API 키 관리: API 키와 토큰은 secrets.toml 파일에 저장하고, st.secrets.get() 메서드를 사용하여 안전하게 불러옴.

성능 최적화: st.cache_data를 활용해 API 호출을 캐싱하여 성능을 최적화.

오류 처리: 모든 API 호출과 데이터 처리 시 예외 처리를 통해 안정성을 높였습니다.

데이터 캐싱: Streamlit의 @st.cache_data를 사용하여 데이터 로딩 속도를 개선하고 API 사용량을 줄였습니다.


---

## 개발자 이메일📧 :  vhzkflfltm6@gmail.com


