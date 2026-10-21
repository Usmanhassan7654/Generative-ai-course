# PACE-DB V7 — independent-source evidence checks (experimental)

**Status:** Functional prototype, **not a novel database engine**, not a production deployment, and not AGI.

Run: `pip install -r requirements.txt && python -m unittest -v test_v7.py && python v7.py --out results/v7.json`.

Three logical stores in a single in-memory SQLite connection / Python process:
* `orders`: authoritative structured status, driver, tenant, timestamp, clearance.
* `docs`: independent text notices, indexed using scikit-learn TF-IDF.
* `edges`: relationships between order and driver, traversed through SQL.

The verifier starts from allowed structured evidence, gathers separately indexed textual evidence and graph evidence (when driver-related), compares consistency, and abstains on disagreement, lack of evidence, insufficient clearance, wrong tenant, or stale records. An audit trace contains selected ids, and hashes of returned evidence. Hashes are not cryptographic proof that sources are correct or independent.

The evaluation uses 240 **invented** order delivery records, controlled document corruptions (16% probability), stale notices (12%), corrupt graph connections (11%) and 40 deliberately unauthorized questions. It is a **sanity-check stress test** rather than independent scientific evidence. SQL is designated ground truth by construction. No neural image/graph embeddings, no model trained on held-out data, and no external PostgreSQL/Qdrant/Neo4j services. Costs are toy compute units and must not be represented as cloud expense. Results are deterministic for seed=41.

The SQL-only baseline is strongest for this artificially structured task. Text one-shot fails on driver-related questions because it retrieves a document field for a relation question—an intentionally weak baseline and not a valid claim about state-of-the-art systems. A fair research experiment would compare strong task-aware, policy-equivalent retrieval methods on real held-out evidence-rich tasks with disputed ground truth, separately measuring accuracy, abstention, latency, and cost.

### Next research tasks
1. Real multi-store deployment with independently maintained source data and ingestion metadata.
2. Real multimodal question answering benchmark with linked image/document/entity ground truth.
3. Adversarial source conflicts, freshness and security tests, randomized repeated runs.
4. Distinguish retrieval sufficiency, verified factual correctness and calibration; compare to strong policy-equivalent baselines.
