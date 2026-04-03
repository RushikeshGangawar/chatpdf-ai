import streamlit as st
import tempfile

from auth import init_auth_db, create_user, login_user
from db import init_db, save_chat
from utils import load_and_split_pdf, create_vector_store, get_answer

st.set_page_config(page_title="ChatPDF AI")

init_auth_db()
init_db()

# Session state
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN ----------------
if st.session_state.user is None:
    st.title("🔐 Login / Signup")

    choice = st.radio("Choose", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            if create_user(username, password):
                st.success("Account created ✅")
            else:
                st.error("User already exists ❌")

    else:
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.user = username
                st.success("Login successful ✅")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")

# ---------------- MAIN APP ----------------
else:
    st.title("🤖 Chat with PDF")

    st.write(f"Welcome {st.session_state.user} 👋")

    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.read())
            path = tmp.name

        chunks = load_and_split_pdf(path)
        db = create_vector_store(chunks)

        st.success("PDF loaded successfully ✅")

        query = st.text_input("Ask question:")

        if query:
            answer = get_answer(query, db)

            st.write("### Answer:")
            st.write(answer)

            save_chat(query, answer)
