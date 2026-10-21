# Phase 0: V1–V8 repository audit

**Scope and limitation:** Read complete engineering handoff. Examined all files in conversation-mounted V1–V8 ZIP bundles. Remote GitHub repository could not be cloned (`git ls-remote` DNS failure), so this is an **archive-complete but NOT verified remote-repository-complete** inventory. Any unlisted GitHub-only files remain unaudited. Environment: Python 3.13.5, Docker unavailable. Tests below were executed on local extracted archives, not fresh GitHub checkout.

## File inventory: purpose, runs, tests, reuse and known bugs

Legend: `runs` is confirmed only for explicitly named CLI/test in raw execution transcript below. Other `.py` files not independently executed. All reused ideas require security/code review. Historical outputs are not publication evidence.

### V1
**Purpose / known bugs:** Synthetic SQLite FTS, sparse TF-IDF, hybrid and rule-router. No live APIs or multi-DB; reusable methodology only.
**Executed:** 1 passed, 0 blocked/failed; see raw transcript. **Reusable:** selective source patterns; no deployment-ready modules certified.

| File (archive-relative) | Purpose | Run/test result | Reuse/known issue |
|---|---|---|---|
| `intelligent_db_prototype/README.md` | Explanation / paper draft | See v1 raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `intelligent_db_prototype/RESULTS.md` | Explanation / paper draft | See v1 raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `intelligent_db_prototype/benchmark.py` | Source / executable or test | See v1 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `intelligent_db_prototype/requirements.txt` | Config / workflow / dependency | See v1 raw output; not individually executed unless entrypoint | Requires pinning and CI verification |
| `intelligent_db_prototype/results/accuracy_comparison.png` | Result / generated sample | See v1 raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `intelligent_db_prototype/results/details.jsonl` | Result / generated sample | See v1 raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `intelligent_db_prototype/results/environment.json` | Result / generated sample | See v1 raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `intelligent_db_prototype/results/queries.jsonl` | Result / generated sample | See v1 raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `intelligent_db_prototype/results/summary.csv` | Result / generated sample | See v1 raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |

### V2A
**Purpose / known bugs:** Tiny banking-like intent classifier, audit CLI, paper draft. Classification proxy not real Bank77 test.
**Executed:** 2 passed, 0 blocked/failed; see raw transcript. **Reusable:** selective source patterns; no deployment-ready modules certified.

| File (archive-relative) | Purpose | Run/test result | Reuse/known issue |
|---|---|---|---|
| `intelligent_database_research/.github/workflows/bank77-benchmark.yml` | Config / workflow / dependency | See v2a raw output; not individually executed unless entrypoint | Requires pinning and CI verification |
| `intelligent_database_research/README.md` | Explanation / paper draft | See v2a raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `intelligent_database_research/app.py` | Source / executable or test | See v2a raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `intelligent_database_research/benchmark.py` | Source / executable or test | See v2a raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `intelligent_database_research/paper/draft.md` | Explanation / paper draft | See v2a raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `intelligent_database_research/paper/preliminary_ieee_manuscript.pdf` | Explanation / paper draft | See v2a raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `intelligent_database_research/paper/render_paper.py` | Source / executable or test | See v2a raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `intelligent_database_research/requirements.txt` | Config / workflow / dependency | See v2a raw output; not individually executed unless entrypoint | Requires pinning and CI verification |
| `intelligent_database_research/results/banking77.json` | Result / generated sample | See v2a raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `intelligent_database_research/results/local_smoke.json` | Result / generated sample | See v2a raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |

### V2B
**Purpose / known bugs:** Crafted 12-question synthetic multi-store/tenant simulation; safe fixture ideas, no live stores.
**Executed:** 2 passed, 0 blocked/failed; see raw transcript. **Reusable:** selective source patterns; no deployment-ready modules certified.

| File (archive-relative) | Purpose | Run/test result | Reuse/known issue |
|---|---|---|---|
| `intelligent_database_research/.github/workflows/bank77-benchmark.yml` | Config / workflow / dependency | See v2b raw output; not individually executed unless entrypoint | Requires pinning and CI verification |
| `intelligent_database_research/README.md` | Explanation / paper draft | See v2b raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `intelligent_database_research/app.py` | Source / executable or test | See v2b raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `intelligent_database_research/benchmark.py` | Source / executable or test | See v2b raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `intelligent_database_research/multistore.py` | Source / executable or test | See v2b raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `intelligent_database_research/paper/draft.md` | Explanation / paper draft | See v2b raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `intelligent_database_research/paper/preliminary_ieee_manuscript.pdf` | Explanation / paper draft | See v2b raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `intelligent_database_research/paper/render_paper.py` | Source / executable or test | See v2b raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `intelligent_database_research/requirements.txt` | Config / workflow / dependency | See v2b raw output; not individually executed unless entrypoint | Requires pinning and CI verification |
| `intelligent_database_research/results/audit.sqlite3` | Result / generated sample | See v2b raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `intelligent_database_research/results/local_smoke.json` | Result / generated sample | See v2b raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `intelligent_database_research/results/multistore.json` | Result / generated sample | See v2b raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `intelligent_database_research/test_multistore.py` | Source / executable or test | See v2b raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |

