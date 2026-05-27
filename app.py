import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="🎧 무드&비트 음악 평론 챗봇", page_icon="🎵")
st.title("🎧 무드&비트 음악 평론 챗봇")
st.caption("피치포크, 리드머, 이즘, RYM 스타일의 깊이 있는 음악 평론을 제공합니다.")

# 2. Streamlit Secrets에서 API 키 불러오기 및 설정
if "GEMINI_API_KEY" not in st.secrets:
    st.error("지정된 GEMINI_API_KEY를 Secrets에서 찾을 수 없습니다. 설정 확인이 필요합니다.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. 세션 상태(Chat History 및 Gemini Chat 세션) 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 가장 중요: 닫히지 않는 공식 Gemini Chat 세션을 Streamlit 세션에 저장
if "gemini_chat" not in st.session_state:
    system_instruction = (
        "당신은 피치포크(Pitchfork), 온음, 리드머, 이즘(IZM), ResMusica, Rate Your Music(RYM), Overtone 등 "
        "국내외 유수의 음악 매체 스타일을 꿰뚫고 있는 전문 음악 평론가입니다. "
        "사용자가 음악, 앨범, 아티스트에 대해 물어보면 단순히 정보를 나열하는 것을 넘어, "
        "사운드적 특징, 문화적 맥락, 앨범의 서사적 구조, 프로덕션을 날카롭고 유려한 문체로 평론해주세요. "
        "피치포크식 소수점 평점이나 리드머식 별점 등을 덧붙여도 좋습니다."
    )
    # 모델 선언 및 채팅 세션 시작 (system_instruction 주입)
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        system_instruction=system_instruction
    )
    # 한 번 연결하면 계속 유지되는 대화방(chat)을 생성합니다.
    st.session_state.gemini_chat = model.start_chat(history=[])

# 4. 이전 대화 기록 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 처리
if user_input := st.chat_input("아티스트, 앨범, 혹은 곡 이름을 입력하고 평론을 요청해보세요!"):
    
    # 사용자 메시지 화면 표시 및 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 6. Gemini 모델 호출 및 답변 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            with st.spinner("평론가가 대상을 분석 중입니다... ✍️"):
                # 기존의 복잡한 변환 없이, 유지되고 있는 세션에 메시지만 새로 보냅니다.
                response = st.session_state.gemini_chat.send_message(user_input)
                full_response = response.text
                
            # 결과 출력 및 저장
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # 오류 처리 및 상세 내용 출력
            error_msg = f"❌ 오류가 발생했습니다: {str(e)}\n\n문제가 지속되면 새로고침(F5) 후 다시 시도해 주세요."
            message_placeholder.error(error_msg)
