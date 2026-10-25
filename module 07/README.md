# LangChain document loaders - beginner teaching package

Learn how TXT, PDF, CSV, websites and Wikipedia become LangChain Documents.
Loading local files needs no API key. Gemini or Groq is an optional final lesson.
This is a simple loader demonstration, not a retrieval or vector-database app.

## Files
- `loaders_demo.py`: commented VS Code Python lesson and command-line entry point.
- `document_loaders_vscode.ipynb`: dedicated local VS Code notebook.
- `document_loaders_colab.ipynb`: Colab notebook with ZIP upload setup.
- `data/successful_dairy_farming.txt`: original classroom text, eight paragraphs.
- `data/pakistan_dairy_meat_report.pdf`: five-page tabular report, FY2016-17 to FY2025-26.
- `data/employee_records.csv`: the supplied CSV, preserved in full (30,000 records).
- `.env.example`: blank key template. Never publish your completed `.env`.
- `requirements.txt`: only packages used in this lesson.
- `requirements-lock.txt`: exact resolved versions from the validation environment, if present.

## VS Code on Windows
1. Extract the ZIP and open the `langchain_loader_classroom` folder in VS Code.
2. Install Python 3.11 or 3.12 and the VS Code Python extension.
3. Open Terminal > New Terminal and run:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe loaders_demo.py
```

Using the environment's Python directly avoids PowerShell activation-policy issues.
Select `.venv` using Python: Select Interpreter in VS Code.
On macOS/Linux use `python3 -m venv .venv`, then `.venv/bin/python` in place of the Windows Python path.

Optional web and Wikipedia lesson:
```powershell
.venv\Scripts\python.exe loaders_demo.py --online
```

## Optional AI summary: choose ONE provider
Copy `.env.example` to `.env` in the project folder and enter only the key you use.
Get a Gemini key at https://aistudio.google.com/apikey or a Groq key at https://console.groq.com/keys.
Gemini uses `GOOGLE_API_KEY`; Groq uses `GROQ_API_KEY`.
No OpenAI key is required. Model availability, billing and quotas depend on the account.

```powershell
Copy-Item .env.example .env
# Edit .env in VS Code, then choose one:
.venv\Scripts\python.exe loaders_demo.py --provider gemini
.venv\Scripts\python.exe loaders_demo.py --provider groq
```

Model defaults are configurable using `GEMINI_MODEL` and `GROQ_MODEL` in `.env`.
If a model is retired or unavailable, copy an available chat model ID from your provider's console.
The optional summary sends the dairy TXT only (at most 8,000 characters).
It does not send the employee CSV. Do not substitute private data without permission.

## Google Colab
1. Open https://colab.research.google.com/ and upload `document_loaders_colab.ipynb` via File > Upload notebook.
2. Run its upload cell and upload the complete classroom ZIP, not individual data files.
3. Run cells from top to bottom. The ZIP contains the Python helper and all three data files.
4. For AI, add one key in Colab Secrets (key icon), grant notebook access, choose `PROVIDER`, and set `RUN_AI = True`.
5. Keep `RUN_AI = False` for an entirely API-free lesson. Colab uploads disappear after a runtime reset; upload again.

Open `document_loaders_vscode.ipynb` for the dedicated VS Code lesson. For VS Code notebooks, install the Jupyter extension and `pip install ipykernel` in `.venv`, open the project folder, select that kernel, and skip the Colab-only upload cell.

## Suggested teaching order (45-60 minutes)
1. Explain `Document.page_content` (text) and `Document.metadata` (source details).
2. Load the TXT: one whole-file Document.
3. Load the PDF: one Document per page; inspect page metadata (page index is normally zero-based).
4. Load five CSV rows with `lazy_load()`: one Document per row. Show how `.load()` would load all 30,000.
5. Try web and Wikipedia when internet is available.
6. Explain that a loader reads data, while a chat model generates a response. Optionally summarize the TXT.

Expected local results: one TXT Document, five PDF Documents, five preview CSV Documents.
PDF extraction preserves readable text, but does not reconstruct tables as structured rows and columns.
This example uses a short whole-text prompt; it does not search all documents for answers.

## Dependency choices
The original list included OpenAI, Anthropic, Ollama, Streamlit and LangGraph. They are not used in this lesson and have been omitted to keep installation simple. `python-dotenv` is the package providing `from dotenv import load_dotenv`. Core LangChain dependencies are installed transitively by the integrations; the umbrella `langchain` package is not needed here.
Use the version ranges in requirements.txt for normal installation. The lock file records the exact validation resolution and is intended for a matching Python environment.

## Report source and scope
The five-page PDF uses the official Pakistan Economic Survey 2025-26, Agriculture, Appendix Table 2.1 B (continued) and Tables 2.14-2.15:
https://www.finance.gov.pk/survey/chapter_26/2_Agriculture.pdf
Milk is the human-consumption series; total meat includes poultry. FY2025-26 is provisional. Growth calculations use nine intervals across ten observations. Official estimates and their census assumptions are explained in the PDF. Higher total output does not establish higher per-animal productivity, farm profit, or better quality. Suggested improvements are author-prepared teaching material.

## Troubleshooting
- Module not found: install requirements using the same Python selected in VS Code or the notebook kernel.
- File not found: extract the full ZIP; keep data beside loaders_demo.py. The script resolves paths from its own location.
- Missing key: check the `.env` filename and selected provider; in Colab enable notebook access to the Secret.
- Authentication/quota/model errors: check the provider console, available model IDs, billing and rate limits. Never paste keys into class slides or notebook cells.
- Web/Wikipedia error: network blocks, ambiguous topics, or site changes can interrupt optional examples. Local files still work.

## Official integration references
- https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai
- https://docs.langchain.com/oss/python/integrations/chat/groq
- https://console.groq.com/docs/models
- https://ai.google.dev/gemini-api/docs/models
