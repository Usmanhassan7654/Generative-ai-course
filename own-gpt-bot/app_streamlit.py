"""
AskBuddy - Version 2
Run this file as a Streamlit web app.

Command:
    streamlit run app_streamlit.py

This version uses the same LangChain + Gemini logic as app_terminal.py.
The main difference is that input/output appears in a browser.
"""

# -----------------------------
# STEP 1: Load environment file
# -----------------------------
from dotenv import load_dotenv

load_dotenv()


# -----------------------------
# STEP 2: Import libraries
# -----------------------------
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st


# -----------------------------
# STEP 3: Create Gemini model
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)


# -----------------------------
# STEP 4: Create the page
# -----------------------------
st.title("🤖 AskBuddy – AI QnA Bot")
st.markdown("A simple QnA chatbot built with **LangChain + Google Gemini + Streamlit**.")


# -----------------------------
# STEP 5: Create conversation memory
# -----------------------------
# session_state keeps data even when Streamlit reruns the file.
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# STEP 6: Show previous messages
# -----------------------------
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])


# -----------------------------
# STEP 7: Get a new user message
# -----------------------------
query = st.chat_input("Ask anything...")


# -----------------------------
# STEP 8: Send message to Gemini
# -----------------------------
if query:

    # Save and display the user's message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    st.chat_message("user").markdown(query)

    # IMPORTANT:
    # We send the COMPLETE conversation history,
    # not only the latest question.
    # This gives the chatbot simple conversation memory.
    response = llm.invoke(st.session_state.messages)

    # Display Gemini's reply
    st.chat_message("assistant").markdown(response.content)

    # Save Gemini's reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": response.content
    })
