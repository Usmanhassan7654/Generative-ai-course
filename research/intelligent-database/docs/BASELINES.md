# Paper v1 baselines: identical policy/evidence envelope

## Common non-negotiable experimental contract
For query q and authenticated principal p at time t, a single policy oracle constructs **E(q,p,t)**: canonical record IDs with tenant match, row-level/field-level permission, valid-time eligibility and visibility. Every retriever and reranker operates only on E, with identity bound server-side; output evidence is *again* checked against E. All indices reflect the same canonical snapshot watermark. All methods receive same query, question image access (none in v1), permitted metadata fields, token budget, answer generator and prompt template, model snapshot and decoding, max_k per call and maximum total context bytes. A baseline without SQL interface may return nothing for exact SQL-only facts; it is not secretly granted gold SQL. PACE cannot access any gold answer, supporting labels, unpermitted record, or future event. ACL/freshness metadata is available equally for filtering, but benchmark correctness labels only in scoring. The policy oracle is outside the planner so every method must comply.

| Method | Available evidence and strategy | Permission rule | Generator and charge |
|---|---|---|---|
| SQL / PostgreSQL FTS | E records with exact joins + tsvector full text + fixed query templates | RLS + adapter filters + final E check | Same pinned generator, actual calls/CPU/latency |
| BM25 | Same eligible text excerpts in E, lexical ranking | pre-filter eligible IDs and final E | Same generator, count lexical index, context |
| Dense | Same eligible excerpts encoded by one frozen encoder | payload/ID filter before scoring and final E | Same generator, embedding and retrieval cost |
| Hybrid + rerank | BM25+dense from E, reranker on same candidate budget | same triple gate | same generator, reranker inference cost counted |
| Fixed SQL + graph | Exact SQL + recursive CTE over edges whose endpoints in E | per-hop tenant/ACL + final E | same generator, traversal execution counted |
| Always all stores | Execute all enabled eligible plans, fuse up to common context limit | each method restricted to E, no leaked union | same generator, charge every call and fusion |
| One-shot learned router | Validation-trained decision between eligible plan methods, no retries | same E and gate | same generator, classifier cost counted |
| PACE | Validation-trained routing + bounded independent-evidence verifier/escalation | same E, gate every round and before output | same generator, all rounds/verifier cost counted |

## Written policy-equivalence proof (conditional, to be verified with tests)
Let `A(m,q)` be records seen or returned by method m. Each retriever constructs candidates using only IDs in E; graph traversal intersects both starting nodes and every neighbor with E; rerankers and generators receive only authorized candidate texts. Every output record is post-filtered against E at the as-of time. Therefore `A(m,q) ⊆ E(q,p,t)` for every method **provided** the adapters enforce the filters and authorization context is immutable. This is a design argument, **not a measured security proof**. Tests must assert the subset invariant on malicious documents, graph paths, cache hits, stale vector IDs, missing identity, expired access, revocation under index lag, and backend failure, for each method. We must also validate equality of policy *opportunity* (all eligible records indexed, same max-age snapshot), not merely zero observed leaks.

## Measured cost accounting
Separate (a) real wall-clock p50/p95 and hardware; (b) per backend call counts, CPU/GPU time, memory and token counts; (c) actual dollar spending *only* from provider invoices; and (d) assigned proxy weights **clearly labeled synthetic modeled cost**. Baselines receive the same timeout, maximum rounds allowance (one-shot has one by definition), and total query budget; if a method exceeds budget, it abstains and is counted accordingly. Report any persistent warm cache effects and indexing costs independently. Avoid an unfair comparator that intentionally violates permissions.
