import streamlit as st
from streamlit_option_menu import option_menu
from eda import run_eda
from home import run_home
from new import run_new
from snagdam import run_sangdam

def main():
    # ✅ Streamlit Option Menu 사용
    with st.sidebar:
        st.markdown("""
            <style>
                .sidebar-title {
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                    color: #007bff;
                    padding: 10px 0;
                }
                .sidebar-container {
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 12px;
                }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='sidebar-title'>📌 지진 예측 AI</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-container'>", unsafe_allow_html=True)
        
        menu = option_menu(
            menu_title="메뉴 선택",
            options=["🏠 홈", "🔍 지진 예측", "지진 발생", "상담", "대비 방법", "대피소 위치"],
            icons=["house", "stethoscope", "bar-chart-line", "chat-text", "shield", "phone"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5px"},
                "icon": {"color": "blue", "font-size": "22px"}, 
                "nav-link": {
                    "font-size": "18px",
                    "text-align": "left",
                    "margin": "5px",
                    "padding": "12px",
                    "border-radius": "10px",
                    "transition": "0.3s",
                    "color": "#333",
                },
                "nav-link-selected": {"background-color": "#007bff", "color": "white"},
                "nav-link:hover": {"background-color": "#e9ecef"}  
            }
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ✅ 선택된 메뉴 실행
    if menu == "🏠 홈":
        run_home()
    elif menu == "🔍 지진 예측":
        run_eda()
    elif menu == "지진 발생":
        run_new()
    elif menu == "상담":
        run_sangdam()
    elif menu == "대비 방법":
        st.markdown("""
            <style>
                .content-box {
                    background: white;
                    padding: 20px;
                    border-radius: 12px;
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                    margin: 20px 0;
                }
                .video-box {
                    display: flex;
                    justify-content: center;
                    padding: 20px;
                    background-color: white;
                    border-radius: 12px;
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                    margin-bottom: 30px;
                }
            </style>
        """, unsafe_allow_html=True)
        
        st.title("🛠️ 지진 대비 방법")
        st.info("✅ 지진 발생 전에 미리 대비하는 것이 중요합니다! 재난은 예고 없이 찾아오지만, 준비된 자는 생존할 확률이 높아집니다.")
        
        st.markdown("""
        <div class='content-box'>
            <h3>📌 기본 대비 사항</h3>
            <ul>
                <li>🏠 <b>긴급 대피 경로 확인</b>: 집, 학교, 직장에서 가장 빠른 대피 경로를 확인하고, 가족과 함께 훈련하세요.</li>
                <li>🎒 <b>비상 용품 준비</b>: 최소 72시간을 버틸 수 있는 물, 비상식량, 손전등, 구급약품, 개인용 위생용품(마스크, 손 세정제 등)을 준비하세요.</li>
                <li>📞 <b>가족과의 연락 방법 정하기</b>: 지진 발생 시 전화가 불통될 수 있으므로, 문자나 SNS 등을 이용한 연락 계획을 수립하세요.</li>
                <li>📻 <b>재난 방송 및 알림 수신 설정</b>: 재난 문자, 라디오, 국가재난안전포털을 통해 실시간 정보를 확인하세요.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='video-box'>
        """, unsafe_allow_html=True)
        st.video("지진대비방법.mp4")
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif menu == "대피소 위치":
        st.title("🏠 대피소 위치 정보")
        st.info("📍 가까운 대피소를 확인하고 미리 알아두세요.")
        st.map()

# ✅ 실행
if __name__ == "__main__":
    main()
