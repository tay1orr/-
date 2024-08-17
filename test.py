"""
import streamlit as st
import openai
import streamlit.components.v1 as components
import time

# OpenAI API 키 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("쉽게 배우는 AI 딥러닝 연수 GPT 240817-240818")

# 세션 상태에서 'messages' 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# 처음 모델 이름을 포함할지 여부를 세션 상태에서 관리
if 'include_model_name' not in st.session_state:
    st.session_state['include_model_name'] = True

def send_message():
    user_message = st.session_state.user_input
    if user_message:
        # 사용자 메시지를 세션 상태에 추가 (전체 대화 히스토리 유지)
        st.session_state['messages'].append({"role": "user", "content": user_message})

        # 로딩 메시지 표시
        with st.spinner("모델이 응답을 생성 중입니다..."):
            # OpenAI Chat API 호출
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",  # 모델 설정
                    messages=st.session_state['messages'],  # 전체 대화 히스토리 전달
                    max_tokens=2048  # 토큰 수 유지
                )
                # 어시스턴트의 응답을 추출
                assistant_message = response['choices'][0]['message']['content']

                # 첫 번째 응답에만 모델 이름 포함
                if st.session_state['include_model_name']:
                    model_used = response['model']
                    final_message = f"(모델: {model_used})\n{assistant_message}"
                    st.session_state['include_model_name'] = False  # 이후에는 모델 이름 제외
                else:
                    final_message = assistant_message

                # 어시스턴트 응답을 세션 상태에 추가
                st.session_state['messages'].append({"role": "assistant", "content": final_message})
            except Exception as e:
                st.error(f"API 호출 중 오류가 발생했습니다: {e}")

        # 입력 필드를 초기화
        st.session_state.user_input = ""

        # 스크롤을 맨 아래로 이동하도록 트리거하기 위해 빈 상태를 업데이트
        st.session_state['scroll_to_bottom'] = True

# 메시지를 출력하여 최신 메시지가 하단에 위치하도록 함
for message in st.session_state['messages']:
    if message['role'] == 'user':
        st.markdown(
            f"<div style='background-color: #d1e7dd; padding: 10px; border-radius: 5px; margin-bottom: 5px;'>User:</div>",
            unsafe_allow_html=True
        )
        st.code(message['content'], language="python")
    else:
        st.markdown(
            f"<div style='background-color: #f8d7da; padding: 10px; border-radius: 5px; margin-bottom: 5px;'>Assistant:</div>",
            unsafe_allow_html=True
        )
        # 응답 메시지 표시
        st.markdown(message['content'])
    st.markdown("---")

# 사용자 입력 받기 (항상 페이지 하단에 위치)
st.text_input("User:", key="user_input", on_change=send_message)

# JavaScript를 사용하여 자동 스크롤
if 'scroll_to_bottom' in st.session_state:
    scroll_script = """
    <script>
    var chatContainer = window.parent.document.getElementsByClassName('main')[0];
    chatContainer.scrollTop = chatContainer.scrollHeight;
    </script>
    """
    components.html(scroll_script)

    # 스크롤 후 상태를 초기화
    st.session_state['scroll_to_bottom'] = False
"""
import streamlit as st
import pandas as pd

# 앱 제목
st.title("독서 진행 상황 추적기")

# 세션 상태에 책 목록 초기화
if 'book_list' not in st.session_state:
    st.session_state.book_list = []

# 책 추가하기
def add_book():
    book_name = st.session_state.book_input
    if book_name:
        st.session_state.book_list.append({"title": book_name, "status": "읽지 않음"})
        st.session_state.book_input = ""  # 입력란 초기화
        st.success(f"'{book_name}'가 목록에 추가되었습니다.")

# 책 삭제하기
def delete_book(selected_book):
    if selected_book:
        st.session_state.book_list = [book for book in st.session_state.book_list if book["title"] != selected_book]
        st.success(f"'{selected_book}' 책이 목록에서 삭제되었습니다.")

# 책 상태 업데이트: 책을 읽음으로 변경
def mark_as_read(selected_book):
    for book in st.session_state.book_list:
        if book["title"] == selected_book:
            book["status"] = "읽음"
            st.success(f"'{selected_book}' 책을 읽음으로 표시하였습니다.")

# 책 상태 업데이트: 책을 읽지 않음으로 변경
def mark_as_unread(selected_book):
    for book in st.session_state.book_list:
        if book["title"] == selected_book:
            book["status"] = "읽지 않음"
            st.success(f"'{selected_book}' 책을 읽지 않음으로 표시하였습니다.")

# 사용자 입력 받기
st.text_input("읽고 싶은 책 제목 입력:", key="book_input", on_change=add_book)

# 현재 읽고 있는 책 목록 표시
if st.session_state.book_list:
    st.subheader("내 책 목록:")
    df = pd.DataFrame(st.session_state.book_list)
    st.write(df)

    # 책 상태 업데이트: 읽은 책 선택
    selected_row = st.selectbox("읽은 책 선택:", df['title'])

    if st.button("책 읽음으로 표시하기"):
        mark_as_read(selected_row)

    # 책 상태 업데이트: 읽지 않은 책 선택
    selected_unread_row = st.selectbox("읽은 책을 읽지 않음으로 변경할 책 선택:", df[df['status'] == '읽음']['title'])
    if st.button("책 읽지 않음으로 표시하기"):
        mark_as_unread(selected_unread_row)

    # 책 삭제: 드롭다운에서 선택 후 삭제 버튼 클릭
    selected_book_to_delete = st.selectbox("삭제할 책 선택:", df['title'].tolist())
    if st.button("책 삭제하기"):
        delete_book(selected_book_to_delete)

    # 읽은 책과 읽지 않은 책 필터링
    if st.checkbox("읽은 책만 보기"):
        df_read = df[df['status'] == '읽음']
        st.write(df_read)

    if st.checkbox("읽지 않은 책만 보기"):
        df_unread = df[df['status'] == '읽지 않음']
        st.write(df_unread)

else:
    st.info("읽고 싶은 책 제목을 입력하여 목록에 추가하세요.")
