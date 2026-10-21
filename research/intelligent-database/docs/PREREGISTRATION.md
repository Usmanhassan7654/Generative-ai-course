# PACE-DB Paper v1 — Preregistration (M0, frozen before any new M1/M2 experiments)

**Status:** PROPOSED — owner approval and independent audit pending. Recorded 2026-10-21 before any new paper-v1 study. Historical prototype re-executions in `progress/00_repo_audit.md` are diagnostic reproductions, not tests of this preregistered hypothesis.

## Primary falsifiable hypothesis (one sentence)
On held-out text-plus-structured multi-hop questions, a budgeted policy-equivalent PACE planner will achieve a higher **correct, fully supported answer rate over all eligible questions** than the strongest validation-selected fixed hybrid+rerank or SQL+graph baseline, with a paired 95% bootstrap confidence interval for the absolute difference entirely above zero.

**Failure criterion:** hypothesis fails unless the test-set PACE score exceeds the better of those two frozen baselines **and** the paired 95% confidence interval for that difference excludes zero on the positive side; equal/lower scores, interval overlapping zero, missing result, or materially different access to data all count as failure/non-confirmation. Do not replace failed hypothesis after test inspection.

## Primary outcome
Correct-and-supported answer rate (CSAR): fraction of eligible test queries for which final answer is correct under dataset gold answer **and** every material claim is supported by authorized, temporally valid returned evidence/citations; abstention and incorrect/unsupported answer count zero. Human adjudication protocol plus deterministic dataset match where possible; no gold labels at inference time.

## Secondary (report separately)
Answer EM/F1; supporting fact precision/recall/F1 and citation precision; unauthorized disclosure count and rate (separate synthetic policy stress set); stale evidence count; coverage and selective risk; p50/p95 wall latency; CPU time and RAM; network bytes/store calls; normalized cost and actual USD only if invoices exist; index lag; provenance correlation detection; calibration ECE/Brier; failure taxonomy. Thresholds optimized on validation only.

## Datasets / independent data
- **HotpotQA distractor** official train and development question/evidence annotations. Primary text multi-hop stratum; public test answers not available: split official training corpus by question-linked *source-article group* into train 70%/validation 15%/test 15%, frozen before training. Ensure source article IDs do not overlap groups when feasible; document overlap/exclusions and leakage checks. Do not assume the official dev set is entirely disjoint by article.
- **BIRD Mini-Dev / BIRD** with permitted download/license: structured SQL stratum, use official train/dev where available; freeze development IDs into validation/test deterministically by database ID (hold out whole databases). If insufficient databases, report this constraint and do not claim cross-database generalization. Use authorized executable SQL templates, never inject gold SQL.
- **Primary combined eligible evaluation:** predeclared equal-weight macro average of CSAR by HotpotQA and BIRD strata. If one dataset unavailable or licensing fails, do **not** silently replace it; preregistration amendment must be timestamped before running its test.
- **Images:** outside paper v1 primary claim; held out for later separately preregistered study.
- Security/freshness synthetic perturbation sets are stress tests, not substitutes for original dataset ground truth.

## Plans and baselines
SQL/FTS, BM25, pinned dense, BM25+dense+reranker, fixed SQL+graph (CTE), always-all-enabled, one-shot router, PACE verifier+escalation. See `BASELINES.md` for evidence/policy equivalence. Planner calibration and reranker training see train/val only; all baselines share identical canonical eligible facts, answer generator, time policies, model versions, indexing snapshots, context budgets, and accounting. All indexes derived from identical train-approved corpus; test answer labels are never indexed.

## Statistical procedure and replication
Five seeds (17, 23, 41, 59, 83) for model training, stochastic order and tie breaks, with a fixed frozen held-out test roster; cluster bootstrap at original article/database group level (10,000 resamples, two-sided 95% percentile CI) and paired permutation test with 10,000 swaps as sensitivity analysis. Report effect sizes/CI and all seeds, no seed cherry picking. Analysis unit is held-out question with clustering by parent dataset object. Repeated runs do not multiply effective sample size. Selection among fixed comparators occurs *only* on validation, not test. Primary alpha 0.05, a single preregistered primary comparison, no sequential peek.

## Integrity gate
No new experiment before freezing hashes of dataset manifest, code revision, scoring code, seeds, model versions, and final eligibility masks. Archive inference traces separately from gold answers. Record hardware, commands, raw stdout/stderr and failing runs. Reproduce from fresh checkout. **Publication outcome unknown.**

## Decisions needed from owner
Approval of paper-v1 hypothesis and dataset download/redistribution terms; compute budget; intended engineering repo location. Until approved this is an explicit *draft preregistration*, not an irrevocably registered public study.
