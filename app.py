import streamlit as st

st.set_page_config(page_title="계산기", page_icon="🧮")

st.title("🧮 파이썬 계산기")

# 숫자 입력
num1 = st.number_input("첫 번째 숫자", value=0.0)
num2 = st.number_input("두 번째 숫자", value=0.0)

# 연산 선택
operation = st.selectbox(
    "연산 선택",
    ["+", "-", "×", "÷"]
)

# 계산 버튼
if st.button("계산하기"):
    
    if operation == "+":
        result = num1 + num2

    elif operation == "-":
        result = num1 - num2

    elif operation == "×":
        result = num1 * num2

    elif operation == "÷":
        if num2 != 0:
            result = num1 / num2
        else:
            result = "0으로 나눌 수 없습니다."

    st.subheader(f"결과: {result}")
