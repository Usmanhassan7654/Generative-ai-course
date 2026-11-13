# 🐄 Module 09 — Advanced RAG Kit (Marhaba Cattle & Dairy Farm)

Is folder mein do tareeqe hain. Jo aasan lage, woh chalayein.

## Option A — Google Colab (sab se aasan)
1. https://colab.research.google.com kholein → **Upload** → `Module09_Advanced_RAG_Lab.ipynb`
2. Upar se neeche har cell `Shift + Enter` se chalayein.
3. Koi aur file upload nahi karni. Notebook documents aur `easy_rag.py` khud bana leti hai.
4. (Optional) Final jawab LLM se likhwana ho to 🔑 **Secrets** mein `GROQ_API_KEY` ya `GEMINI_API_KEY` daalein.

## Option B — VS Code
```bash
# 1. Folder kholein: File > Open Folder > Module09_Advanced_RAG_Kit
# 2. Terminal (Ctrl + `) mein:
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Mac / Linux
pip install -r requirements.txt

# 3. (Optional) .env.example ko copy karke .env banayein aur free key paste karein

# 4. Ek ek script chalayein
python 01_reranking.py
python 02_hybrid_search.py
python 02b_rrf_by_hand.py
python 03_query_rewriting.py
python 04_multi_document.py
python 05_long_context.py
python 06_failure_modes.py
python 07_handson_upgrade.py
```
Pehli dafa chalane par 2 chhote models download honge (~110 MB, internet chahiye). Uske baad fast chalega.

## Files
| File | Kya hai |
|---|---|
| `easy_rag.py` | Saare helper functions — har line par comment, aur upar poora FLOW diagram |
| `farm_docs/` | 7 farm documents (made-up classroom data) |
| `01` – `07` | Har topic ki ek script, end mein **YOUR TURN** exercise |
| `02b_rrf_by_hand.py` | RRF ka hisaab step by step: k=60 vs k=0 vs raw scores |
| `Module09_Advanced_RAG_Lab.ipynb` | Colab notebook, saare topics ek jagah |

## Free API keys (sirf final jawab ke liye)
- Groq: https://console.groq.com/keys
- Gemini: https://aistudio.google.com/apikey

Retrieval (search, re-rank, hybrid, rewrite) **bina key** ke chalta hai. Key ke baghair `ask_llm()` aapko woh prompt dikha deta hai jo LLM ko bheja jata.

⚠️ Apni key kabhi share na karein, aur `.env` file kisi ko submit na karein.
