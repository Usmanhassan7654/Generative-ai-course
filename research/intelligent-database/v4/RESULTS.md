# PACE-DB V4 — Learned retrieval routing

Status: exploratory synthetic benchmark. Code was locally implemented, 5 tests passed. The downloadable experiment bundle is the full reproducible run; this GitHub directory records the methodology and initial result.

## Experiment (21 October 2026)

- 10 synthetic business entities, 30 records, 2 forbidden/stale records.
- 180 template-generated queries (120 training / 60 held-out by template).
- Three candidate routes: exact keyed lookup, character TF-IDF, or TF-IDF followed by graph-neighbor expansion.
- Multinomial logistic regression trained to predict **the cheapest route that recovered all labeled evidence** in training.
- Every method applies the same tenant/clearance/freshness filter, including post-expansion.
- Success requires retrieving **all** required evidence IDs, not merely any related record.
- Five local unit tests passed.

| Method | Full-evidence success | Hits/60 | Cost units/query |
|---|---:|---:|---:|
| Exact only | 33.33% | 20 | 1.00 |
| TF-IDF only | 36.67% | 22 | 2.00 |
| Graph-expanded TF-IDF only | 100.00% | 60 | 3.50 |
| **Learned auto router** | **91.67%** | **55** | **2.29** |

Router selected 20 exact, 15 TF-IDF, 25 graph queries. Against the always-graph baseline: **8.33 percentage points worse accuracy**, **34.52% fewer assumed cost units**. Unit costs (1 / 2 / 3.5) are **model assumptions, not observed money, time, CPU or cloud charges**.

## Methodological limitations

This does **not** prove superiority over established retrieval systems. Queries are generated from hand-authored templates and split by template, not from independently collected human questions. TF-IDF does not use a neural embedding model; exact is an in-memory keyed lookup; graph relations are in-process. The fixed graph method always retrieves all required evidence on these constructed examples. This evaluation measures retrieval evidence completeness, not final factual answer accuracy or AGI capabilities. Timings are single-machine microbenchmarks and not production latencies.

## Next experiment

Evaluate on independent natural-language benchmark splits (HotpotQA passage and support-fact retrieval, BIRD text-to-SQL) with identical authorization rules for all methods, real PostgreSQL/Qdrant/Neo4j execution, calibrated fallback thresholds and observed latency/cost. A publishable claim will require multiple seeds, confidence intervals, stronger baselines and out-of-domain testing.