### V3
**Purpose / known bugs:** Sparse local evidence, graph adjacency, manual requires_multihop; external adapters unverified.
**Executed:** 2 passed, 1 blocked/failed; see raw transcript. **Reusable:** selective source patterns; no deployment-ready modules certified.

| File (archive-relative) | Purpose | Run/test result | Reuse/known issue |
|---|---|---|---|
| `pace_db_v3/.github/workflows/v3-checks.yml` | Config / workflow / dependency | See v3 raw output; not individually executed unless entrypoint | Requires pinning and CI verification |
| `pace_db_v3/README.md` | Explanation / paper draft | See v3 raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `pace_db_v3/docker-compose.yml` | Service configuration | See v3 raw output; not individually executed unless entrypoint | Docker absent; not live-verified |
| `pace_db_v3/pace/__init__.py` | Source / executable or test | See v3 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `pace_db_v3/pace/adapters.py` | Source / executable or test | See v3 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `pace_db_v3/pace/core.py` | Source / executable or test | See v3 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `pace_db_v3/pace/demo.py` | Source / executable or test | See v3 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `pace_db_v3/pace/hotpot_eval.py` | Source / executable or test | See v3 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `pace_db_v3/requirements.txt` | Config / workflow / dependency | See v3 raw output; not individually executed unless entrypoint | Requires pinning and CI verification |
| `pace_db_v3/results/demo.json` | Result / generated sample | See v3 raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `pace_db_v3/sql/001_schema.sql` | Config / workflow / dependency | See v3 raw output; not individually executed unless entrypoint | Requires pinning and CI verification |
| `pace_db_v3/tests/test_core.py` | Source / executable or test | See v3 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |

### V4
**Purpose / known bugs:** Synthetic automatic routing and modeled cost; graph fixed beats accuracy; no calibrated production costs.
**Executed:** 2 passed, 0 blocked/failed; see raw transcript. **Reusable:** selective source patterns; no deployment-ready modules certified.

| File (archive-relative) | Purpose | Run/test result | Reuse/known issue |
|---|---|---|---|
| `pace_db_v3/results/v4_synthetic.json` | Result / generated sample | See v4 raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `pace_db_v3/v4/README.md` | Explanation / paper draft | See v4 raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `pace_db_v3/v4/__init__.py` | Source / executable or test | See v4 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `pace_db_v3/v4/auto_router.py` | Source / executable or test | See v4 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `pace_db_v3/v4/benchmark.py` | Source / executable or test | See v4 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `pace_db_v3/v4/test_router.py` | Source / executable or test | See v4 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |

### V5
**Purpose / known bugs:** Digits/Iris proxy classifiers and same-source image augmentation retrieval, not independent visual QA.
**Executed:** 3 passed, 0 blocked/failed; see raw transcript. **Reusable:** selective source patterns; no deployment-ready modules certified.

| File (archive-relative) | Purpose | Run/test result | Reuse/known issue |
|---|---|---|---|
| `README.md` | Explanation / paper draft | See v5 raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `RESEARCH_LOG.md` | Explanation / paper draft | See v5 raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `experiment.py` | Source / executable or test | See v5 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `photos.py` | Source / executable or test | See v5 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `repeat.py` | Source / executable or test | See v5 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `requirements.txt` | Config / workflow / dependency | See v5 raw output; not individually executed unless entrypoint | Requires pinning and CI verification |
| `results/photos.json` | Result / generated sample | See v5 raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `results/repeated.json` | Result / generated sample | See v5 raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `results/results.json` | Result / generated sample | See v5 raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `tests/test_v5.py` | Source / executable or test | See v5 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |

### V6
**Purpose / known bugs:** Image-model consensus/abstain, not fact checking; near-duplicate photo evaluation.
**Executed:** 3 passed, 0 blocked/failed; see raw transcript. **Reusable:** selective source patterns; no deployment-ready modules certified.

