import streamlit as st
import pandas as pd

# 앱의 제목
st.title("독서 진행 상황 기록 앱")

# 책 목록을 저장할 데이터프레임 초기화
if 'books' not in st.session_state:
    st.session_state.books = pd.DataFrame(columns=["책 이름", "읽음 여부"])

# 책 추가 기능
def add_book(book_name):
    new_book = pd.DataFrame({"책 이름": [book_name], "읽음 여부": [False]})
    st.session_state.books = pd.concat([st.session_state.books, new_book], ignore_index=True)

# 책 삭제 기능
def delete_book(book_name):
    st.session_state.books = st.session_state.books[st.session_state.books["책 이름"] != book_name]

# 책 읽음 상태 업데이트 기능
def toggle_read_status(book_name):
    st.session_state.books.loc[st.session_state.books['책 이름'] == book_name, '읽음 여부'] = \
        not st.session_state.books.loc[st.session_state.books['책 이름'] == book_name, '읽음 여부'].values[0]

# 책 추가 입력란
book_name = st.text_input("책 이름을 입력하세요:")
if st.button("책 추가"):
    if book_name:
        add_book(book_name)
        st.success(f"'{book_name}'이 추가되었습니다.")
    else:
        st.warning("책 이름을 입력해주세요.")

# 책 삭제 입력란
book_name_to_delete = st.selectbox("삭제할 책을 선택하세요:", st.session_state.books["책 이름"].tolist() if not st.session_state.books.empty else [''])
if st.button("책 삭제"):
    if book_name_to_delete:
        delete_book(book_name_to_delete)
        st.success(f"'{book_name_to_delete}'이 삭제되었습니다.")
    else:
        st.warning("삭제할 책을 선택해주세요.")

# 현재 책 목록 표시
st.subheader("현재 독서 목록")
for index, row in st.session_state.books.iterrows():
    read_status = "읽음" if row["읽음 여부"] else "읽지 않음"
    if st.checkbox(f"{row['책 이름']} ({read_status})", value=row["읽음 여부"], key=row['책 이름']):
        toggle_read_status(row['책 이름'])

# 앱 종료 시 상태 저장
if st.button("상태 저장"):
    st.session_state.books.to_csv("책_목록.csv", index=False)
    st.success("상태가 저장되었습니다.")
