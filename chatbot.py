import os
import streamlit as st
import time
import base64
import uuid
import tempfile
import fitz  # PyMuPDF
from openai import OpenAI

# 세션 초기화
if "id" not in st.session_state:
    st.session_state.id = uuid.uuid4()
    st.session_state.file_cache = {}
    st.session_state.messages = []

session_id = st.session_state.id

# OpenAI 클라이언트 설정
client = OpenAI(
    api_key="up_BBuHWnUU9XAXW9jKJxNqMgiNZtCjL",  # 여기에 Upstage API 키 입력
    base_url="https://api.upstage.ai/v1"
)

qa_system_prompt = """질문-답변 업무를 돕는 보조원입니다. 
질문에 답하기 위해 검색된 내용을 사용하세요. 
답을 모르면 모른다고 말하세요. 
답변은 세 문장 이내로 간결하게 유지하세요.

## 답변 예시
📍답변 내용: 
📍증거: 

{context}"""

# PDF 파일을 텍스트로 변환
def extract_text_from_pdf(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_file.read())
        temp_pdf_path = temp_pdf.name

    doc = fitz.open(temp_pdf_path)
    text = "\n".join(page.get_text("text") for page in doc)
    os.remove(temp_pdf_path)
    return text

# AI 응답 함수
def get_response(user_input, retrieved_context=""):
    messages = [
        {"role": "system", "content": qa_system_prompt.format(context=retrieved_context)},
        #{"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model="solar-pro",
        messages=messages,
        stream=False  # 스트리밍을 원하면 True로 변경
    )

    return response.choices[0].message.content

# PDF 미리보기
def display_pdf(file):
    st.markdown("### PDF Preview")
    base64_pdf = base64.b64encode(file.read()).decode("utf-8")
    pdf_display = f"""<iframe src="data:application/pdf;base64,{base64_pdf}" width="400" height="100%" type="application/pdf"
                        style="height:100vh; width:100%">
                    </iframe>"""
    st.markdown(pdf_display, unsafe_allow_html=True)

# 사이드바 - 문서 업로드
with st.sidebar:
    st.header(f"게임 State 데이터 테이블 업로드")
    uploaded_file = st.file_uploader("Choose your `.pdf` file", type="pdf")

    # ✨ 챗봇 설명 추가 ✨
    st.markdown("""

    게임 상태 데이터를 분석해 플레이어 행동을 파악하고 게임 퀘스트와 이벤트를 자동 생성하는데 Upstage의 Solar LLM을 적용해보자
    """)

    if uploaded_file:
        st.write("Extracting text from document...")
        retrieved_context = extract_text_from_pdf(uploaded_file)

        st.success("Ready to Chat!")
        display_pdf(uploaded_file)

# 웹사이트 제목
st.title("Solar LLM Chatbot을 사용하여 게임 퀘스트 및 Event 생성하기")


# 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 프롬프트 비용 절약을 위한 메시지 제한
MAX_MESSAGES_BEFORE_DELETION = 4

# 유저 질문 처리
if prompt := st.chat_input("Ask a question!"):
    # 메시지 개수 제한
    if len(st.session_state.messages) >= MAX_MESSAGES_BEFORE_DELETION:
        del st.session_state.messages[0:2]

    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = get_response(prompt, retrieved_context if uploaded_file else "")

        # 증거자료 보여주기
        with st.expander("Evidence context"):
            st.write(retrieved_context if uploaded_file else "No document provided.")

        # 타이핑 효과
        for chunk in full_response.split(" "):
            full_response += chunk + " "
            time.sleep(0.2)
            message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

    # AI 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": full_response})

print("_____________________")
print(st.session_state.messages)
