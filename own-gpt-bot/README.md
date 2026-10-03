# 🤖 AskBuddy – Beginner LangChain + Gemini Project

This project contains **two very simple VS Code versions** of the same AI chatbot.

The goal is to help students move from a terminal chatbot to a Streamlit web app without changing the core AI logic.

## Files

```text
own-gpt-bot/
│
├── app_terminal.py      # Version 1: runs in VS Code terminal
├── app_streamlit.py     # Version 2: runs as a web app
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 1. Open the folder in VS Code

Open the `own-gpt-bot` folder in VS Code.

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
```

Activate it:

### Command Prompt

```bash
.venv\Scripts\activate
```

### PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

After activation, you should see `(.venv)` in the terminal.

## 3. Install the libraries

```bash
pip install -r requirements.txt
```

## 4. Create your `.env` file

Copy `.env.example` and rename the copy to `.env`.

Add your Gemini API key:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Do **not** upload `.env` to GitHub.

## 5. Run Version 1 — Terminal chatbot

```bash
python app_terminal.py
```

Type `exit` to stop the program.

## 6. Run Version 2 — Streamlit web app

```bash
streamlit run app_streamlit.py
```

Open the local address Streamlit shows in the terminal, usually:

```text
http://localhost:8501
```

## Important concept

Both versions use the same AI logic:

```python
response = llm.invoke(messages)
```

The terminal version uses `input()` and `print()`.
The Streamlit version uses `st.chat_input()` and `st.chat_message()`.

We send the full message history so Gemini can remember the current conversation.
