# app.py

import streamlit as st
import google.generativeai as genai

# ---------------------------------

# 페이지 설정

# ---------------------------------

st.set_page_config(
page_title="AI 음악 평론 챗봇",
page_icon="🎵"
)

st.title("🎵 AI 음악 평론 챗봇")
st.caption("Pitchfork / 리드머 / IZM 감성 기반")

# ---------------------------------

# API KEY

# ---------------------------------

try:
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
except Exception as e:
st.error("Secrets 설정 오류")
st.stop()

# ---------------------------------

# 모델 설정

# ---------------------------------

MODEL_NAME = "gemini-2.5-flash-lite"

try:
model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
st.error(f"모델 로딩 실패: {e}")
st.stop()

# ---------------------------------

# 시스템 프롬프트

# ---------------------------------

SYSTEM_PROMPT = """
너는 전문 음악 평론가다.

스타일 참고:

* Pitchfork
* 리드머
* IZM
* 온음
* RYM

답변 규칙:

1. 장르 분석 포함
2. 믹싱/사운드 설명
3. 감정선 설명
4. 단순 칭찬 금지
5. 필요하면 비판 가능
6. 평점은 10점 만점
   """

# ---------------------------------

# 채팅 기록

# ---------------------------------

if "messages" not in st.session_state:
st.session_state.messages = []

# 이전 메시지 출력

for message in st.session_state.messages:
with st.chat_message(message["role"]):
st.markdown(message["content"])

# ---------------------------------

# 입력창

# ---------------------------------

user_input = st.chat_input("앨범, 곡, 아티스트 입력")

if user_input:

```
# 사용자 메시지 저장
st.session_state.messages.append({
    "role": "user",
    "content": user_input
})

# 사용자 메시지 출력
with st.chat_message("user"):
    st.markdown(user_input)

# 대화 합치기
conversation = SYSTEM_PROMPT + "\n\n"

for msg in st.session_state.messages:
    role = "사용자" if msg["role"] == "user" else "평론가"
    conversation += f"{role}: {msg['content']}\n"

# AI 응답
try:
    with st.chat_message("assistant"):

        with st.spinner("평론 작성 중..."):

            response = model.generate_content(
                conversation,
                generation_config={
                    "temperature": 0.9,
                    "max_output_tokens": 1000,
                    "top_p": 0.95
                }
            )

            # 응답 안전 처리
            ai_response = ""

            if hasattr(response, "text"):
                ai_response = response.text
            else:
                ai_response = "응답 생성 실패"

            st.markdown(ai_response)

            # 저장
            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_response
            })

except Exception as e:

    error_msg = f"""
```

오류 발생:

{str(e)}
"""

```
    st.error(error_msg)
```