| File (archive-relative) | Purpose | Run/test result | Reuse/known issue |
|---|---|---|---|
| `pace_db_v6/README.md` | Explanation / paper draft | See v6 raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `pace_db_v6/experiment.py` | Source / executable or test | See v6 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `pace_db_v6/photos_v6.py` | Source / executable or test | See v6 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `pace_db_v6/reference_v5/experiment.py` | Source / executable or test | See v6 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `pace_db_v6/reference_v5/photos.py` | Source / executable or test | See v6 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `pace_db_v6/requirements.txt` | Config / workflow / dependency | See v6 raw output; not individually executed unless entrypoint | Requires pinning and CI verification |
| `pace_db_v6/results/photos_v6.json` | Result / generated sample | See v6 raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `pace_db_v6/results/v6.json` | Result / generated sample | See v6 raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `pace_db_v6/tests/test_v6.py` | Source / executable or test | See v6 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |

### V7
**Purpose / known bugs:** Synthetic order delivery evidence; benchmark favors authoritative SQL.
**Executed:** 2 passed, 0 blocked/failed; see raw transcript. **Reusable:** selective source patterns; no deployment-ready modules certified.

| File (archive-relative) | Purpose | Run/test result | Reuse/known issue |
|---|---|---|---|
| `pace_db_v7/README.md` | Explanation / paper draft | See v7 raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `pace_db_v7/requirements.txt` | Config / workflow / dependency | See v7 raw output; not individually executed unless entrypoint | Requires pinning and CI verification |
| `pace_db_v7/results/v7.json` | Result / generated sample | See v7 raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `pace_db_v7/test_v7.py` | Source / executable or test | See v7 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `pace_db_v7/v7.py` | Source / executable or test | See v7 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |

### V8
**Purpose / known bugs:** Synthetic event reconciliation, author-selected source reliabilities; no live sources.
**Executed:** 2 passed, 0 blocked/failed; see raw transcript. **Reusable:** selective source patterns; no deployment-ready modules certified.

| File (archive-relative) | Purpose | Run/test result | Reuse/known issue |
|---|---|---|---|
| `README.md` | Explanation / paper draft | See v8 raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `RESEARCH_LOG.md` | Explanation / paper draft | See v8 raw output; not individually executed unless entrypoint | Background, claims unaudited |
| `results/v8.json` | Result / generated sample | See v8 raw output; not individually executed unless entrypoint | Historical only; data leakage or synthetic assumptions |
| `tests/test_v8.py` | Source / executable or test | See v8 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |
| `v8.py` | Source / executable or test | See v8 raw output; not individually executed unless entrypoint | Candidate; review security and assumptions |

## Diagnostic commands run and full raw stdout/stderr

These command executions are historical-code *audits*, not a newly preregistered paper-v1 experiment. Non-zero returns are preserved.

### v1: benchmark — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v1/intelligent_db_prototype`
Command `python benchmark.py --output /tmp/pace_m0_v1`
```text
records 1500 queries 520
{'method': 'SQL/FTS', 'query_type': 'all', 'n': 520, 'any_hit_at_5': 0.7923, 'normalized_recall_at_5': 0.7744, 'median_ms': 0.1621, 'p95_ms': 0.7822}
{'method': 'SQL/FTS', 'query_type': 'unseen_paraphrases', 'n': 48, 'any_hit_at_5': 0.625, 'normalized_recall_at_5': 0.625, 'median_ms': 0.5006, 'p95_ms': 0.6109}
{'method': 'Vector TF-IDF', 'query_type': 'all', 'n': 520, 'any_hit_at_5': 0.3192, 'normalized_recall_at_5': 0.3083, 'median_ms': 0.4223, 'p95_ms': 0.6153}
{'method': 'Vector TF-IDF', 'query_type': 'unseen_paraphrases', 'n': 48, 'any_hit_at_5': 0.625, 'normalized_recall_at_5': 0.625, 'median_ms': 0.4315, 'p95_ms': 0.5881}
{'method': 'Hybrid RRF', 'query_type': 'all', 'n': 520, 'any_hit_at_5': 0.8077, 'normalized_recall_at_5': 0.7808, 'median_ms': 0.8866, 'p95_ms': 1.4514}
{'method': 'Hybrid RRF', 'query_type': 'unseen_paraphrases', 'n': 48, 'any_hit_at_5': 0.625, 'normalized_recall_at_5': 0.625, 'median_ms': 1.1438, 'p95_ms': 1.3441}
{'method': 'Intelligent router', 'query_type': 'all', 'n': 520, 'any_hit_at_5': 0.9654, 'normalized_recall_at_5': 0.9654, 'median_ms': 0.0118, 'p95_ms': 0.3923}
{'method': 'Intelligent router', 'query_type': 'unseen_paraphrases', 'n': 48, 'any_hit_at_5': 0.625, 'normalized_recall_at_5': 0.625, 'median_ms': 0.4003, 'p95_ms': 0.6133}
```

