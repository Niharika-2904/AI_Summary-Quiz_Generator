# 📄 AI Summary - Quiz Generator


## 📋 Overview :-

A web app built with **Streamlit** and **Groq Llama 3**, which :  

-  Summarizes any uploaded PDF  
-  Generates a multiple-choice quiz based on the content  
-  Lets the user take the quiz and shows the score

### 🌐 Live Demo on Streamlit - https://niharika-2904-ai-summary-quiz-generator-app-fruumh.streamlit.app/


## 🌟 Features :-

⭐ Upload a PDF and extract its text  
⭐ Get a clear, concise summary of the document  
⭐ Auto-generated quiz with MCQs and answers  
⭐ Take the quiz interactively and see your score  
⭐ Responsive, clean UI styled with CSS  
 

## 📂 Project Structure :-

- `app.py` — 🚀 Main Streamlit app (frontend & logic)
- `groq_api.py` — 🧠 Handles Groq API calls (summary & quiz)
- `requirements.txt` — 📦 Python dependencies
- `.env` — 🔑 Your API key (never push this to GitHub)
- `.gitignore` — 🙈 Files & folders to ignore in git
- `README.md` — 📄 Project documentation
- `static/style.css` — 🎨 Custom CSS styles for Streamlit
- `venv/` — 🐍 Virtual environment (optional, not pushed)
- `pdf_utils.py` — 📂 PDF handling utility



## 🖥️ Tech Stack :-

- Python
- Streamlit
- Groq API
- Llama 3
- PyPDF2


## 🚀 Installation :-

### Clone the repository;

git clone https://github.com/yourusername/ai-pdf-quiz-app.git
cd ai-pdf-quiz-app

### Create a virtual environment;

python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

### Install dependencies;

pip install -r requirements.txt

### Add your Groq API Key; 

Create a .env file in the root folder:
GROQ_API_KEY=your_groq_api_key_here

### Run the App;

streamlit run app.py


## 👩‍💻 Author :-
🌟Niharika Saxena
