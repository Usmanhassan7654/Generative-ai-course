# Evidence-aware AI Support Routing — Reproducible Research Prototype

**Status:** exploratory research / NOT a new database engine / NOT publication-validated.

An executable, read-only banking-support triage application and evaluation harness. The proposed contribution is a **validation-tuned selective-routing policy** that can defer uncertain classifications to review. The implemented prototype combines word-level and character-level TF-IDF/logistic models, compares their late fusion to an adaptive gate, and records traceable decisions in SQLite. It does not yet implement a graph database, neural embeddings, SQL query planning, streaming, model security policy enforcement, or calibrated uncertainty. Do not describe any of those as tested.

## Real dataset

[Banking77, PolyAI](https://github.com/PolyAI-LDN/task-specific-datasets/tree/master/banking_data), CC BY 4.0, 10,003 train utterances + 3,080 untouched official test utterances, 77 fine-grained intents. The full benchmark downloads files pinned to commit `9d081458ff52e53cf7e848f414e6e9344e4e6696`, checks SHA256, stratifies 20% of the *training split* for validation and uses the held-out official test set once. Raw datasets are not redistributed; original citations/terms apply. No sensitive banking customer information or real account systems are used.

## Run

```bash
python -m pip install -r requirements.txt
python benchmark.py --demo --out results/local_smoke.json
python app.py --demo 'When will my card arrive?'
# internet access required for official, complete data
python benchmark.py --out results/banking77.json
python app.py 'My transfer is still pending'
```

Results are reproducible with random seed 42. Accuracy and macro-F1 are recorded for word logistic, character logistic, equal-weight probability fusion, and validation-gated method. A *paired bootstrap* 95% confidence interval estimates the test-set difference between gated and hybrid performance. The abstain threshold is tuned on validation for >=90% accepted-answer accuracy where possible, and evaluated on test without retuning. This is not a formal reliability guarantee.

## Observed local result (24 demo utterances; 6 test examples)

- Word baseline 83.33%, character baseline 83.33%, fusion 83.33%, gated method 83.33%.
- Accuracy gain: **0.00 percentage points**, paired bootstrap CI `[0, 0]` (uninformative due to tiny sample).
- Selective coverage 66.7%, accepted-answer accuracy 100% (`4/4`).
- These are **smoke-test-only** outcomes and must not be compared to state-of-the-art results.

## Research limitations and integrity

1. This tests intent classification, not vector search, graph traversal, RAG response generation, database transaction throughput or deployed customer-support resolution.
2. Validation chooses thresholds; we still need calibration, independent tasks, shifts/freshness stress tests and ablations.
3. No present evidence establishes the component combinations as novel. Adaptive-RAG (Jeong et al. 2024) and Corrective RAG (Yan et al. 2024) are important prior art.
4. The demonstration does not send money, expose accounts or execute operational actions. `app.py` only proposes an intent and writes a local audit log.
5. AI-assisted preparation: all submissions must disclose assistance under the venue's policies and all authors must verify references and results.

## Future experiments necessary before conference submission

- Stronger baselines: BM25, dense sentence embeddings, cross-encoder reranking, logistic and calibrated selective classification.
- Multiple domains: Banking77, CLINC150 and CRAG; separate intent accuracy from grounded answer accuracy.
- True multi-source agent: transactional SQL queries, searchable document corpora and graph joins; authorization and freshness guards.
- Metrics: task success, ungrounded claims, expected calibration error, abstention risk/coverage, p50/p95 end-to-end latency, cost per successful answer, update freshness, reproducibility by seed and paired confidence intervals.
- Clearly preregister the primary outcome and hold test data untouched before changing policies.

See `paper/draft.md` for the IEEE-style preliminary manuscript (not submission-ready). README and paper deliberately do not claim state-of-the-art or universal improvement.
