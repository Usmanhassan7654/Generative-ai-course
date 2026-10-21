# PACE-DB V8 — Bounded Event-Reconciliation Loop

**Status: executed synthetic research prototype, not a deployed database or validated novel contribution.**

## What changed from V7?

V7 refused to answer when SQL and document evidence disagreed. V8 retrieves an additional **independently generated carrier event**, cross-checks the event with at least one existing store, then returns an answer or abstains. This is an automatic, bounded (one escalation) reconciliation loop, not autonomous long-running agents or neural retrieval.

Four logical sources are held in SQLite: SQL record, document, graph edge, and event. This does **not** establish a real PostgreSQL/Qdrant/Neo4j deployment. The simulated text and graph values are direct lookup fields, not vector similarity or a graph query planner. All records are synthetic.

## Experiment design

- 600 test cases per seeded run, five independent random seeds (40–44).
- 50% status and 50% driver queries; ~12.5% intentionally unauthorized.
- SQL records corrupted randomly with probability 0.15; documents 0.24; graph edges 0.18; carrier events 0.06, with ~9% missing events. These are **experiment-author-chosen probabilities**, not measured field rates.
- Test ground truth is stored only in the benchmark evaluator, not provided to `decide`.
- Same exact source data and permission constraints for all approaches.
- Comparison: SQL-only, V7 (strict document/graph agreement), V8 (event reconciliation).
- Metrics: correct / eligible, accuracy on answered, coverage, assigned compute units. There is no monetary or measured latency cost.
- No neural image test in V8. Earlier image experiments remain in V5/V6 and should not be merged into this benchmark.

## Execute

```bash
python -m unittest discover -s tests -v
python v8.py --n 600 --out results/v8.json
```

Uses Python standard library only. Output contains five complete per-seed evaluations and event decision traces for review.

## Findings

See `results/v8.json`. Mean of five seeded runs:

| Method | Eligible query success | Accuracy when answered | Answer coverage | Modeled retrieval units/query |
|---|---:|---:|---:|---:|
| SQL-only | 83.70% | 83.70% | 87.50% | 1.000 |
| V7 | 53.87% | 99.01% | 47.60% | 3.363 |
| V8 | 90.44% | 98.38% | 80.43% | 4.947 |

V8 improves eligible query success by 6.74 percentage points compared with SQL-only, and 36.57 points compared with strict V7, **on this authored synthetic distribution only**. V8 remains more costly than both. V7 has the highest selective accuracy because it abstains more.

## Key limitations and threats to validity

- The event source has deliberately been simulated as highly reliable; V8's advantage depends strongly on that assumption. An event-ledger-only baseline and reliability sensitivity ablations must be added.
- Source errors may be artificially independent; in real systems errors can propagate from a common upstream event. Shared-source dependencies are not modeled.
- Tenant and clearance checks are filtering in a local simulator, not external service controls or a security penetration test.
- Integrity hashes identify the exact returned record representation; they **do not prove that the original record is true or independently sourced**.
- V8 can be confidently wrong when sources agree on the same incorrect fact; test for correlated failures is still required.
- Authored truth is an intentionally hidden evaluation label, not independently adjudicated ground truth.
- All policy-equivalent baselines could be made stronger; broad superiority, novelty, or AGI relevance has not been established.

## Next scientific milestone

Run a pre-registered benchmark with public real-world data, separate services, independent event signatures, latency measurements, correlated-error stress tests, event-first and retrieval-augmented baselines, and calibrated uncertainty. Any paper must report V8's extra cost and lower selective accuracy versus V7.
