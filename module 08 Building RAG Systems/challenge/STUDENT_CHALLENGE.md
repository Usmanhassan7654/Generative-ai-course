# Student challenge — Multi-document company RAG assistant

## Story
You are an AI engineer hired by **Northstar Office Supplies**, a fictional Pakistan-based company. Support agents lose time searching across four documents. Build an assistant that answers customer and employee questions using **only the provided company files**.

## Required behavior (students implement independently)
1. Load **all four** input documents from `company_documents/` using Module 07 loaders.
2. Split, embed and persist them in a local vector DB; **do not re-embed every question**.
3. Retrieve relevant excerpts and answer using an LLM, including **source filenames**.
4. If a question is unsupported, clearly state that the answer cannot be found.
5. Make a simple chatbot UI or command-line interface.
6. Include five evaluation questions with evidence excerpts and explain two failure cases.
7. Keep API credentials outside source control. Never claim a refund policy not found in the documents.

## Questions to test
1. What is the return window for unopened stationery? (policy)
2. Does NS-240 include a rechargeable battery? (catalog)
3. When is the sales support desk available? (FAQ)
4. How many annual leave days does a full-time employee receive? (handbook)
5. Can I return a used ink cartridge? (policy)
6. Who founded Northstar Office Supplies? (**not documented**)
7. Is free international shipping available? (**not documented**)
8. If an item is defective on arrival, what should I provide to support? (policy)
9. What is the price of NS-240? (catalog)
10. How many total employees work at Northstar? (**not documented**)

## Scoring (100 points)
- Multi-format loading and metadata: 15
- Chunking, embeddings, persistent vector store: 20
- Accurate evidence retrieval: 15
- Grounded answer + visible source citation: 20
- Correct abstention and injection-aware prompt: 15
- Evaluation and clear demo: 15

## Stretch goals
Add source-linked page numbers, configurable retrieval `k`, a simple evaluation dashboard, or a reranker. Avoid storing sensitive data in public repositories.

**Instructor note:** The challenge can be tackled with the reusable module code as a starting point, but students should independently adapt ingestion, source selection, and UI. Do not hand over a prebuilt challenge-specific solution.
