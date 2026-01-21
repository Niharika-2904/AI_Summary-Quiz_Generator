import streamlit as st
import PyPDF2
import json
import os
from dotenv import load_dotenv
from groq_api import get_summary, generate_quiz

load_dotenv()

# Session state init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Upload"
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "quiz" not in st.session_state:
    st.session_state.quiz = ""
if "username" not in st.session_state:
    st.session_state.username = ""
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

# Login Page
def login_page():
    st.title("🔒 Login")
    username = st.text_input("Enter your name")
    password = st.text_input("Enter password", type="password")
    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Please enter both name and password.")

# Main App
def main_app():
    st.sidebar.title("📄 AI SUMMARY-QUIZ GENERATOR")
    st.sidebar.write(f"👋 Welcome, {st.session_state.username}!")
    st.sidebar.radio("Navigate", ["Upload", "Summary", "Quiz"], key="page")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    if st.session_state.page == "Upload":
        upload_page()
    elif st.session_state.page == "Summary":
        summary_page()
    elif st.session_state.page == "Quiz":
        quiz_page()

# Upload Page
def upload_page():
    st.title("📤 Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    if uploaded_file:
        st.session_state.pdf_text = extract_text(uploaded_file)
        st.success("✅ PDF text extracted.")

        if st.button("Generate Summary"):
            if st.session_state.pdf_text.strip():
                with st.spinner("Generating summary..."):
                   st.session_state.summary = get_summary(st.session_state.pdf_text)
                st.success("✅ Summary generated. Check the Summary page.")
            else:
                st.error("❌ No readable text found in PDF.")

        if st.button("Generate Quiz"):
            if st.session_state.pdf_text.strip():
                with st.spinner("Generating quiz..."):
                   st.session_state.quiz = generate_quiz(st.session_state.pdf_text)
                   st.session_state.quiz_answers = {}
                   st.session_state.quiz_submitted = False
                st.success("✅ Quiz generated. Check the Quiz page.")
            else:
                st.error("❌ No readable text found in PDF.")


# Summary Page
def summary_page():
    st.title("📝 Summary")
    if st.session_state.summary:
        st.write(st.session_state.summary)
    else:
        st.info("No summary yet. Please generate it from the Upload page.")

# Quiz Page
def quiz_page():
    st.title("🧪 Quiz")
    if not st.session_state.quiz:
        st.info("No quiz yet. Please generate it from the Upload page.")
        return

    try:
        quiz_data = json.loads(st.session_state.quiz)
        questions = quiz_data.get("quiz", [])
    except Exception as e:
        st.error(f"Failed to load quiz: {e}")
        return

    with st.form("quiz_form"):
        st.write("### Answer the questions below:")

        for idx, q in enumerate(questions):
            q_key = str(idx)

            # Initialize answer if not already set
            if q_key not in st.session_state.quiz_answers:
                st.session_state.quiz_answers[q_key] = None

            # Safe default index
            options = q['options']
            selected = st.session_state.quiz_answers[q_key]
            if selected in options:
                default_index = options.index(selected)
            else:
                default_index = 0  # default to first option

            st.session_state.quiz_answers[q_key] = st.radio(
                f"**Q{idx+1}: {q['question']}**",
                options,
                index=default_index,
                key=f"quiz_q{idx}"
            )

        submitted = st.form_submit_button("✅ Submit Quiz")
        if submitted:
            st.session_state.quiz_submitted = True

    if st.session_state.quiz_submitted:
        score = 0
        total = len(questions)

        st.subheader("🎯 Results:")
        for idx, q in enumerate(questions):
            q_key = str(idx)
            correct_letter = q['answer'].strip()
            correct_option = next(
                (opt for opt in q['options'] if opt.startswith(correct_letter)),
                None
            )
            user_answer = st.session_state.quiz_answers.get(q_key)

            if user_answer == correct_option:
                st.success(f"✅ Q{idx+1}: Correct!")
                score += 1
            else:
                st.error(f"❌ Q{idx+1}: Wrong. Correct Answer: {correct_option}")

        st.markdown(f"### 📝 Your Score: **{score}/{total}**")

# Extract PDF text
def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text.strip()

# Run App
if not st.session_state.logged_in:
    login_page()
else:
    main_app()


   