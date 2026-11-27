# 🗺️ Agent Blueprint Card (print one per team)

> Module 12 · Designed by **Engr Usman Hasan**

**Team:** ______________________   **Agent name:** ______________________

| Part | Your answer |
|---|---|
| 🎯 **Job**: what does the agent do, for whom? (one sentence) | |
| 🧠 **Brain**: which LLM? (Groq / Gemini) | |
| 📜 **Instructions**: who is it, and what must it NEVER do? | |
| 🔧 **Tool 1**: name + one-line description + input | |
| 🔧 **Tool 2**: name + one-line description + input | |
| 🔧 **Tool 3**: name + one-line description + input | |
| 💬 **Short-term memory**: what must it remember inside one chat? | |
| 📒 **Long-term memory**: what should it remember for next time? | |
| 📚 **Knowledge (RAG)**: which documents can it search? | |
| 🛑 **Human check**: which action needs a human's YES first? | |
| 🔁 **Step limit**: max steps before it stops | |
| ⚠️ **Biggest risk**: how could it go wrong? | |

**Test question** (one that needs at least 2 tools): ______________________________________________

**Agent or workflow?** If the steps are ALWAYS the same, you may not need an agent. Tick one: ☐ Agent ☐ Workflow. Why? ____________

---
Example: *Marhaba Farm Agent*. Tools: `get_price`, `check_stock`, `calculator`, `search_farm_rules`, `place_order`. Remembers each customer's usual order in a diary. A human says YES before any order is placed. Max 6 steps.
