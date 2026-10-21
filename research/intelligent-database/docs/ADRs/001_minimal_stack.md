# ADR-001 — Choose minimal PostgreSQL stack first
**Status:** Proposed, awaiting owner approval. 2026-10-21.

## Decision
Build M1 on **PostgreSQL + pgvector + native full-text search + recursive CTEs**, plus FastAPI, migrations, and local file/object storage. Keep Qdrant and Neo4j behind typed adapters; do **not** require them to run M1. PostgreSQL is canonical, RLS mandatory. This deliberately challenges the handoff's default of deploying three external stores on day one.

## Why
One database preserves transaction boundaries, consistent permission and timestamp snapshots, observability and reproducibility without three separate identity/ACL implementations, CDC/dual writes, distributed backups, and three service availability failure modes. pgvector supplies dense approximate/exact similarity; FTS supplies lexical retrieval; recursive CTE gives bounded graph walks. A separate reranker remains an application-level component. Benchmark a simple strong implementation *first*. Qdrant/Neo4j are not independent evidence when they index PostgreSQL documents.

## Cost and complexity
Local MVP: one DB service + one API; minimum proposed developer laptop >= 16 GB RAM, >= 4 cores, ~20 GB free; CPU embeddings possible but slow. Approximate hosted testing budget $0–$100/month on local/free infrastructure or $50–$250/month for always-on small cloud services, **estimates only—not provider quotes or observed costs**. Three-store: >=3 persistence services + indexing workers, credentials, backups, monitored replication, reconciliation; variable cloud cost often substantially higher. Measure actual CPU-hours, memory, wall latency, operations, and invoices before making cost claims.

## When to introduce extra stores
**Qdrant:** predeclared volume/latency test: pinned pgvector at required recall@k and authorized filtering misses the published p95 service target by >=25% on >=100k embeddings and the Qdrant adapter meets recall/safety while improving p95 or memory/cost >=20% on same hardware. Results must be repeated on fresh index snapshots and policy filters.
**Neo4j:** realistic multi-hop query set shows CTE plan becomes costly or restrictive (e.g., >=25% higher p95 or >20% developer complexity proven by tracked maintenance tasks) and Neo4j matches RLS-equivalent graph visibility while producing reproducible benefits across seeds. No forced integration solely for presentation.

## Consequences
M1 vertical slice will be a *real running Postgres-backed product*, not proof of performance superiority. M2 can swap backends without changing Evidence/Plan contracts. Image ingestion will be later; paper v1 excludes images. Three independent stores are a later adapter benchmark, not M1 requirement. Need owner approval because handoff default preferred all three.
