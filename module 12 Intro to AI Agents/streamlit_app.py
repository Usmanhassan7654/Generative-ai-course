"""
streamlit_app.py  -  Module 12: chat with the farm agent and WATCH it think
===========================================================================
Designed by Engr Usman Hasan  (Bano Qabil Generative AI course)

THE FLOW
  you type a question -> farm_agent.run_agent() -> Thought / Action / Observation steps
  -> the steps appear in the "🧠 Agent thinking" box -> the final answer appears in the chat

HOW TO RUN
  pip install -r requirements.txt
  copy .env.example to .env and paste a FREE key
  streamlit run streamlit_app.py
"""

# Streamlit builds the web page
import streamlit as st

# our agent from scratch (same code as the Day 1 notebook)
import farm_agent

# the title of the browser tab and the page layout
st.set_page_config(page_title="Marhaba Farm Agent", page_icon="🐄")
# the big heading on the page
st.title("🐄 Marhaba Farm Agent")
# a small line under the heading
st.caption(f"An AI agent built from scratch · brain: {farm_agent.PROVIDER} · Designed by Engr Usman Hasan")

# the left sidebar
with st.sidebar:
    # a heading for the tools list
    st.header("🔧 Agent's tools")
    # show every tool's name and description (what the LLM reads)
    for name, func in farm_agent.TOOLS.items():
        # tool name in bold, description below it
        st.markdown(f"**{name}**  \n{func.__doc__}")
    # the safety limit, which students can change with a slider
    max_steps = st.slider("max_steps (safety limit)", 1, 10, 6)
    # some example questions to try
    st.header("💡 Try asking")
    # example 1
    st.write("Ali ko 15 litre doodh chahiye, bill kitna hoga aur stock hai?")
    # example 2
    st.write("I live in Clifton. 10 litre milk with delivery?")
    # example 3
    st.write("25 litre doodh discount ke saath kitne ka?")

# keep the chat history while the page re-runs (Streamlit re-runs the file on every click)
if "history" not in st.session_state:
    # an empty chat the first time
    st.session_state.history = []

# draw the old messages again
for role, text in st.session_state.history:
    # one chat bubble per message
    with st.chat_message(role):
        # the message text
        st.markdown(text)

# the text box at the bottom of the page
question = st.chat_input("Ask the farm agent...")
# when the user presses Enter
if question:
    # show the user's message
    with st.chat_message("user"):
        # the question text
        st.markdown(question)
    # save it in the history
    st.session_state.history.append(("user", question))

    # the agent's reply bubble
    with st.chat_message("assistant"):
        # a spinner while the agent works
        with st.spinner("Agent is thinking..."):
            # run the agent loop (show=False: don't print to the terminal)
            answer, steps = farm_agent.run_agent(question, max_steps=max_steps, show=False)
        # a box that can be opened to see every step
        with st.expander(f"🧠 Agent thinking ({len(steps)} steps)", expanded=True):
            # one block per step
            for s in steps:
                # the step number
                st.markdown(f"**Step {s['step']}**")
                # what the LLM wrote (Thought / Action / Action Input)
                st.code(s["llm"], language="text")
                # what the tool returned (if a tool was used)
                if s["observation"]:
                    # 👀 = observation
                    st.markdown(f"👀 **Observation:** {s['observation']}")
        # the final answer
        st.markdown(answer)
    # save the answer in the history
    st.session_state.history.append(("assistant", answer))
