# PACE-DB V3 — falsifiable multi-store agent memory experiment

Status: **research implementation**. Local pure-Python policy planner and tests verified; Dockerized PostgreSQL/Qdrant/Neo4j wiring supplied, not verified in the authoring environment (no Docker daemon). No claim of AGI or originality established.

## Dataset decision
Primary: HotpotQA distractor dev: realistic multi-hop questions, labeled supporting facts (CC BY-SA 4.0). Structured complementary: BIRD Mini-Dev (execute SQL); temporal complementary: Meta CRAG (CC BY-NC 4.0, separate licensing). These are three distinct benchmarks and must **never** be merged into one score. No private customer data is distributed.

## Quick verification

```sh
python -m unittest discover -s tests -v
python -m pace.demo
```

## Three external databases

```sh
docker compose up -d
pip install -r requirements.txt
```

Postgres schema auto-initializes. For a full benchmark, load licensed public corpus into PostgreSQL, encode documents with a pinned sentence-transformer in Qdrant, and load vetted entity relationships into Neo4j. `pace/adapters.py` contains ingestion adapter functions; **the live cross-service query planner is not yet wired up**. Credentials in compose are DEVELOPMENT ONLY; never expose these ports to the internet.

## What is V3.2 here?
Policy gate enforces same-tenant access, minimum clearance, explicit time cutoff, and revalidates every result *after* graph expansion. Evidence receives a source pointer and hash; planner abstains when no permitted evidence is available. Retrieval is word-frequency sparse search locally (not neural embeddings); `Qdrant` adapter accepts dense embeddings but runtime is not validated.

## Measurement and publication caveats
Report answer EM/F1, supporting-fact EM/F1, citation validity, invalid evidence rate, refusal precision, p50/p95 latency and model/API cost against **policy-equivalent** BM25, dense retriever and hybrid baselines. Freeze evaluation labels and splits before changes. Avoid leaking gold supporting facts into the planner. A public dataset's standard questions **do not** contain tenant permission labels: any synthetic permission perturbations must be separately reported as a stress test, not original HotpotQA ground truth.

## Contribution to AGI research
The plausible long-term connection is **grounded, auditable, updatable external memory for general-purpose agents**. It does not establish AGI or general intelligence. Transfer across domains and task types should be tested explicitly.

## HotpotQA local passage retrieval evaluation

```sh
python -m pace.hotpot_eval --path datasets/hotpot_dev_distractor_v1.json --limit 100 --k 5
```

The dataset is not bundled; fetch from the official HotpotQA dataset repository / mirrors respecting CC BY-SA requirements. This simple test does not measure answer quality. Since the current planner does not construct independent entity edges from HotpotQA, the `pace` and `lexical` modes should yield the **same retrieval**; this is an expected negative control, not an improvement claim.
