# 🤖 Module 12: Intro to AI Agents (Marhaba Cattle & Dairy Farm)

> Designed by **Engr Usman Hasan** · Bano Qabil Generative AI course

**A chatbot answers. An agent acts.** Bilal, our farm bot, could already talk, read the farm's files (RAG) and learn habits (fine-tuning). In this module he gets **hands**: tools he chooses and uses by himself, in a loop, until the job is done. This is where students move from GenAI to **agentic AI**.

| Class | Slides | Notebook | What happens |
|---|---|---|---|
| **Day 1, Saturday (2 h)** | `Module_12_Day1_Saturday_Agents_from_Scratch.pptx` | `Module12_Day1_Agent_From_Scratch_*.ipynb` | Chatbot vs workflow vs agent · the agent loop · **ReAct** · tools · build an agent **from scratch** in plain Python · failure lab |
| **Day 2, Sunday (2 h)** | `Module_12_Day2_Sunday_Memory_Design_LangGraph.pptx` | `Module12_Day2_Memory_and_LangGraph_*.ipynb` | LangChain `create_agent` · **memory** (short-term, long-term, knowledge) · single-agent design · **LangChain vs LangGraph** · build a graph · human-in-the-loop · **your own agent** |

**Syllabus:** What are AI agents? Agent loops and reasoning patterns (ReAct) · Giving agents tools and memory · Single-agent architecture design · Hands-on: build a simple single-agent system that uses tools.

## 🎬 Start Saturday with the opening demo
Open `Module12_Opening_Demo_Watch_an_Agent_Think.ipynb` (Colab or VS Code), run the first two cells before class, then run **🎬 The show** on the projector: a plain chatbot fails, then the agent loops through Think → Act → Observe until it answers.

## Run in Google Colab (no install, no GPU)
1. Open https://colab.research.google.com → **File → Upload notebook** → choose the `..._Colab.ipynb` file.
2. Click the 🔑 **Secrets** icon (left side) → **Add new secret** → name `GROQ_API_KEY` (or `GEMINI_API_KEY`) → paste your free key → turn **Notebook access** ON.
3. Run the cells from top to bottom.

## Run in VS Code
```bash
python -m venv .venv
.venv\Scripts\activate            # Windows   (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env            # macOS/Linux: cp .env.example .env   → paste your free key in .env
```
Open a `..._VSCode.ipynb` notebook, pick the `.venv` kernel, and run the cells in order.

```bash
python farm_agent.py "Ali ko 15 litre doodh chahiye, bill kitna hoga?"   # the agent in the terminal
streamlit run streamlit_app.py                                           # chat app with a live "Agent thinking" box
```

Free keys: [Groq](https://console.groq.com/keys) · [Google AI Studio (Gemini)](https://aistudio.google.com/apikey). **Never commit `.env`.**
Each notebook has `PROVIDER = "groq"` at the top. Change it to `"gemini"` to use Gemini.

## Files
| File | What it is |
|---|---|
| `Module_12_Day1_Saturday_Agents_from_Scratch.pptx` / `Module_12_Day2_Sunday_Memory_Design_LangGraph.pptx` | The two decks, with speaker notes in Roman Urdu |
| `Module12_Day1_Agent_From_Scratch_VSCode.ipynb` / `_Colab.ipynb` | Day 1 lab: tools, ReAct prompt, the loop by hand, the loop in code, a new tool, failure lab. Every line commented |
| `Module12_Day2_Memory_and_LangGraph_VSCode.ipynb` / `_Colab.ipynb` | Day 2 lab: `@tool`, `create_agent`, memory, `recursion_limit`, a LangGraph graph built by hand, `interrupt()` before orders, your own agent. Every line commented |
| `Module12_Opening_Demo_Watch_an_Agent_Think.ipynb` | Teacher's opening demo: chatbot vs agent, every loop shown as big coloured steps. One file for Colab and VS Code |
| `farm_agent.py` | The Day 1 agent from scratch in one file (used by the app) |
| `streamlit_app.py` | Chat with the agent and watch every Thought / Action / Observation |
| `AGENT_BLUEPRINT.md` | Printable card for the Day 2 design game and boss level |
| `HOMEWORK.md` | Saturday → Sunday homework and the final mini-project |
| `TROUBLESHOOTING.md` | Common errors and fixes |

## Models
- Groq: `llama-3.3-70b-versatile` · Gemini: `gemini-flash-latest` (always the newest Flash model).
- Model names change. If you get `model not found`, check https://console.groq.com/docs/models or https://ai.google.dev/gemini-api/docs/models and change the name in the notebook (Day 1: `MODELS`, Day 2: the brain cell) or in `farm_agent.py`.

The farm's prices, stock and rules are invented for teaching.

---
© Module 12 course material designed by **Engr Usman Hasan**.