### v2a: smoke — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v2a/intelligent_database_research`
Command `python benchmark.py --demo`
```text
{
  "results": [
    {
      "method": "word_tfidf_logistic",
      "n": 6,
      "accuracy": 0.833333,
      "macro_f1": 0.822222
    },
    {
      "method": "char_tfidf_logistic",
      "n": 6,
      "accuracy": 0.833333,
      "macro_f1": 0.822222
    },
    {
      "method": "hybrid_mean_probabilities",
      "n": 6,
      "accuracy": 0.833333,
      "macro_f1": 0.822222
    },
    {
      "method": "validation_gated_router",
      "n": 6,
      "accuracy": 0.833333,
      "macro_f1": 0.822222
    }
  ],
  "paired_gain": 0.0,
  "bootstrap_95_ci": [
    0.0,
    0.0
  ],
  "validation_gate_thresholds": {
    "word": 0.0,
    "char": 0.0
  },
  "selective": {
    "threshold": 0.44,
    "coverage": 0.6666666666666666,
    "accuracy_accepted": 1.0,
    "n_accepted": 4,
    "n_total": 6
  },
  "labels": 3,
  "data": {
    "train": 12,
    "validation": 6,
    "test": 6
  },
  "caveats": [
    "Classification benchmark, not end-to-end SQL/vector/graph query execution.",
    "TF-IDF character features are not dense neural embeddings.",
    "Abstention confidence is not calibrated and may fail under distribution shift.",
    "No public benchmark establishes novelty of this approach."
  ],
  "mode": "SMOKE_TEST_3_INTENTS_NOT_PUBLISHABLE"
}
```

### v2a: app — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v2a/intelligent_database_research`
Command `python app.py "When will my card arrive?" --demo --db /tmp/pace_m0_app.sqlite3`
```text
{
  "trace_id": "61d6a0a9-428f-4ae9-ba9e-b8fa04be81b0",
  "intent": "card_arrival",
  "confidence": 0.5701,
  "decision": "route_to_policy",
  "evidence": "char-ngram TF-IDF logistic model",
  "customer_data_accessed": false
}
```

### v2b: unit — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v2b/intelligent_database_research`
Command `python -m unittest -v test_multistore.py`
```text

[STDERR]
test_all_12_cases (test_multistore.MultiStoreSafetyTests.test_all_12_cases) ... ok
test_audit_trail (test_multistore.MultiStoreSafetyTests.test_audit_trail) ... ok
test_cross_tenant_isolation (test_multistore.MultiStoreSafetyTests.test_cross_tenant_isolation) ... ok
test_graph_cannot_cross_tenant (test_multistore.MultiStoreSafetyTests.test_graph_cannot_cross_tenant) ... ok
test_graph_path (test_multistore.MultiStoreSafetyTests.test_graph_path) ... ok
test_stale_record_excluded (test_multistore.MultiStoreSafetyTests.test_stale_record_excluded) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.082s

OK
```

### v2b: benchmark — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v2b/intelligent_database_research`
Command `python multistore.py --out /tmp/pace_m0_v2.json`
```text
[
  {
    "method": "lexical",
    "correct": 9,
    "n": 12,
    "accuracy": 0.75,
    "unauthorized_or_outdated_answers": 2,
    "stale_answers": 0,
    "median_ms": 0.5458
  },
  {
    "method": "vector",
    "correct": 7,
    "n": 12,
    "accuracy": 0.5833,
    "unauthorized_or_outdated_answers": 4,
    "stale_answers": 0,
    "median_ms": 0.5624
  },
  {
    "method": "hybrid",
    "correct": 8,
    "n": 12,
    "accuracy": 0.6667,
    "unauthorized_or_outdated_answers": 3,
    "stale_answers": 0,
    "median_ms": 0.4537
  },
  {
    "method": "policy_hybrid",
    "correct": 11,
    "n": 12,
    "accuracy": 0.9167,
    "unauthorized_or_outdated_answers": 0,
    "stale_answers": 0,
    "median_ms": 0.5871
  },
  {
    "method": "no_graph",
    "correct": 11,
    "n": 12,
    "accuracy": 0.9167,
    "unauthorized_or_outdated_answers": 0,
    "stale_answers": 0,
    "median_ms": 0.5094
  },
  {
    "method": "no_policy",
    "correct": 9,
    "n": 12,
    "accuracy": 0.75,
    "unauthorized_or_outdated_answers": 3,
    "stale_answers": 0,
    "median_ms": 0.6526
  },
  {
    "method": "proposed",
    "correct": 12,
    "n": 12,
    "accuracy": 1.0,
    "unauthorized_or_outdated_answers": 0,
    "stale_answers": 0,
    "median_ms": 0.6031
  }
]
```

