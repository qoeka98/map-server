import streamlit as st

def run_map():
    st.title("앱개발과정")

    st.markdown('''
## 📱 앱 개발 과정: 실시간 지진 예측 및 대비 시스템

### 1. 프로젝트 개요
본 프로젝트는 **실시간 지진 예측 및 대비 시스템**을 구축하는 것을 목표로 진행되었습니다. 사용자가 실시간으로 지진 관련 정보를 확인하고, 예측 모델을 통해 지진 발생 가능성을 평가하며, 안전한 대피소를 안내받을 수 있도록 설계되었습니다.

---

### 2. 데이터 수집 및 처리
- **실시간 데이터 수집:** USGS(미국 지질 조사소) API를 사용하여 규모 4.5 이상의 지진 데이터를 실시간으로 수집했습니다. (`new.py`, `eda.py`)
- **자동 CSV 파일 생성:** API에서 실시간 데이터를 받아와 CSV 파일로 저장하는 기능을 구현하여, 데이터 갱신 시 자동으로 최신 데이터가 반영되도록 설정하였습니다.
- **데이터 전처리:** 실시간으로 수집된 데이터를 `pandas`를 이용해 정리하고, 지진의 발생 위치, 규모, 깊이 등의 중요한 정보를 가공하여 모델에 입력할 수 있도록 준비했습니다.

---

### 3. 머신러닝 모델 학습
#### 🔍 초기 KNN 모델 학습
- 초기에는 KNN 알고리즘을 사용하여 지진 예측 모델을 구축했습니다.
- 정확도는 0.9218로 높았지만, 클래스 0(작은 지진)의 재현율이 0.46으로 매우 낮아 큰 지진만을 예측하는 경향이 있었습니다.

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

#### 🔄 Oversampling 기법 적용
- 데이터 불균형 문제를 해결하기 위해 작은 지진 샘플을 Oversampling하여 데이터의 균형을 맞췄습니다.
- 그러나 모델의 정확도가 0.5609로 크게 감소하여 다른 모델로의 전환이 필요했습니다.

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

#### 🌲 Random Forest 모델 최종 채택
- 최종적으로 Random Forest 모델을 활용하여 예측 성능을 개선하였습니다.
- 모델의 정확도는 0.8044로, 작은 지진과 큰 지진 모두 안정적으로 예측할 수 있었습니다.

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

### 4. 주요 기능 구현
#### 1) 🌍 **실시간 지진 예측 시스템** 
- 사용자가 입력한 위치의 지진 발생 가능성을 실시간으로 예측합니다.
- 과거 1년간의 지진 데이터와 실시간 수집 데이터를 결합하여 위험 지역을 시각화합니다.
- `folium` 라이브러리를 사용하여 HeatMap을 표시하고, 주요 국가의 지진 위험도를 분석하여 시각적으로 보여줍니다.
- 예측 모델은 `Nominatim API`를 통해 주소를 좌표로 변환하여 예측에 활용하였습니다.

#### 2) 🛠️ **지진 대비 시스템** 
- 두 개의 대피소 API (`DSSP-IF-00706`, `DSSP-IF-10941`)를 사용하여 기존 대피소 정보뿐만 아니라 통합 대피소 정보를 제공할 수 있었습니다.
- `geopy` 라이브러리를 사용해 사용자의 위치와 대피소 위치 간의 거리를 계산하고, `folium`으로 지도를 만들어 최적의 대피소를 시각적으로 표시하였습니다.
- `st.data_editor`를 통해 대피소의 상세 주소와 거리 정보를 데이터 테이블 형태로 제공하여 사용자가 빠르게 정보를 확인할 수 있도록 했습니다.

#### 3) 💬 **AI 챗봇 기능**
- Hugging Face의 `google/gemma-2-9b-it` 모델을 사용하여 AI 챗봇을 구현하였습니다.
- 프롬프트 예시: "너는 지진 대비 및 자연재해 전문가 AI야. 사용자가 지진 대비, 대피 요령, 내진 설계, 지진 예측 기술에 대해 질문하면 최적의 답변을 제공해줘."
- 사용자 함수를 통해 입력시, 지진 관련 질문만 필터링하도록 구현했습니다다.
- **챗봇의 템퍼러쳐(temperature)는 1.3로 설정하여** 상황에 따른 적절한 답변을 제공하도록 했습니다. 템퍼러쳐가 0이면 자연재해에 대한 답변을 제공하지만 특정 유연성이 필요한 질문은 대답을 잘 하지 못했으며, 2는 답변의 정확성을 떨어뜨리므로 1.5로 설정하여 **상황에 맞는 답변을 제공**할 수 있도록 조정했습니다.
- `st.session_state`를 사용해 채팅 기록을 유지하도록 구현하였습니다.
                
#### 4) 📰 **실시간 지진 뉴스**
- 네이버 뉴스 검색 및 구글 뉴스 RSS 피드를 활용하여 최신 지진 뉴스를 실시간으로 제공합니다.
- `BeautifulSoup`을 사용하여 네이버 뉴스에서 HTML 데이터를 정제하고, `feedparser`를 통해 구글 뉴스의 RSS 데이터를 가공하였습니다.
- 뉴스 기사는 `datetime` 모듈을 사용해 날짜를 변환하고 최신 순으로 정렬하여 사용자에게 가장 최신 정보를 빠르게 제공할 수 있도록 구성하였습니다.

---

### 5. 배포 및 보안 설정
- 최종 앱은 Streamlit을 통해 배포하였으며, `requirements.txt` 파일을 사용하여 필요한 라이브러리를 손쉽게 설치할 수 있도록 했습니다.
- API 키와 토큰은 `secrets.toml` 파일에 저장하고, `st.secrets.get` 메서드를 사용하여 안전하게 불러오도록 구현했습니다.
- API 호출 시 `st.cache_data`를 사용하여 호출 빈도를 줄여 성능을 최적화했습니다.

이와 같은 과정을 통해 **실시간 지진 예측 및 대비 시스템**을 개발하였으며, 이를 통해 사용자가 지진에 보다 안전하게 대비할 수 있도록 돕는 것을 목표로 삼았습니다.


''')