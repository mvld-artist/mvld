import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="Music Critic AI", page_icon="🎵", layout="centered")
st.title("🎵 음악 평론 챗봇: Critic AI")
st.caption("Pitchfork, Rate Your Music, 리드머, 온음 등의 스타일로 앨범을 깊이 있게 평론합니다.")

# 2. Streamlit Secrets에서 API 키 불러오기 및 클라이언트 초기화
try:
    # Streamlit Cloud 환경 또는 local의 .streamlit/secrets.toml에서 키를 가져옵니다.
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("API 키를 찾을 수 없습니다. Streamlit Secrets에 'GEMINI_API_KEY'를 설정해주세요.")
    st.stop()

# 3. 세션 상태(Session State) 초기화 (채팅 기록 및 대화 객체 유지)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    # 챗봇의 페르소나를 부여하는 시스템 지침(System Instruction) 설정
    system_instruction = (
        "당신은 전 세계의 다양한 음악 평론 매체(Pitchfork, Rate Your Music(RYM), 리드머, 온음, IZM, ResMusica 등)의 "
        "장점을 흡수한 전문 음악 평론가입니다. 사용자가 특정 앨범이나 아티스트, 곡을 언급하면 다음과 같은 원칙으로 평론을 진행하세요.\n\n"
        "1. **전문성과 깊이**: 단순히 '좋다/나쁘다'를 넘어 사운드 엔지니어링, 프로덕션, 노랫말의 서사, 음악사적 맥락을 짚어내세요.\n"
        "2. **비평적 시각**: 무조건적인 찬양은 지양하며, 아쉬운 점이나 한계도 날카롭게 지적하세요.\n"
        "3. **매체별 스타일 융합**: Pitchfork 특유의 세련되고 힙한 분석, RYM의 장르적 마니아성, 리드머/온음 등 국내 평론지의 텍스트적 깊이를 조합하세요.\n"
        "4. **가상의 평점 제공**: 평론 마지막에는 해당 앨범에 대한 가상의 평점(10점 만점 또는 별점 5점 만점)과 한 줄 평을 반드시 포함하세요."
    )
    
    # gemini-2.5-flash-lite 모델로 대화 세션 시작
    try:
        st.session_state.chat_session = client.chats.create(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
        )
    except Exception as e:
        st.error(#요류 발생 시 메시지
            f"Gemini 모델 초기화 중 오류가 발생했습니다: {e}"
        )
        st.stop()

# 4. 기존 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 처리
if user_input := st.chat_input("평론을 원하는 앨범이나 아티스트를 입력하세요. (예: 켄드릭 라마 - To Pimp a Butterfly)"):
    # 사용자 메시지 화면에 표시 및 세션 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 챗봇 답변 생성 및 에러 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🎵 앨범을 분석하고 평론을 작성하는 중입니다...")
        
        try:
            # API 호출
            response = st.session_state.chat_session.send_message(user_input)
            full_response = response.text
            
            # 결과 출력 및 세션 저장
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except APIError as e:
            # Gemini API 관련 에러 처리
            error_msg = f"Gemini API 오류가 발생했습니다: {e.message}"
            message_placeholder.markdown(error_msg)
            st.error(error_msg)
        except Exception as e:
            # 기타 일반 에러 처리
            error_msg = f"알 수 없는 오류가 발생했습니다: {str(e)}"
            message_placeholder.markdown(error_msg)
            st.error(error_msg)
