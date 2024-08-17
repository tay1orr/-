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
