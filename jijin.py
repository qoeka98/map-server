import streamlit as st

from eda import run_eda
from new import run_new



# ✅ 메인 실행 함수
def run_jijin():
    st.title("🌍 지진 예측 및 위험 지역 분석")

    # 📌 **탭 UI 적용**
    tab1, tab2 = st.tabs([ "🌍 위험 지역 분석","📊 지진 예측"])

    with tab1:
        run_new()

    with tab2:
        run_eda()
        

# 실행
if __name__ == "__main__":
    run_jijin()
