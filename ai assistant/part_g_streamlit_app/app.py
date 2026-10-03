import pandas as pd
import streamlit as st

from assistant_core import create_assistant
from business_logic import LEADS_FILE
from company_data import COMPANY_CONFIG

st.set_page_config(
    page_title=f"{COMPANY_CONFIG['company_name']} AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title(f"🤖 {COMPANY_CONFIG['company_name']} Assistant")
st.caption("A practical LangChain + Groq + Tools website assistant")

with st.sidebar:
    st.header("Company")
    st.write(COMPANY_CONFIG["about"])
    st.write(f"📍 {COMPANY_CONFIG['location']}")
    st.write(f"🕒 {COMPANY_CONFIG['working_hours']}")
    st.divider()
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

if "assistant" not in st.session_state:
    st.session_state.assistant = create_assistant()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask about services, prices, discounts or contact...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = st.session_state.assistant.invoke({
                "messages": st.session_state.messages
            })
            answer = result["messages"][-1].content
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.divider()

with st.expander("View captured leads"):
    if LEADS_FILE.exists():
        leads_df = pd.read_csv(LEADS_FILE)
        st.dataframe(leads_df, use_container_width=True)
    else:
        st.info("No leads captured yet.")
