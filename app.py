import streamlit as st
from streamlit_option_menu import option_menu

from deabi import run_deabi
from deapo import run_deapi
from eda import run_eda
from home import run_home
from jijin import run_jijin
from map import run_map
from new import run_new
from snagdam import run_sangdam

def main():
    # ✅ Streamlit Option Menu 사
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
            options=["🏠 홈", "🔍 지진 예측", "대비 방법 및 상담","앱개발과정"],
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
        run_jijin()
    
   
    elif menu == "대비 방법 및 상담":
        run_deabi()

    elif menu == "앱개발과정":
        run_map()
  
      

# ✅ 실행
if __name__ == "__main__":
    main()