### v3: unit — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v3/pace_db_v3`
Command `python -m unittest discover -s tests -v`
```text

[STDERR]
test_abstain (test_core.TestCore.test_abstain) ... ok
test_audit (test_core.TestCore.test_audit) ... ok
test_clearance (test_core.TestCore.test_clearance) ... ok
test_final_guard_even_diagnostic (test_core.TestCore.test_final_guard_even_diagnostic) ... ok
test_freshness (test_core.TestCore.test_freshness) ... ok
test_graph (test_core.TestCore.test_graph) ... ok
test_provenance (test_core.TestCore.test_provenance) ... ok
test_tenant (test_core.TestCore.test_tenant) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.001s

OK
```

### v3: demo — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v3/pace_db_v3`
Command `python -m pace.demo`
```text
{
  "evidence": [
    {
      "id": "a",
      "text": "The card was dispatched to the delivery service",
      "tenant": "A",
      "classification": 0,
      "observed_at": 1792582232,
      "source": "record",
      "parent": "card",
      "provenance": "demo/a",
      "sha256": "0c07765a9794b175e54928fa72d721a95db0bc25ab3153d262920974d194928c"
    },
    {
      "id": "b",
      "text": "The shipping provider tracking information is available",
      "tenant": "A",
      "classification": 0,
      "observed_at": 1792582232,
      "source": "document",
      "parent": "card",
      "provenance": "demo/b",
      "sha256": "7a4aa76efae45c3e476cbf022b2462dfbfac7599d0f69dad2f1d0da39140dc82"
    }
  ],
  "audit": {
    "query_sha256": "f032b27a9c40c95b73b8278fa0bafd6360c5e57b84d9e67425cb38e8a80c4a66",
    "tenant": "A",
    "candidate_count": 1,
    "allowed_count": 2,
    "returned_ids": [
      "a",
      "b"
    ],
    "abstained": false,
    "policy_checked": true,
    "mode": "pace",
    "elapsed_ms": 0.1135
  },
  "answer": "Evidence retrieved; generation not implemented"
}
```

### v3: hotpot_no_data — exit `1`
Working directory `/mnt/data/pace_phase0/audit_sources/v3/pace_db_v3`
Command `python -m pace.hotpot_eval --path /tmp/nonexistent_hotpot.json --limit 1`
```text

[STDERR]
Dataset not found. Download from official HotpotQA page; specify --path, or run --download in a networked environment.
```

### v4: unit — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v4/pace_db_v3`
Command `python -m unittest -v v4.test_router`
```text

[STDERR]
test_benchmark_full (v4.test_router.RouterTests.test_benchmark_full) ... ok
test_guard_on_graph_neighbor (v4.test_router.RouterTests.test_guard_on_graph_neighbor) ... ok
test_stale_exclusion (v4.test_router.RouterTests.test_stale_exclusion) ... ok
test_tenant_isolation (v4.test_router.RouterTests.test_tenant_isolation) ... ok
test_train_predict (v4.test_router.RouterTests.test_train_predict) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.349s

OK
```

### v4: benchmark — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v4/pace_db_v3`
Command `python -m v4.benchmark --out /tmp/pace_m0_v4.json`
```text
{
  "train_n": 120,
  "test_n": 60,
  "metrics": {
    "exact": {
      "n": 60,
      "all_required_evidence_recall": 0.3333333333333333,
      "mean_cost_units": 1.0,
      "median_ms": 0.011167,
      "p95_ms": 0.012258,
      "route_counts": {
        "exact": 60,
        "semantic": 0,
        "graph": 0
      },
      "by_query_family": {
        "exact": 1.0,
        "semantic": 0.0,
        "graph": 0.0
      }
    },
    "semantic": {
      "n": 60,
      "all_required_evidence_recall": 0.36666666666666664,
      "mean_cost_units": 2.0,
      "median_ms": 0.429295,
      "p95_ms": 0.621244,
      "route_counts": {
        "exact": 0,
        "semantic": 60,
        "graph": 0
      },
      "by_query_family": {
        "exact": 0.1,
        "semantic": 1.0,
        "graph": 0.0
      }
    },
    "graph": {
      "n": 60,
      "all_required_evidence_recall": 1.0,
      "mean_cost_units": 3.5,
      "median_ms": 0.4126755,
      "p95_ms": 0.590597,
      "route_counts": {
        "exact": 0,
        "semantic": 0,
        "graph": 60
      },
      "by_query_family": {
        "exact": 1.0,
        "semantic": 1.0,
        "graph": 1.0
      }
    },
    "adaptive": {
      "n": 60,
      "all_required_evidence_recall": 0.9166666666666666,
      "mean_cost_units": 2.2916666666666665,
      "median_ms": 0.6557405000000001,
      "p95_ms": 0.929527,
      "route_counts": {
        "exact": 20,
        "semantic": 15,
        "graph": 25
      },
      "by_query_family": {
        "exact": 1.0,
        "semantic": 1.0,
        "graph": 0.75
      }
    }
  }
}
```

