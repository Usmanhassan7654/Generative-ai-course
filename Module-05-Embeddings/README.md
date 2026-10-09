# Module 05 — Beginner edition
Prepared by Engr Usman Hasan

## Teaching story
Module 4: exact ID → saved parcel status. Limitation of that classroom app: no search of written policies. Module 5: add meaning-based search while keeping exact lookup.

1. Concepts from zero, with the same cat / kitten / airplane example.
2. Real API practice with that same example.
3. Three parcel policies, one customer question, same comparison process.

## Files
- 56-slide PPTX with teacher explanations in speaker notes; PDF copy.
- Colab and VS Code notebooks, each with slide-linked tiny steps.
- Standalone Python practice; requirements.txt; blank .env.example.

## VS Code
Install Python 3.11+ and VS Code Python/Jupyter extensions. Open this folder. Run `python -m venv .venv`. Windows installation: `.venv\Scripts\python -m pip install -r requirements.txt`. macOS/Linux: `.venv/bin/python -m pip install -r requirements.txt`. Select this environment as notebook kernel. Copy .env.example to .env and enter your Google key. Run notebook top to bottom. Run Module_05_Semantic_Search.py with the same environment for terminal practice.

## Colab
Upload the Colab notebook. Use CPU. Read concepts and run the two offline exercises first. Install packages when the notebook reaches API setup. Enter a Google AI Studio key in hidden input. Run remaining cells in order.

## Scope
The beginner section uses one Google key and ends with an ordinary search function. Part D adds a Groq LLM, both tool definitions and a bounded tool-message loop. No Pydantic teaching code, advanced sorting or thresholds. Google vectors are generated through LangChain. The earlier Module 4 lookup remains separate and exact.

## Limitations and checks
Fictional policies; illustrative vectors and arrows are marked as toys. Actual API outputs are not prefilled. Highest similarity is not a guarantee of usefulness or correctness; an unrelated question can still return a nearest policy. Live API calls require authorized keys and available quota and were not executed during authoring. Live model routing and API output should be checked with your authorized keys before class.

## Sources
https://ai.google.dev/gemini-api/docs/embeddings
https://docs.langchain.com/oss/python/integrations/embeddings/google_generative_ai
https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html


## Added project: parcel customer support (Part D)
Use the notebook after the beginner exercises. Groq selects get_parcel_status or search_delivery_policy, and can request both for a mixed question. The policy tool reuses embedding vectors and cosine comparison. Python executes requested tools and sends matching ToolMessage results, then Groq explains the evidence. Source labels P1/P2/P3 identify saved policies.

Demo: “Where is PK101, and can I pay the rider when it arrives?”

Standalone: run Module_05_Parcel_Support_Agent.py in the same environment. It loads both keys from .env or hidden input. Google key: https://aistudio.google.com/apikey . Groq key: https://console.groq.com/keys . Embedding model: gemini-embedding-001 . Groq chat model: openai/gpt-oss-20b . One key does not authenticate both providers. Account quotas and model access apply. These models run through APIs, so a local GPU is unnecessary.

The app reads fictional sample data. It does not connect to a live courier or change records. A fresh conversation starts for each question. Nearest-policy search can return irrelevant evidence; prompt instructions cannot guarantee factuality. Run the notebook checklist with real keys before class. API outputs are not fabricated.

Additional sources:
https://docs.langchain.com/oss/python/integrations/chat/groq
https://console.groq.com/docs/models
https://docs.langchain.com/oss/python/langchain/tools
https://docs.langchain.com/oss/python/langchain/models
