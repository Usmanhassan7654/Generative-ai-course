# PACE-DB V4: Learned retrieval-route selection (exploratory)

This is a reproducible test of *automatic* route choice under equal, hard-coded access guards. It is not a new DBMS, not live PostgreSQL/Qdrant/Neo4j, and not a claim of AGI or publication-grade novelty.

## Run

```sh
pip install numpy scikit-learn
python -m unittest v4.test_router -v
python -m v4.benchmark --out results/v4_synthetic.json
```

The benchmark builds 30 evidence documents plus two forbidden/stale examples and 180 template-generated queries across 10 entities. 120 template-family questions train an intent-to-route classifier, while 60 questions from unseen templates evaluate exact keyed lookup, character TF-IDF search, graph-expanded TF-IDF, and learned routing. All methods enforce identical tenant, classification and freshness constraints before and after retrieval. Scores are **all required evidence retrieved**; no answer generation is measured.

## Results (local single run)

| Method | Hits/60 | Recall | Modeled cost/query |
|---|---:|---:|---:|
| Exact keyed lookup | 20 | 33.33% | 1.00 |
| Character TF-IDF | 22 | 36.67% | 2.00 |
| Graph expansion | 60 | 100.00% | 3.50 |
| Learned adaptive router | 55 | 91.67% | 2.29 |

Automatic router used 20 exact, 15 TF-IDF and 25 graph routes. Against always graph, it saves **34.52% in declared proxy cost** but misses 5 queries (−8.33 percentage points). These are invented weights (exact=1, semantic=2, graph=3.5), **not measured dollars or actual infrastructure consumption**. Adaptive median wall-clock time includes classifier inference and is not better than always graph on this small in-memory prototype. One run on synthetic data gives no external validity or uncertainty intervals.

## Known limitations

Synthetic phrase templates / shared entity distribution; the routing model is taught ideal strategies by answers on training questions. Character TF-IDF is **not** a neural embedding/vector DB. The graph is local adjacency; SQL is emulated as an exact-key lookup. Graph-expanded method benefits from generously connected synthetic records. Future work must use released datasets, real stores, fixed authorization rules for every baseline, p95 timing, cost instrumentation, repeated splits, OOD domains, multi-hop supporting-fact metrics and failure analysis.
