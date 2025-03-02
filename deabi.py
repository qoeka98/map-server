import streamlit as st

from deapo import run_deapi
from news import run_news
from snagdam import run_sangdam

def run_deabi():
    st.markdown("""
        <style>
            .content-box {
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                margin: 20px 0;
            }
            .danger {
                color: red;
                font-weight: bold;
            }
            .safe {
                color: green;
                font-weight: bold;
            }
            .important {
                color: orange;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("🛠️ 지진 대비 시스템")
    
    # 📌 **각 탭 설명 추가**
    st.markdown("""
    ### 🔍 사용 안내
    - **🏠 지진 대비**: 지진의 원인과 위험성, 기본 대비 방법, 긴급 행동 요령을 제공합니다.
    - **🛑 대피경로**: 현재 위치 또는 입력한 지역을 기반으로 가장 가까운 대피소 정보를 제공합니다.
    - **💬 상담**: 지진 대비 및 재난 시 대처 방법에 대한 전문가 상담을 받을 수 있습니다.
    - **📰 실시간 뉴스**: 최신 지진 관련 뉴스 및 재난 정보를 실시간으로 확인할 수 있습니다.
    """)

    # 📌 **탭 방식 UI**
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 지진 대비", "🛑 대피경로", "💬 상담", "📰 실시간 뉴스"])

    with tab1:
        st.header("🌍 지진이란?")
        st.markdown("""
        **지진**은 지각이 단층을 따라 갑작스럽게 움직이며 발생하는 **자연 재해**입니다.  
        주로 **지구 내부의 판 구조 운동, 화산 활동, 인공 폭발** 등으로 발생하며,  
        큰 규모의 지진은 **<span class='danger'>🔥 화재, 🌊 쓰나미, 🏠 건물 붕괴</span>** 등 심각한 피해를 초래할 수 있습니다.
        """, unsafe_allow_html=True)

        # 📺 **지진 관련 동영상**
        st.info("간단한 영상 : [지진은 왜 위험한가?]")
        st.video("지진왜위험할까.mp4")

        st.markdown("<h2 class='danger'>⚠️ 지진의 위험성</h2>", unsafe_allow_html=True)
        st.markdown("""
        - 🏠 **건물 붕괴** → <span class='danger'>노후 건물은 위험!</span> 내진 설계 부족 시 붕괴 가능성이 큽니다.
        - 🌊 **쓰나미** → 해저 지진 발생 시 **<span class='danger'>몇 분 안에 쓰나미 도착!</span>** 즉시 높은 곳으로 대피해야 합니다.
        - 🔥 **화재 발생** → **<span class='danger'>가스관 파손</span>** 및 **전기 합선**으로 불이 번질 위험이 있습니다.
        - 🚧 **도로 및 교량 파손** → 대피 경로 차단 가능성.
        - 🚗 **교통 마비** → **<span class='danger'>교통이 마비될 가능성이 높음!</span>**
        """, unsafe_allow_html=True)

        # 📌 **기본 대비 사항**
        st.markdown("""
            <div class='content-box'>
                <h3>📌 <span class='safe'>기본 대비 사항</span></h3>
                <ul>
                    <li>🏠 <b>긴급 대피 경로 확인</b>: 집, 학교, 직장에서 가장 빠른 대피 경로를 확인하고, 가족과 함께 훈련하세요.</li>
                    <li>🎒 <b>비상 용품 준비</b>: 최소 72시간을 버틸 수 있는 <span class='safe'>물, 식량, 손전등, 구급약</span>을 준비하세요.</li>
                    <li>📞 <b>가족과 연락 방법 정하기</b>: <span class='important'>전화가 불통될 가능성이 높음!</span> 문자/SNS 활용 대비.</li>
                    <li>📻 <b>재난 방송 수신 설정</b>: <span class='safe'>국가재난안전포털, 라디오</span> 필수!</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        # 🚨 **긴급 대비 사항**
        st.markdown("""
            <div class='content-box'>
                <h3>🚨 <span class='danger'>긴급 대비 사항</span></h3>
                <ul>
                    <li>⚠️ <b>지진 발생 시 안전한 장소로 대피</b>: <span class='safe'>책상 아래, 기둥 옆, 튼튼한 가구 밑</span> 등으로 이동하세요.</li>
                    <li>🔥 <b>가스 및 전기 차단</b>: <span class='danger'>화재 예방을 위해 신속히 차단!</span></li>
                    <li>🚪 <b>출구 확보</b>: 문이 변형될 수 있으므로 **출구를 확보하세요!**</li>
                    <li>🚨 <b>대피 시 엘리베이터 사용 금지</b>: <span class='danger'>💀 갇힘 사고 위험!</span> 계단 이용 필수.</li>
                    <li>🌳 <b>야외에서는 개방된 공간으로 이동</b>: <span class='safe'>건물과 전신주에서 멀리 떨어지세요!</span></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with tab2:
        run_deapi()  # ✅ `run_deapi()` 실행 (대피소 검색)

    with tab3:
        run_sangdam()  # ✅ `run_sangdam()` 실행 (상담 기능)

    with tab4:
        run_news()  # ✅ `run_news()` 실행 (실시간 뉴스)

if __name__ == "__main__":
    run_deabi()
