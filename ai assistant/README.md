# AI Assistant — Module 04

Beginner-friendly Universal Company AI Assistant using LangChain, Groq and tools.

Model used throughout: `openai/gpt-oss-20b`

## Files

- `Module_04_Colab_Parts_A_to_F.ipynb` — Parts A–F for Google Colab.
- `Module_04_VSCode_Parts_A_to_F.ipynb` — Parts A–F for local VS Code learning.
- `Module_04_Part_G_Streamlit_VSCode.ipynb` — Part G: convert the assistant into a Streamlit app.
- `part_g_streamlit_app/` — ready-to-run Streamlit project.

## Learning flow

1. Setup and connect Groq.
2. Start with normal Python functions.
3. Convert functions into LangChain tools.
4. Add company information, pricing, calculator and lead-capture tools.
5. Create the AI assistant with a system prompt.
6. Add simple conversation history.
7. Complete the student project.
8. Move the same code into Streamlit and prepare it for deployment.

## Run Streamlit

```bash
cd "ai assistant/part_g_streamlit_app"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

Add your Groq API key to `.env` before running.