### v5: unit — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v5`
Command `python -m unittest discover -s tests -v`
```text

[STDERR]
test_all_predictions_accounted_for (test_v5.TestV5.test_all_predictions_accounted_for) ... ok
test_disjoint_split (test_v5.TestV5.test_disjoint_split) ... ok
test_every_route_has_audit_trace (test_v5.TestV5.test_every_route_has_audit_trace) ... ok
test_no_ground_truth_in_attempts (test_v5.TestV5.test_no_ground_truth_in_attempts) ... ok
test_photos_count (test_v5.TestV5.test_photos_count) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.953s

OK
```

### v5: photo — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v5`
Command `python photos.py --out /tmp/pace_m0_v5photos.json`
```text
{
  "dataset": "scikit-image sample photographs and images",
  "n_originals": 14,
  "n_validation_augmented": 56,
  "n_test_augmented": 56,
  "task": "retrieve SAME SOURCE image after transformations; not caption/image-semantic search",
  "training_and_test_separation": "same image corpus; augmentation random seeds differ, so NOT held-out source photographs",
  "threshold": 0.01,
  "cost_proxy": {
    "color": 1,
    "spatial": 3,
    "combined": 4,
    "loop": 1.0
  },
  "accuracy": {
    "color": 0.9464285714285714,
    "spatial": 1.0,
    "combined": 1.0,
    "loop": 0.9464285714285714
  },
  "escalations": 0
}
```

### v5: experiment — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v5`
Command `python experiment.py --out /tmp/pace_m0_v5.json`
```text
{
  "digits": {
    "n": 450,
    "metrics": {
      "fast_only": {
        "accuracy": 0.9533333333333334,
        "correct": 429,
        "n": 450,
        "cost_proxy": 1.0
      },
      "full_only": {
        "accuracy": 0.9866666666666667,
        "correct": 444,
        "n": 450,
        "cost_proxy": 3.0
      },
      "strong_only": {
        "accuracy": 0.9888888888888889,
        "correct": 445,
        "n": 450,
        "cost_proxy": 8.0
      },
      "loop": {
        "accuracy": 0.9844444444444445,
        "correct": 443,
        "n": 450,
        "cost_proxy": 1.448888888888889
      },
      "single_route": {
        "accuracy": 0.9844444444444445,
        "correct": 443,
        "n": 450,
        "cost_proxy": 1.2755555555555556
      }
    },
    "route_counts": {
      "fast": 388,
      "full": 60,
      "strong": 2
    },
    "calibration": {
      "t_fast": 0.72,
      "t_full": 0.57,
      "validation_accuracy": 0.9851632047477745,
      "validation_strong_accuracy": 0.9881305637982196,
      "validation_proxy_cost": 1.4391691394658754,
      "selection_objective": "minimum proxy cost while accuracy within 1pp of strong baseline on validation"
    }
  },
  "iris": {
    "n": 38,
    "metrics": {
      "fast_only": {
        "accuracy": 0.9210526315789473,
        "correct": 35,
        "n": 38,
        "cost_proxy": 1.0
      },
      "full_only": {
        "accuracy": 0.9736842105263158,
        "correct": 37,
        "n": 38,
        "cost_proxy": 3.0
      },
      "strong_only": {
        "accuracy": 0.9473684210526315,
        "correct": 36,
        "n": 38,
        "cost_proxy": 8.0
      },
      "loop": {
        "accuracy": 0.9210526315789473,
        "correct": 35,
        "n": 38,
        "cost_proxy": 1.0
      },
      "single_route": {
        "accuracy": 0.9210526315789473,
        "correct": 35,
        "n": 38,
        "cost_proxy": 1.0
      }
    },
    "route_counts": {
      "fast": 38,
      "full": 0,
      "strong": 0
    },
    "calibration": {
      "t_fast": 0.57,
      "t_full": 0.57,
      "validation_accuracy": 0.9642857142857143,
      "validation_strong_accuracy": 0.9642857142857143,
      "validation_proxy_cost": 1.0,
      "selection_objective": "minimum proxy cost while accuracy within 1pp of strong baseline on validation"
    }
  }
}
```

### v6: unit — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v6/pace_db_v6`
Command `python -m unittest discover -s tests -v`
```text

[STDERR]
test_abstention (test_v6.TestVerifier.test_abstention) ... ok
test_agreement (test_v6.TestVerifier.test_agreement) ... ok
test_disagreement_escalation (test_v6.TestVerifier.test_disagreement_escalation) ... ok
test_no_label_access (test_v6.TestVerifier.test_no_label_access) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
```

