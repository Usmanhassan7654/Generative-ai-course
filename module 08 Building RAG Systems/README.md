# Bano Qabil — Module 08: Building RAG Systems, Part 2

## Start teaching here

**Your main teaching file is `vscode.ipynb` or `colab.ipynb`.** Teach each Markdown explanation, run the next code cell, and pause to discuss the **printed text, vectors, chunk boundaries and retrieved evidence**. Both notebooks contain the whole lesson inline; nothing is hidden in `core.py` or a separate implementation.

## Contents

- `vscode.ipynb` — full local classroom notebook; all steps from loaders through final RAG function
- `colab.ipynb` — same full classroom notebook, with Colab ZIP upload and Secrets setup
- `streamlit_app.py` — thoroughly commented standalone chatbot interface (run locally)
- `data/greenfield_farm_knowledge.txt` — realistic **fictional** teaching knowledge base
- `Module_08_RAG_Part_2_Classroom.pptx` — 16-slide visual PowerPoint
- `requirements.txt` — Python packages for both notebooks and Streamlit
- `.env.example` — example credential names; **never publish real API keys**
- `challenge/STUDENT_CHALLENGE.md` — multi-document company RAG exercise

## Option A — VS Code (Python 3.11 or 3.12)

1. Extract the ZIP, then **open the `Module_08_Teacher_Ready` folder** in VS Code.
2. Select a Python notebook kernel; in VS Code terminal run `python -m pip install -r requirements.txt`.
3. Copy `.env.example` to `.env`, add either `GROQ_API_KEY` or `GOOGLE_API_KEY`, and set `LLM_PROVIDER`.
4. Open **`vscode.ipynb`** and execute its cells sequentially.
5. After the notebook, run `python -m streamlit run streamlit_app.py` and open the localhost link.

## Option B — Google Colab

1. Open a new notebook in Colab. **Upload `colab.ipynb` using File → Upload notebook**.
2. Run its ZIP-upload cell and choose this entire **`Module_08_Teacher_Ready.zip`** archive; that includes the data, requirements, and app.
3. Run its install cell. Add `GROQ_API_KEY` or `GOOGLE_API_KEY` in Colab Secrets (key icon) and allow notebook access.
4. Run the remaining cells in order. The last page introduces the Streamlit app; the app is intended to be run from VS Code or a terminal, not in Colab by default.

## Teacher schedule

1. Review Module 07 and load the sample TXT (print original document).
2. Split, print **every chunk**, examine source positions and compare chunk sizes.
3. Compute local Hugging Face embeddings and inspect vector values/dimensions.
4. Search Chroma with and without distance scores; print retrieved evidence.
5. Construct the exact prompt; talk about untrusted document data; call a Groq/Gemini LLM.
6. Evaluate retrieval on known facts, inspect an unknown fact, compare `k=1,3,5`.
7. Assemble one `ask_rag()` function, then show the Streamlit app.
8. Give the independent multi-document company challenge.

**Note:** Free Groq/Gemini tiers have changing quotas and model availability. The default model names are examples; change them if your account requires. Embedding download needs internet the first time, but no Hugging Face API key. The demonstration uses Chroma's local vectors and a single fictional document.

**Safety:** Prompt construction is a mitigation, not a foolproof prompt-injection defense. Similarity search always returns top matches even for irrelevant questions, so human review and more advanced retrieval filtering are needed before real-world deployment.
