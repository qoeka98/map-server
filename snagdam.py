import streamlit as st
from huggingface_hub import InferenceClient
import re
import time

# ✅ 사용자 입력 필터링 함수
def clean_input(text):
    text = re.sub(r"\b(해줘|알려줘|설명해 줘|말해 줘)\b", "", text, flags=re.IGNORECASE)
    return text.strip()

# ✅ 지진 관련 질문 필터링 함수
def is_earthquake_related(text):
    earthquake_keywords = ["지진", "진도", "진앙", "지진 대비", "쓰나미", "대처방법","안전","대피소","내진설계","구조 활동","안전수칙","내진 설계","지진예측","지진 대책","지진 안정","지진 대응","키트","응급처치","대피","대피 장소","지진 대처","대비 물품","지진 행동 요령","지진 발생 후","심리적","충격","2차피해","안전한 장소","안전한장소"]   
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

    # ✅ 예시 질문 표시 (답변 수정)
    with st.expander("💡 예시 질문 보기"):

        st.markdown(
            """
            
            -  지진 발생 시 안전한 장소는 어디인가요?
            
            - 지진 발생 후 구조 활동이 이루어질 때, 개인적으로 할 수 있는 안전한 대처 방법은 무엇인가요?
            
            - 지진 대비를 위해 어떤 물품을 준비해야 할까요?
            
            - 내진 설계가 중요한 이유는 무엇인가요?
            
            - 쓰나미 경보가 발령되면 어떻게 대처해야 하나요?
            
            - 지진 후 발생할 수 있는 2차 피해에 대한 대처법은 무엇인가요?
            
            - 지진 발생 후 심리적 충격을 어떻게 극복할 수 있나요?
    
            """, unsafe_allow_html=True
        )

    token = get_huggingface_token()
    client = InferenceClient(model="google/gemma-2-9b-it", api_key=token)

    # ✅ 기존 채팅 기록 유지
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요! 지진 대비 챗봇입니다. 궁금한 점을 물어보세요!"}
        ]

    # ✅ 사용자 입력 받기
    chat = st.chat_input("지진 관련 질문을 입력하세요!")

    if chat:
        clean_chat = clean_input(chat)

        if not is_earthquake_related(clean_chat):
            response = "❌ 죄송합니다. 지진 관련 상담만 가능합니다."
        else:
            # ✅ AI 응답 요청 (Gemma 모델 사용)
            system_prompt = (          
       
    '''너는 지진 대비 및 자연재해 그리고 건축 내진설계 및 안전 전문가 AI야.  
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

 **기타**:
   - 최근 발생한 주요 지진과 그로 인한 피해 사례를 언급할 수 있어.
   - 심리적 불안을 겪는 사람들에게 지진 이후 스트레스를 극복하는 방법을 안내해.
   - 한국과 세계 각국의 지진 대비 정책이나 대피소 운영 시스템을 소개할 수 있어.

6️⃣ **내진 설계 설명**:
   - 내진 설계의 정의와 목적을 설명해.
   - 내진 설계가 적용된 건축물의 주요 특징과 기술을 안내해.
   - 내진 설계가 지진 피해를 줄이는 데 어떻게 도움이 되는지 설명해.

   **지진 발생시 안전한 장소 설명**
   - 지진 발생 시 안전한 장소를 찾는 방법을 설명해.
   - 지진 발생 시 안전한 장소의 조건과 위치를 설명해.
   - 지진 발생 시 안전한 장소에서의 행동 요령을 안내해.

**예시 질문에 대한 대답**:


 "지진 발생 후 구조 활동이 이루어질 때, 개인적으로 할 수 있는 안전한 대처 방법은 무엇인가요?"  
   → 구조 활동이 시작되면, 자신이 안전한 장소에 있어야 하며, **여진**에 대비하고, **구조 요청 방법**을 알아둬야 합니다. 또한, **수분 섭취**와 **체온 유지**가 중요합니다.


 "내진 설계가 중요한 이유는 무엇인가요?"  
   → 내진 설계는 건물의 **안전성**을 확보하고, 지진 발생 시 **건물의 붕괴를 방지**하여 생명과 재산을 보호하는 데 중요한 역할을 합니다.


 "지진 후 발생할 수 있는 2차 피해에 대한 대처법은 무엇인가요?"  
   → 화재, 산사태, **전력망 손상** 등에 대비하려면 **소화기**, **건강 상태 확인**, **안전한 지역으로 대피**하는 것이 중요합니다.
. "지진 발생 후 심리적 충격을 어떻게 극복할 수 있나요?"  
   → 지진 후 심리적 충격을 극복하려면, **심리적 지원**을 받는 것이 중요하며, **스트레스 관리**를 위한 **휴식과 대화**가 필요합니다.

520자 이하로 대답해줘.'''

)


            
            full_prompt = system_prompt + "\n\n" + clean_chat

            # ✅ 스피너로 AI 응답 기다리기
            with st.spinner("AI가 응답 중입니다..."):
                response = client.text_generation(prompt=full_prompt, max_new_tokens=520, temperature=0.13,  
    top_p=0.9,        
    top_k=50)
                time.sleep(2)  # 응답을 기다리는 동안 잠시 지연을 추가할 수 있습니다.

        # ✅ 채팅 기록 추가
        st.session_state.messages.append({"role": "user", "content": clean_chat})
        st.session_state.messages.append({"role": "assistant", "content": response})

    # ✅ 기존 채팅 기록 표시 (역순으로 채팅 기록을 표시)
    for message in st.session_state.messages[::-1]:  # 역순으로 채팅 기록을 표시
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

    # ✅ 자동으로 스크롤 하여 최신 메시지로 이동
    st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
