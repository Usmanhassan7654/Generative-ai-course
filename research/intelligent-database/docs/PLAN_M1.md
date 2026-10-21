# M1 smallest vertical slice — draft awaiting owner decisions

## Goal / exit
A real HTTP application, with authenticated identity provided server-side, that ingests a small licensed *text + structured* corpus into one PostgreSQL source of truth, uses Postgres FTS + pgvector + recursive CTEs on actual service calls, returns valid Evidence/QueryTrace, and passes tenant/time/lineage security tests. No neural intelligent-planner superiority claim and no image implementation in paper v1.

## Planned directory and files (no feature code written in Phase 0)
```
pace-db/
  compose.yaml                    # postgres with pgvector, api, worker, healthchecks
  .env.example                    # never commit live credentials
  pyproject.toml                  # pinned deps incl fastapi,pydantic2,sqlalchemy,psycopg,alembic,pgvector,pytest
  app/main.py                     # /health/live, /health/ready, POST /v1/query, POST /v1/ingest
  app/auth.py                     # verified subject -> tenant/clearance server-side
  app/schemas.py                  # Pydantic from docs/SCHEMAS.md
  app/policy.py                   # tenant/ACL/current-at timestamp, fail closed
  app/adapters/postgres.py       # parameterized SQL, FTS, pgvector, bounded CTE
  app/ingestion/loader.py         # licensed corpus + synthetic security fixtures
  app/ingestion/outbox.py         # version/watermark, idempotent replay
  app/planner/fixed.py            # fixed safe routing, NOT learned V4 reuse
  app/verifier/gate.py            # sufficient slots, authority and provenance
  app/observability.py            # trace audit no sensitive plaintext
  migrations/versions/0001.py    # tenants, principals, docs, evidence, links, outbox, trace tables + RLS
  datasets/manifests/hotpot.json  # license, hashes, split IDs (not raw copyrighted data)
  scripts/bootstrap.sh
  scripts/test_m1.sh
  tests/unit/test_contracts.py
  tests/integration/test_ingest_query.py
  tests/security/test_rls.py
  tests/integration/test_outbox_replay.py
  tests/e2e/test_demo.py
  docs/progress/01_m1.md
```

## Services
- Required: PostgreSQL with pgvector extension; FastAPI service; ingestion/replay worker. Local version-pinned Docker Compose with healthchecks and persistent volume. No Qdrant/Neo4j yet under ADR-001; adapters are interface stubs only, **not fake successes**.
- Optional external: local folder raw text store. LLM generation disabled initially; return ranked evidence with deterministic derived answer on exact queries. All citations must resolve to ingested evidence.

## Operator commands (targets; NOT executed in Phase 0)
```
cp .env.example .env
docker compose up --build -d
docker compose ps
python -m app.ingestion.loader --manifest datasets/manifests/hotpot.json --subset 100
curl -fsS http://localhost:8000/health/ready
curl -fsS -X POST http://localhost:8000/v1/query -H 'Authorization: Bearer <development-token>' -H 'Content-Type: application/json' -d '{"query":"Where is order 893?"}'
pytest -q tests/unit tests/integration tests/security tests/e2e
```
All commands are planned; they are not evidence until accompanied by raw output from an actual integrated deployment.

## M1 acceptance gates
1. Fresh clone and single documented bootstrap gives `/health/ready` 200 with DB reachable; restart retains data; all real services logged with container IDs/health.
2. Tenant-scoped insert, exact lookup, FTS, dense pgvector query and recursive CTE produce actual SQL traces; no hardcoded fixture response.
3. Unauthorized/expired/stale/revoked records excluded by enforced DB RLS and final policy gate, including graph edges and vector retrieval. Zero disclosed in >100 adversarial tests, but never interpret finite tests as global zero-risk proof.
4. Deterministic idempotent ingest, provenance lineage, source hash, outbox replay and watermark verified, including failure injection and stale index handling.
5. JSON request/response validate Pydantic v2 contract; no client-controlled `tenant_id`; evidence IDs/citations stable; `max_rounds` bounded.
6. Measured p50/p95 latency, query error rate, CPU/RAM, ingest throughput; no arbitrary fake price/cost. Log raw command/output, git SHA, dataset/model hashes.
7. Run one basic independently held-out text+structured evaluation only after preregistration approved/frozen. Failures reported prominently.

## Risk register
| Risk | Impact | Mitigation / test |
|---|---|---|
| Permission bypass via owner role, SQL functions or vector indexes | Critical | RLS FORCE where applicable, non-owner restricted DB role, adversarial tenant tests |
| Label/gold leakage to router | Publication invalidity | Locked test corpus, split manifest, no answer in ingest/search at inference |
| Index lag and stale evidence | Wrong answers | outbox watermark and strict `as_of`, fail closed when lag beyond bound |
| Dataset license or download unavailable | Blocks integration | approved public dataset manifest; no silent replacement |
| pgvector extension unavailable on user's machine | Blocks startup | pin image and local smoke preflight before M1 |
| Novelty not established | Paper rejection | separate prior-art evidence review; publish negative results |
| Over-budget embeddings CPU inference | Slow deployment | pin small encoder, cache vectors with source versions, measure actual timing |
| Missing Docker/network on current runtime | Cannot validate M1 here | owner-supplied Linux/CI runner with Docker, avoid claiming deployment success |

## Compute and cost estimate (NOT a quote or experiment result)
Local development: 4+ vCPU, 16 GB RAM, 20–40 GB free, CPU embeddings small corpus; free open-source services aside from electricity and operator time. If hosted, exploratory $25–$200/month small DB/app hosting **planning range only**; costs depend on RAM/compute/storage region and continuous runtime; paid LLM excluded. M1 likely 2–5 engineer-days after infrastructure, policy and dataset decisions, but effort estimate is not a delivery guarantee.

## DECISIONS NEEDED — STOP before feature code
1. Owner approve PostgreSQL-first ADR (rather than required three stores from old handoff).
2. Approve current repository research-branch path vs new `pace-db` repository; GitHub connector does not expose create-repository in this environment.
3. Approve paper v1 dataset licensing/manifests, hypothesis and compute budget.
4. Provide Docker-capable runner / machine or grant appropriate execution context for real M1 acceptance testing.
