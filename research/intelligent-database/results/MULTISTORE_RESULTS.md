# Multi-store exploratory benchmark — October 2026

The full test cases and run-time measurements are regenerated using `python multistore.py --out results/multistore.json`.

**Data:** 12 invented banking records and 12 manually authored test queries. These are not independent test samples.

| Approach | Correct /12 | Accuracy | Unauthorized or outdated retrieved |
|---|---:|---:|---:|
| Unrestricted lexical | 9 | 75.0% | 2 |
| Unrestricted sparse TF-IDF vector | 7 | 58.3% | 4 |
| Unrestricted hybrid | 8 | 66.7% | 3 |
| **Policy-aware hybrid** | **11** | **91.7%** | **0** |
| No graph / policy maintained | 11 | 91.7% | 0 |
| No policy / graph maintained | 9 | 75.0% | 3 |
| **Proposed policy + graph routing** | **12** | **100.0%** | **0** |

**Unit tests:** `python -m unittest -v test_multistore.py`: 6 passed. Includes tenant isolation, graph permission checks, freshness constraints, graph path traversal and audit verification.

**Integrity warning:** Only one additional query is answered correctly relative to the fair policy-aware hybrid baseline. These results do **not** demonstrate statistical significance, novelty, or real-world superiority. Sparse TF-IDF is not a dense neural embedding model; relationships are SQLite edge tuples, not a separate graph database. Do not describe the test as production banking data. Timings are runtime-sensitive and stored in regenerated JSON.

The follow-up study needs preregistered held-out real queries, policy-equivalent strong baselines, dense embeddings, separated graph store, cost/p95 latency, distribution shift, and ablations.