### v6: photo — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v6/pace_db_v6`
Command `python photos_v6.py --out /tmp/pace_m0_v6photo.json`
```text
{
  "dataset": "14 scikit-image sample photographs with augmentation; source images occur in reference set",
  "n": 56,
  "counts": {
    "color": 53,
    "spatial": 56,
    "combined": 56,
    "v6": 56
  },
  "accuracy": {
    "color": 0.9464285714285714,
    "spatial": 1.0,
    "combined": 1.0,
    "v6": 1.0
  },
  "coverage": 1.0,
  "abstentions": 0,
  "limitations": [
    "Same source images in gallery, augmented queries only",
    "Feature agreement is not independent provenance and is not an image-language model",
    "No train/test photo identity isolation",
    "Images are loaded from scikit-image at runtime, not included in repository"
  ]
}
```

### v6: experiment — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v6/pace_db_v6`
Command `python experiment.py --out /tmp/pace_m0_v6.json`
```text
{
  "digits": {
    "fast": {
      "accuracy": 0.9533333333333334
    },
    "full": {
      "accuracy": 0.9866666666666667
    },
    "strong": {
      "accuracy": 0.9888888888888889
    },
    "v5": {
      "accuracy": 0.9844444444444445,
      "proxy_cost": 1.448888888888889
    },
    "v6": {
      "coverage": 0.9955555555555555,
      "selective_accuracy": 0.9933035714285714,
      "end_to_end_accuracy_with_abstentions_wrong": 0.9888888888888889,
      "abstentions": 2,
      "proxy_cost": 4.408888888888889
    }
  },
  "iris": {
    "fast": {
      "accuracy": 0.9210526315789473
    },
    "full": {
      "accuracy": 0.9736842105263158
    },
    "strong": {
      "accuracy": 0.9473684210526315
    },
    "v5": {
      "accuracy": 0.9210526315789473,
      "proxy_cost": 1.0
    },
    "v6": {
      "coverage": 1.0,
      "selective_accuracy": 0.9473684210526315,
      "end_to_end_accuracy_with_abstentions_wrong": 0.9473684210526315,
      "abstentions": 0,
      "proxy_cost": 4.421052631578948
    }
  }
}
```

### v7: unit — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v7/pace_db_v7`
Command `python -m unittest -v test_v7.py`
```text

[STDERR]
test_conflicting_doc (test_v7.Tests.test_conflicting_doc) ... ok
test_conflicting_graph (test_v7.Tests.test_conflicting_graph) ... ok
test_cross_tenant (test_v7.Tests.test_cross_tenant) ... ok
test_evaluation (test_v7.Tests.test_evaluation) ... ok
test_expired (test_v7.Tests.test_expired) ... ok
test_provenance (test_v7.Tests.test_provenance) ... ok
test_valid (test_v7.Tests.test_valid) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.049s

OK
```

### v7: benchmark — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v7/pace_db_v7`
Command `python v7.py --n 24 --out /tmp/pace_m0_v7.json`
```text
{
  "setup": {
    "records": 24,
    "queries": 24,
    "seed": 41,
    "data": "synthetic",
    "real_external_databases": false
  },
  "methods": {
    "sql_only": {
      "correct": 20,
      "answered": 20,
      "abstained": 4,
      "unauthorized_answers": 0,
      "selective_accuracy": 1.0,
      "end_to_end_success": 0.8333,
      "coverage": 0.8333,
      "mean_modeled_cost": 1.0,
      "abstention_causes": {
        "no_authorized_current_record": 4
      }
    },
    "one_shot": {
      "correct": 9,
      "answered": 17,
      "abstained": 7,
      "unauthorized_answers": 0,
      "selective_accuracy": 0.5294,
      "end_to_end_success": 0.375,
      "coverage": 0.7083,
      "mean_modeled_cost": 2.667,
      "abstention_causes": {
        "no_authorized_current_record": 4,
        "unknown": 3
      }
    },
    "verified": {
      "correct": 11,
      "answered": 11,
      "abstained": 13,
      "unauthorized_answers": 0,
      "selective_accuracy": 1.0,
      "end_to_end_success": 0.4583,
      "coverage": 0.4583,
      "mean_modeled_cost": 3.0,
      "abstention_causes": {
        "no_authorized_current_record": 4,
        "sql_document_disagreement": 6,
        "missing_independent_document": 3
      }
    }
  },
  "failures": {}
}
```

### v8: unit — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v8`
Command `python -m unittest discover -s tests -v`
```text

[STDERR]
test_clearance_abstains (test_v8.Tests.test_clearance_abstains) ... ok
test_cross_tenant_abstains (test_v8.Tests.test_cross_tenant_abstains) ... ok
test_graph_disagreement_escalation (test_v8.Tests.test_graph_disagreement_escalation) ... ok
test_matching_quorum (test_v8.Tests.test_matching_quorum) ... ok
test_reconcile_sql_error (test_v8.Tests.test_reconcile_sql_error) ... ok
test_reproducibility (test_v8.Tests.test_reproducibility) ... ok
test_stale_event_abstains (test_v8.Tests.test_stale_event_abstains) ... ok
test_unsubstantiated_event_abstains (test_v8.Tests.test_unsubstantiated_event_abstains) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.007s

OK
```

