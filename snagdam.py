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
                background-color: #d4f8c4; /* 연두색 */
                padding: 10px;
                border-radius: 12px;
                margin-bottom: 10px;
                font-weight: bold;
                max-width: 80%;
            }
            .ai-message {
                background-color: #fff5cc; /* 연한 노란색 */
                padding: 10px;
                border-radius: 12px;
                margin-bottom: 10px;
                max-width: 80%;
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

    # ✅ 예시 질문 표시
    with st.expander("💡 예시 질문 보기"):
        st.markdown(
            """
            - 최근 지진 정보는 어디서 확인할 수 있나요?
            - 지진 발생 시 가장 안전한 장소는?
            - 지진 대비를 위해 어떤 물품을 준비해야 하나요?  
            - 내진 설계가 중요한 이유는 무엇인가요? 
            - 쓰나미 경보가 발령되면 어떻게 대처해야 하나요? 
            """,
            unsafe_allow_html=True
        )

    token = get_huggingface_token()
    client = InferenceClient(model="google/gemma-2-9b-it", api_key=token)

    # ✅ 기존 채팅 기록 유지
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요! 지진 대비 챗봇입니다. 궁금한 점을 물어보세요!"}
        ]

    # ✅ 기존 채팅 기록 표시 (프로필 아이콘 추가)
    for message in st.session_state.messages:
        role = message["role"]
        message_content = message["content"]

        if role == "user":
            icon_url = "https://cdn-icons-png.flaticon.com/512/1144/1144760.png"  # 사용자 아이콘
            message_class = "user-message"
        else:
            icon_url = "https://cdn-icons-png.flaticon.com/512/4712/4712034.png"  # AI 아이콘
            message_class = "ai-message"

        st.markdown(
            f"""
            <div class="chat-container">
                <img src="{icon_url}" class="chat-icon">
                <div class="{message_class}">{message_content}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ✅ 사용자 입력 받기 (고유한 key 값 추가)
    chat = st.chat_input("지진 관련 질문을 입력하세요!", key="chat_input")

    if chat:
        clean_chat = clean_input(chat)

        if not is_earthquake_related(clean_chat):
            response = "❌ 죄송합니다. 지진 관련 상담만 가능합니다."
        else:
            # ✅ AI 응답 요청 (Gemma 모델 사용)
            system_prompt = (          
                '''너는 지진 대비 및 자연재해 전문가 AI야.  
너의 역할은 사용자에게 **지진 대비, 대피 요령, 긴급 상황 행동 지침, 내진 설계, 지진 예측 기술, 심리적 대처 방법**에 대한 정보를 제공하는 것이야.  
다음과 같은 원칙을 준수해야 해:

1️⃣ **지진 발생 전**:
   - 지진 대비를 위해 사전에 준비해야 할 필수 물품(비상식량, 응급 키트 등)을 설명해.
   - 내진 설계가 중요한 이유와 내진 성능이 뛰어난 건물의 특징을 설명해.
   - 가정과 직장에서 가장 안전한 대피 장소를 안내해.
   - 지진 발생 시 가족과의 연락 방법 및 대피 계획을 수립하는 방법을 설명해.

2️⃣ **지진 발생 시**:
   - 실내와 실외에서 지진 발생 시 행동 요령을 구체적으로 안내해.
   - 높은 건물 안에 있을 경우, 차량을 운전 중일 경우, 해안가에 있을 경우 등 다양한 상황에 맞는 대처법을 제공해.
   - 엘리베이터 사용 금지, 문을 열어 출구 확보 등의 중요성을 강조해.

3️⃣ **지진 발생 후**:
   - 추가적인 여진에 대비하는 방법을 설명해.
   - 무너진 건물에 갇혔을 경우 대처법(구조 요청 방법, 공기 확보, 체온 유지 등)을 안내해.
   - 재난 이후 안전한 지역으로 이동하는 방법과 정부 지원을 받을 수 있는 방법을 설명해.

4️⃣ **쓰나미 대처**:
   - 해안 지역에서 지진 발생 시 쓰나미 위험 여부를 확인하는 방법을 알려줘.
   - 쓰나미 경보가 발령될 경우 즉시 이동해야 하는 안전한 장소를 안내해.
   - 높은 지대로 신속히 대피하는 방법과 대피소 정보를 제공해.

5️⃣ **기타**:
   - 최근 발생한 주요 지진과 그로 인한 피해 사례를 언급할 수 있어.
   - 심리적 불안을 겪는 사람들에게 지진 이후 스트레스를 극복하는 방법을 안내해.
   - 한국과 세계 각국의 지진 대비 정책이나 대피소 운영 시스템을 소개할 수 있어.
'''
      
                '''너는 지진 대비 및 자연재해 전문가 AI야.  
너의 역할은 사용자에게 **지진 대비, 대피 요령, 긴급 상황 행동 지침, 내진 설계, 지진 예측 기술, 심리적 대처 방법**에 대한 정보를 제공하는 것이야.  
'''
            )
            full_prompt = system_prompt + "\n\n" + clean_chat

            response = client.text_generation(prompt=full_prompt, max_new_tokens=520)

        # ✅ 채팅 기록 추가
        st.session_state.messages.append({"role": "user", "content": clean_chat})
        st.session_state.messages.append({"role": "assistant", "content": response})

        # ✅ 사용자 메시지 표시
        st.markdown(
            f"""
            <div class="chat-container">
                <img src="https://cdn-icons-png.flaticon.com/512/1144/1144760.png" class="chat-icon">
                <div class="user-message">{clean_chat}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ✅ AI 응답 메시지 표시
        st.markdown(
            f"""
            <div class="chat-container">
                <img src="https://cdn-icons-png.flaticon.com/512/4712/4712034.png" class="chat-icon">
                <div class="ai-message">{response}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
