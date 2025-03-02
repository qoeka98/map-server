import streamlit as st

def run_home():
    # 스타일 적용
    st.markdown(
        """
        <style>
            body {
                background-color: #f8f9fa;
            }
            .title-container {
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(135deg, #1976d2, #42a5f5);
                color: white;
                border-radius: 12px;
                box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
                margin-bottom: 30px;
            }
            .title-container h1 {
                font-size: 38px;
                font-weight: bold;
                margin-bottom: 10px;
                animation: glow 1.5s infinite alternate;
            }
            @keyframes glow {
                0% { text-shadow: 0 0 5px #ffffff; }
                100% { text-shadow: 0 0 20px #00e5ff; }
            }
            .title-container p {
                font-size: 18px;
                opacity: 0.9;
            }
            .warning-box {
                background-color: #ffe0e0;
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0px 4px 10px rgba(255, 0, 0, 0.2);
                font-size: 18px;
                margin-bottom: 30px;
            }
            .warning-box h3 {
                color: #b71c1c;
                font-size: 22px;
                margin-bottom: 10px;
            }
            .video-container {
                display: flex;
                justify-content: center;
                flex-direction: column;
                align-items: center;
                padding: 20px;
                background-color: white;
                border-radius: 12px;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
                margin-bottom: 30px;
            }
            .video-title {
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 10px;
                text-align: center;
                color: #64b5f6;
            }
            .footer {
                text-align: center;
                font-size: 16px;
                color: #555;
                margin-top: 20px;
            }
            .footer a {
                color: #007bff;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    

    st.write("API_KEY_1:", st.secrets.get("API_KEY_1"))
    st.write("API_KEY_2:", st.secrets.get("API_KEY_2"))

    st.markdown(
        """
        <div class='title-container'>
            <h1>🌍 지진 예측 및 대비</h1>
            <p>지진은 예고 없이 찾아옵니다. 올바른 대비로 생명을 보호하세요.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    # 경고 메시지 박스
    st.markdown(
        """
        <div class='warning-box'>
            <h3>⚠️ 지진은 언제든지 발생할 수 있습니다!</h3>
            <p>지진이 발생하면 순식간에 심각한 피해를 초래할 수 있습니다.<br>
               아래 영상을 통해 지진의 위험성과 올바른 대비 방법을 익혀보세요.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 비디오 컨테이너
    st.markdown("""
        <div class='video-container'>
            <div class='video-title'>📽️ 간단 소개 영상</div>
    """, unsafe_allow_html=True)
    st.video("지진위험.mp4")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 출처 링크 스타일 추가
    st.markdown(
        """
        <div class='footer'>
            🎬 동영상 출처: <a href='https://ai.invideo.io/watch/q1dc72Fu_jh'>인비디오 AI</a>
        </div>
        """,
        unsafe_allow_html=True
    )
