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
        "1. **전문성과 깊이**:
