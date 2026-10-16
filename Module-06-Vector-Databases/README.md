# Module 06: beginner class
Prepared by Engr Usman Hasan

Open the PowerPoint first. It follows the six requested headings: what a vector database is, why we use one, how it works, use cases, common options, and a Python/LangChain demonstration.

The lesson uses the same three parcel policies as Module 5. The core demo has only three database operations: open, save and search. Part B then introduces batch storage, reusable queries, indexing concepts and a twelve-file document-set exercise. Part C reconnects the familiar Groq tool loop and displays the final customer answer with source citations. Advanced index tuning remains outside the required code. The database can return saved text without an LLM generating an answer.

## Files
- Module_06_Vector_Databases_Lecture.pptx: 56 visual slides, with teacher explanations and Roman Urdu cues in speaker notes.
- Module_06_Vector_Databases_Lecture.pdf: a reading copy.
- Module_06_Vector_Databases_Colab.ipynb: the basic demo followed by document-set practice.
- Module_06_Vector_Databases_VSCode.ipynb: the same lesson with local setup instructions.
- parcel_documents/: twelve fictional short policy files.
- Student_Test_Sheet.csv: expected versus observed checks.
- Module_06_Simple_Demo.py: the same small example as a terminal script.
- requirements.txt: direct versions exercised with real local Chroma on Python 3.12.

## Colab
Upload the notebook, choose CPU, run top to bottom, and enter the Google key through hidden input. Installation needs internet. If imports fail after installation, restart the runtime and run from the key/model cells onward. Colab storage can disappear on a runtime reset. It is not a durable cloud database.

## VS Code
Use Python 3.11+. Open a terminal in this extracted folder.

Windows:
```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

macOS/Linux:
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Install the VS Code Python and Jupyter extensions. Select this environment as the notebook kernel. Run the notebook cells in order. The installation cell can also install into the selected kernel.

For the terminal script, run `.venv\Scripts\python Module_06_Simple_Demo.py` on Windows or `.venv/bin/python Module_06_Simple_Demo.py` on macOS/Linux. It requests the Google key privately. After the first save, change `SAVE_POLICIES = True` to `False` near the top and rerun. The saved folder stays the same and only the new question is embedded.

## Provider setup
Google key: https://aistudio.google.com/apikey
Model: gemini-embedding-001, matching Module 5.

Parts A and B need no Chroma Cloud or Groq key. Part C needs a separate Groq API key. Google embedding calls require network, model access and quota. No local GPU is needed. Never put API keys in GitHub or screenshots.

## Teaching sequence
Suggested 90–120 minutes with coding pauses. Begin with the familiar cash-on-arrival question. Explain saved text and vectors with a library catalogue analogy. Walk through saving and searching as two separate stages. Pause for the broken-parcel prediction before showing the answer. Introduce Chroma/Pinecone/Qdrant/Weaviate briefly, then run the tiny demo. Finish by trying an unanswered refund question.

## Important details
The collection uses cosine, continuing Module 5. The API returns matching Documents, so we do not add a second score system in this first demo. An internal configuration key named hnsw selects the index family; advanced algorithms are outside this lesson.

`add_texts()` generates embeddings before saving them. Stable IDs prevent extra logical duplicates in this integration, but re-running a save may still use embedding quota. When reopening unchanged policies, skip saving. Use the same collection name, folder, embedding model and settings. If changing models, create a new collection and re-embed its documents.

Search returns a nearest candidate even when there is no suitable answer. Read the evidence. A refund period is absent from our three policies and must not be invented. Exact parcel IDs still need exact lookup. All business data are fictional.

The small collection demonstrates storage and search, not large-scale performance. Local Chroma and deterministic test vectors were exercised, including a fresh-process reopen. Live Google API calls were not run during authoring; run the demo with your key before class.

## Official references
- https://docs.langchain.com/oss/python/integrations/vectorstores/chroma
- https://docs.trychroma.com/docs/collections/configure
- https://ai.google.dev/gemini-api/docs/embeddings
- https://docs.pinecone.io/guides/get-started/overview
- https://qdrant.tech/documentation/overview/
- https://docs.weaviate.io/weaviate


## Part B: storing and searching as the collection grows
Slides 37–56 extend the approved beginner introduction. The graphics explain groups of files, repeated saving steps, query-vector reuse, exact scanning, HNSW neighbor maps and IVF regions. Index choices are conceptual; local Chroma builds its HNSW index internally. The exercise keeps cosine as its closeness metric.

The notebooks first use three policies in parcel_easy_06, then create a separate collection parcel_documents_06 in ./parcel_document_db. This prevents warm-up IDs from mixing with document filenames. Part B reads twelve .txt files, stores text with stable IDs and source filenames, embeds/writes four records per batch, retrieves a few matches and reopens the saved collection.

The twelve-file example proves the workflow, not million-vector performance. Four records is a teaching batch size, not a production prescription. The classroom loader holds twelve texts in Python; a large loader should read bounded groups. Respect API limits, track failed batches, handle updates and backups, and measure quality/latency/memory for production. These procedures are discussed, not implemented as hidden features.

On repeat ingestion, stable IDs keep logical record counts stable, but add_texts can regenerate embeddings and consume quota. For the persistence experiment skip all save cells and run imports/model setup plus the Part B reopen cell. New questions still need query embeddings. Part B prints original source text for inspection. Part C lets Groq request that search through a tool and write the final answer.

Suggested delivery: two sessions. Teach slides 1–36 and Part A first. Then use slides 37–56 with Part B, including deliberate pauses to explain list slicing. Alternatively allow about 3 hours plus breaks for the whole module. Teacher explanations and Roman Urdu cues remain in the speaker notes.


## Part C: the LLM searches Chroma and writes the answer
Run Parts A and B to populate doc_db, then continue to Part C in either notebook. The updated installation cell includes langchain-groq. Enter the Groq key through hidden input: https://console.groq.com/keys . The LLM is openai/gpt-oss-20b through ChatGroq, matching Module 5. Google still creates query embeddings inside the tool.

The first model turn requires a search tool request. Groq writes the query, Python executes the allowed Chroma tool, and matching ToolMessages return text and source filenames. Groq then explains the retrieved evidence in simple language. Markdown renders the final response clearly. The application does not manually preselect a passage and then merely ask an LLM to paraphrase it.

Use C7 with show_trace=True to show the model's search queries and database evidence in class. Use C8 with show_trace=False for a clean customer-facing answer. Each question starts fresh. The four-turn bound prevents an unbounded search loop. The model may refine its query before answering.

Grounding instructions require source citations and honest missing-policy answers, but prompt rules cannot guarantee factuality. Test actual retrieval and generation with your authorized Google/Groq keys. Local tests use real Chroma with deterministic embedding vectors and simulated LLM requests; live model routing and generated answers were not validated during authoring. No keys or fabricated model outputs are included.
