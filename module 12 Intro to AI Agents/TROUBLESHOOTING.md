# 🔧 Troubleshooting (Module 12)

> Module 12 · Designed by **Engr Usman Hasan**

| Problem | Fix |
|---|---|
| `KeyError: 'GROQ_API_KEY'` / key not found (VS Code) | Copy `.env.example` to `.env` (same folder as the notebook), paste the key after `=` with no spaces or quotes, then **restart the kernel** |
| Key not found (Colab) | 🔑 Secrets: the name must be exactly `GROQ_API_KEY` or `GEMINI_API_KEY`, and **Notebook access** must be ON |
| `SecretNotFoundError` in Colab | You set `PROVIDER = "groq"` but only added a Gemini key (or the other way round). Change `PROVIDER` |
| `model not found` / `model_decommissioned` | Model names change. See the links in the README and change the model name |
| `429` / `rate limit` | Free keys allow a limited number of calls per minute. Wait 1 minute, or switch `PROVIDER`. Agents make several calls per question! |
| Day 1: agent says "Wrong format" again and again | The model is not following the ReAct format. Run again, or try the other provider. This is a real failure mode: discuss it in class |
| Day 1: `⛔ Stopped: max_steps reached` | The question needed more steps. Increase `max_steps`, or ask a simpler question |
| Day 2: `GraphRecursionError` | Same thing in LangGraph: the agent needed more steps than `recursion_limit` |
| Day 2: graph picture does not show | Drawing the picture needs internet. The notebook prints the graph as text instead, which is fine |
| Day 2: `input()` box doesn't appear | Look for a small text box under the cell (VS Code: at the top of the window). Type `yes` or `no` and press Enter |
| Answers differ from the teacher's screen | Normal! The agent decides its own steps. Compare the **steps**, not the exact words |
| `ModuleNotFoundError` | Run the install cell (Colab) or `pip install -r requirements.txt` (VS Code), then restart the kernel |