### v8: benchmark — exit `0`
Working directory `/mnt/data/pace_phase0/audit_sources/v8`
Command `python v8.py --n 24 --out /tmp/pace_m0_v8.json`
```text
{
  "sql": {
    "eligible_success": {
      "mean": 0.7905,
      "min": 0.7143,
      "max": 0.8571
    },
    "answered_accuracy": {
      "mean": 0.7905,
      "min": 0.7143,
      "max": 0.8571
    },
    "coverage": {
      "mean": 0.875,
      "min": 0.875,
      "max": 0.875
    },
    "cost_per_query_modeled": {
      "mean": 1.0,
      "min": 1.0,
      "max": 1.0
    }
  },
  "v7": {
    "eligible_success": {
      "mean": 0.5238,
      "min": 0.4286,
      "max": 0.6667
    },
    "answered_accuracy": {
      "mean": 0.9633,
      "min": 0.9,
      "max": 1.0
    },
    "coverage": {
      "mean": 0.475,
      "min": 0.4167,
      "max": 0.5833
    },
    "cost_per_query_modeled": {
      "mean": 3.2668,
      "min": 3.167,
      "max": 3.417
    }
  },
  "v8": {
    "eligible_success": {
      "mean": 0.8857,
      "min": 0.8571,
      "max": 0.9048
    },
    "answered_accuracy": {
      "mean": 0.9604,
      "min": 0.9048,
      "max": 1.0
    },
    "coverage": {
      "mean": 0.8083,
      "min": 0.75,
      "max": 0.875
    },
    "cost_per_query_modeled": {
      "mean": 4.95,
      "min": 4.625,
      "max": 5.125
    }
  }
}
```

## Historical metric registry — classification and prohibition on reuse as research evidence

| Historical result | Type | Limitation |
|---|---|---|
| V1 96.54% any-hit@5 router vs 80.77% hybrid, 520 questions, +15.77 pp; unseen paraphrases both 62.5% | Synthetic | Familiar templated queries; no generalization, differing machine latency |
| V2a 83.33% on six questions, equal among methods | Proxy / authored | Not real Banking77 nor multi-database |
| V2b 12/12 proposed versus 11/12 policy-hybrid; six tests | Synthetic | Authored questions, SQLite/in-memory logical stores |
| V3 8/8 tests; 3 external store adapters | Synthetic functional; unverified deployment | Graph flag manually set, HotpotQA missing, no live store integration |
| V4 55/60 91.67% adaptive vs 60/60 graph, 34.5% fewer assigned cost units | Synthetic | Learned route proxy, cost not actual dollars |
| V5 digits 443/450 98.44% vs fixed 445/450 98.89%, Iris 35/38 92.11%; 53/56 photo augmented | Real public data, **proxy model classification/near-duplicate** | Not end-to-end database or image QA; photo originals shared |
| V6 digits 445/450 98.89%, Iris 36/38 94.74%, photos 56/56 | Real public data, **proxy ensemble and transformed-image retrieval** | Agreement not provenance truth; photo duplicates |
| V7 146/240 correct with verifier vs 200/240 SQL, 7/7 tests | Synthetic | SQL ground-truth advantaged |
| V8 five seeds × 600 scenarios: V8 90.44% eligible success vs SQL 83.70%, V7 53.87%; 8/8 tests, cost 4.95 units | Synthetic | Author-selected error distributions and source reliability; proxy cost |
| HotpotQA, BIRD, CRAG and ScienceQA evaluation scores | **Not measured** | Cannot claim real test success |
| Working live PostgreSQL+Qdrant+Neo4j system | **Not verified** | No live integrated runtime |

## Raw environment blockers
```text
$ git ls-remote https://github.com/Usmanhassan7654/Generative-ai-course.git HEAD
fatal: unable to access 'https://github.com/Usmanhassan7654/Generative-ai-course.git/': Could not resolve host: github.com
$ command -v docker
(no output)
$ python -V
Python 3.13.5
```

## Known defects requiring follow-up
- No clone/build/run confirmation for remote GitHub state; archived bundle inventory could be incomplete.
- Missing external HotpotQA dataset (`hotpot_no_data` exit 1 above); no independent benchmark execution.
- No external Postgres/Qdrant/Neo4j live calls validated, persistent RLS or service recovery.
- Gold-label correlation risk in authored synthetic scenarios; photo duplicate-source leakage; modeled costs incorrectly attractive if quoted as real.
- `Evidence` hashes assert byte identity, not correctness/independence; verify origin and provenance explicitly.

## DECISIONS NEEDED
Approve repo path, PostgreSQL-first ADR, primary data license/hypothesis/compute, and Docker-capable execution runner. STOP before feature code.
