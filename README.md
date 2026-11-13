# Generative AI Course: from LLM APIs to RAG and fine-tuning

The classroom materials for the Generative AI course I teach at **Bano Qabil** in Karachi.
Students go from their first LLM API call to tool-calling assistants, retrieval-augmented
generation (RAG) and fine-tuning datasets. Each module comes with a slide deck and runnable
code (a VS Code notebook or script, plus a Google Colab version). Most modules follow one
running scenario: a parcel-support desk and a fictional dairy business. That way students see
each new technique fix a limitation of the last one.

> Slides and speaker notes are written for beginners, with Roman Urdu teaching cues. The code
> comments and READMEs are in English, except Module 09, which is in Roman Urdu.

## Where to start

| If you are… | Start with |
|---|---|
| New to LLMs | Module 02, then 03 |
| Comfortable with API calls and want to build an assistant | Module 04 and [`ai assistant/`](ai%20assistant/) |
| Here for RAG | Modules 05 → 06 → 07 → 08 → 09 |
| Here for fine-tuning | Module 10 (no GPU or API key needed) |

## Modules

| # | Topic | What you build | Run in | API key |
|---|---|---|---|---|
| 02 | [LLM APIs to LangChain](Module-02-LLM-APIs-to-LangChain/) | Call Gemini and Groq directly, then through LangChain | VS Code, Colab | Gemini or Groq |
| 03 | [Developer prompt engineering](Module-03-Developer-Prompt-Engineering/) | Static prompts → reusable prompt chains | VS Code, Colab | Groq |
| 04 | [Tool calling](Module-04-Tool-calling/) | A parcel-status assistant that calls Python functions | VS Code, Colab | Groq |
| 04+ | [AI assistant project](ai%20assistant/) | A company assistant with LangChain tools, then a Streamlit app | VS Code, Colab | Groq |
| — | [Own GPT bot](own-gpt-bot/) | The same chatbot as a terminal app and as a Streamlit app | VS Code | Gemini |
| 05 | [Embeddings](Module-05-Embeddings/) | Semantic search over parcel policies alongside exact ID lookup | VS Code, Colab | Gemini or Groq |
| 06 | [Vector databases](Module-06-Vector-Databases/) | Store and search policies in Chroma; answers with source citations | VS Code, Colab | Gemini or Groq |
| 07 | [Document loaders](module%2007/) | Load TXT, PDF, CSV, web pages and Wikipedia into LangChain documents | VS Code, Colab | Not needed (optional final step) |
| 08 | [Building RAG systems](module%2008%20Building%20RAG%20Systems/) | Chunk → embed → retrieve → answer, with retrieval checks and a Streamlit chatbot | VS Code, Colab | Groq or Google |
| 09 | [Advanced RAG](module%2009%20Advanced%20RAG%20Techniques/) | Re-ranking, hybrid search, reciprocal rank fusion (RRF) by hand, query rewriting, failure modes | VS Code, Colab | Not needed for retrieval |
| 10 | [Intro to fine-tuning](module%2010%20Intro%20to%20Fine%20Tuning/) | Turn a spreadsheet into train/val/test JSONL and validate it | VS Code, Colab | Not needed |

## Setup (VS Code)

```bash
git clone https://github.com/Usmanhassan7654/Generative-ai-course.git
cd Generative-ai-course/"module 10 Intro to Fine Tuning"     # pick a module
python -m venv .venv
.venv\Scripts\activate            # Windows   (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt   # Module 10 needs nothing beyond Python
```

Each module that needs a key has a `.env.example`. Copy it to `.env` and paste your own key.
Free keys are available from [Groq](https://console.groq.com/keys) and
[Google AI Studio](https://aistudio.google.com/apikey). **Never commit `.env`.**

## Check that it works

These commands were run from a fresh clone on Python 3.13:

```bash
cd "module 10 Intro to Fine Tuning"
python make_dataset.py examples/01_farm_order_slips
python validate_dataset.py examples/01_farm_order_slips              # RESULT: READY
python validate_dataset.py examples/04_bad_dataset/bad_examples.jsonl # RESULT: NOT READY (on purpose)
```

## About the data

The business scenarios, policies, orders and knowledge-base texts in the exercises are written
for teaching. They are not real customer or company records. The one exception is Module 07's
PDF report: it uses public figures from the Pakistan Economic Survey 2025-26, and its source
is cited in that module's README.

## License

[MIT](LICENSE) © 2026 Usman Hasan
