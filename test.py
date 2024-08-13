import streamlit as st
import openai
import streamlit.components.v1 as components

# OpenAI API 키 설정
openai.api_key = "sk-8qn-iwsc5zAnDEtS5nMOGpD8BCmKyVhaRi8AnmmAEtT3BlbkFJgWkSwBQ6MEFB-SSXnpig9t3jEyAyDjYDohRIxreswA"

st.title("쉽게 배우는 AI 딥러닝 연수 GPT 240817-240818")

# 세션 상태에서 'messages' 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

def send_message():
    user_message = st.session_state.user_input
    if user_message:
        # 사용자 메시지를 세션 상태에 추가
        st.session_state['messages'].append({"role": "user", "content": user_message})

        # OpenAI API 호출 (최신 방식으로 수정)
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo",
                prompt=user_message,
                max_tokens=150
            )
            # 어시스턴트의 응답을 추출
            assistant_message = response.choices[0].text.strip()

            # 어시스턴트 응답을 세션 상태에 추가
            st.session_state['messages'].append({"role": "assistant", "content": assistant_message})
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
            f"<div style='background-color: #d1e7dd; padding: 10px; border-radius: 5px;'>User:</div>",
            unsafe_allow_html=True
        )
        st.code(message['content'], language="python")
    else:
        st.markdown(
            f"<div style='background-color: #f8d7da; padding: 10px; border-radius: 5px;'>Assistant:</div>",
            unsafe_allow_html=True
        )
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
    del st.session_state['scroll_to_bottom']
