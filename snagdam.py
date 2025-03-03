import streamlit as st
from huggingface_hub import InferenceClient
import re

# ✅ 사용자 입력 필터링 함수
def clean_input(text):
    text = re.sub(r"\b(해줘|알려줘|설명해 줘|말해 줘)\b", "", text, flags=re.IGNORECASE)
    return text.strip()

# ✅ 지진 관련 질문 필터링 함수
def is_earthquake_related(text):
    earthquake_keywords = ["지진", "진도", "진앙", "지진 대비", "쓰나미", "대피소"]
    return any(keyword in text for keyword in earthquake_keywords)

# ✅ Hugging Face API 토큰 가져오기
def get_huggingface_token():
    return st.secrets.get("HUGGINGFACE_API_TOKEN")

# ✅ AI 챗봇 실행 함수
def run_sangdam():
    st.markdown("<h1 style='text-align: center; color: #007bff;'>🌍 지진 대비 AI 챗봇</h1>", unsafe_allow_html=True)

    # ✅ CSS 스타일 추가 (유저와 AI 메시지 구분)
    st.markdown("""
        <style>
            .chat-container {
                display: flex;
                align-items: flex-start;
                margin-bottom: 10px;
            }
            .chat-icon {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                margin-right: 10px;
            }
            .user-message {
                background-color: #d4f8c4;
                padding: 10px;
                border-radius: 12px;
                margin-bottom: 10px;
                font-weight: bold;
                max-width: 80%;
            }
            .ai-message {
                background-color: #fff5cc;
                padding: 10px;
                border-radius: 12px;
                margin-bottom: 10px;
                max-width: 80%;
            }
            .highlight {
                background-color: #e0f7fa;
                padding: 5px;
                border-radius: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

    # ✅ 사용 방법 안내
    st.info(
        """
        🔍 **이 챗봇은 다음 기능을 제공합니다.**  
        - ✅ 실시간 지진 대비 및 안전 대책 제공  
        - ✅ 지진 발생 시 행동 요령 안내  
        - ✅ 내진 설계 및 지진 예측 관련 정보 제공  
        - ✅ 쓰나미 및 긴급 대피소 정보 안내  

        **📝 사용 방법:**  
        1️⃣ 아래 입력창에 질문을 입력하세요.  
        2️⃣ AI가 지진 대비 관련 정보를 제공합니다.  
        3️⃣ 원하는 질문을 반복 입력하여 상담하세요.  
        """
    )

    # ✅ 예시 질문 표시 및 상단 고정
    st.markdown("### 💡 예시 질문 (질문을 클릭하면 자동 입력됩니다)")
    example_questions = [
        "최근 지진 정보는 어디서 확인할 수 있나요?",
        "지진 발생 시 가장 안전한 장소는?",
        "지진 대비를 위해 어떤 물품을 준비해야 하나요?",
        "내진 설계가 중요한 이유는 무엇인가요?",
        "쓰나미 경보가 발령되면 어떻게 대처해야 하나요?"
    ]

    # ✅ 선택된 질문을 저장할 변수 초기화
    if 'selected_question' not in st.session_state:
        st.session_state['selected_question'] = ''

    for question in example_questions:
        if st.button(question):
            st.session_state['selected_question'] = question

    token = get_huggingface_token()
    client = InferenceClient(model="google/gemma-2-9b-it", api_key=token)

    # ✅ 기존 채팅 기록 유지
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요! 지진 대비 챗봇입니다. 궁금한 점을 물어보세요!"}
        ]

    # ✅ 기존 채팅 기록 표시
    for message in st.session_state.messages:
        role = message["role"]
        message_content = message["content"]
        icon_url = "https://cdn-icons-png.flaticon.com/512/1144/1144760.png" if role == "user" else "https://cdn-icons-png.flaticon.com/512/4712/4712034.png"
        message_class = "user-message" if role == "user" else "ai-message"

        st.markdown(f"""
            <div class="chat-container">
                <img src="{icon_url}" class="chat-icon">
                <div class="{message_class}">{message_content}</div>
            </div>
            """, unsafe_allow_html=True)

    # ✅ 사용자 입력 받기
    placeholder_text = st.session_state.get('selected_question', "") or "지진 관련 질문을 입력하세요!"
    chat = st.chat_input("지진 관련 질문을 입력하세요!", key="chat_input", placeholder=placeholder_text)

    if chat:
        clean_chat = clean_input(chat)

        # ✅ AI 응답 요청
        system_prompt = '''
        너는 지진 대비 및 자연재해 전문가 AI야.
        너의 역할은 사용자에게 지진 대비, 대피 요령, 긴급 상황 행동 지침, 내진 설계, 지진 예측 기술, 심리적 대처 방법에 대한 정보를 제공하는 것이야.
        예시 질문에도 답변할 수 있도록 해.
        '''

        full_prompt = system_prompt + "\n\n" + clean_chat
        response = client.text_generation(prompt=full_prompt, max_new_tokens=520)

        # ✅ 채팅 기록 추가
        st.session_state.messages.append({"role": "user", "content": clean_chat})
        st.session_state.messages.append({"role": "assistant", "content": response})
