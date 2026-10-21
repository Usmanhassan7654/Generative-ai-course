# Typed contracts — Pydantic v2 (proposal, M0)

All UTC timestamps timezone-aware; strings non-empty; IDs stable. Invariant checks, server identity enforcement, SHA checking, and lineage DAG cycle checks belong to policy/data services beyond type validation. This is intended executable schema source for M1; not yet imported by a running API.

```python
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, model_validator

class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

class Evidence(Strict):
    evidence_id: UUID
    source_record_id: str = Field(min_length=1)
    source_type: Literal['sql','text','image','graph','event']
    tenant_id: str = Field(min_length=1)
    object_uri: str | None = None
    text_excerpt: str | None = None
    entity_ids: list[str]
    observed_at: datetime
    effective_at: datetime
    ingested_at: datetime
    expires_at: datetime | None = None
    visibility: Literal['public','internal','restricted']
    acl_policy_id: str
    source_system: str
    source_authority: Literal['authoritative','derived','untrusted']
    origin_id: str
    parent_evidence_ids: list[UUID] = Field(default_factory=list)
    content_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    embedding_model_version: str | None = None
    index_watermark: str | None = None
    retrieval_score: float | None = None
    rank: int | None = Field(default=None, ge=1)
    source_location: dict[str, str]

class Plan(Strict):
    plan_id: UUID
    query_id: UUID
    round_number: int = Field(ge=1, le=3)
    strategy: Literal['sql','fts','bm25','dense','hybrid','graph','sql_graph']
    backend: str
    reason_code: str
    required_slots: list[str]
    allowed_tenant_id: str
    policy_version: str
    as_of: datetime
    max_age_seconds: int = Field(ge=0)
    top_k: int = Field(gt=0, le=100)
    timeout_ms: int = Field(gt=0)
    estimated_cost_units: float = Field(ge=0)
    depends_on_evidence_ids: list[UUID] = Field(default_factory=list)

class VerifierResult(Strict):
    query_id: UUID
    sufficient: bool
    conflicts: list[str]
    missing_slots: list[str]
    accepted_evidence_ids: list[UUID]
    rejected_evidence_ids: list[UUID]
    independent_origin_ids: list[str]
    policy_passed: bool
    freshness_passed: bool
    decision: Literal['answer','escalate','abstain','deny']
    reason_code: str
    @model_validator(mode='after')
    def enforce_gate(self):
        if self.decision == 'answer' and (not self.sufficient or not self.policy_passed or not self.freshness_passed or self.conflicts):
            raise ValueError('Answer requires sufficient, current, authorized, conflict-free evidence')
        return self

class QueryTrace(Strict):
    trace_id: UUID
    query_id: UUID
    principal_subject_hash: str = Field(pattern=r'^[0-9a-f]{64}$')
    tenant_id: str
    query_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    started_at: datetime
    finished_at: datetime
    policy_version: str
    plan_ids: list[UUID]
    returned_evidence_ids: list[UUID]
    final_decision: Literal['answered','abstained','denied','error']
    store_calls: int = Field(ge=0)
    elapsed_ms: float = Field(ge=0)
    cpu_ms: float | None = Field(default=None, ge=0)
    measured_usd: float | None = Field(default=None, ge=0)
    error_codes: list[str]
```

## Valid JSON examples (UUIDs are illustrative, hashes 64 lowercase hexadecimal chars)

### Evidence
```json
{"evidence_id":"00000000-0000-4000-8000-000000000001","source_record_id":"order_evt_893","source_type":"event","tenant_id":"tenant_demo","object_uri":null,"text_excerpt":"Order 893 was delivered at 12:04 UTC","entity_ids":["order:893"],"observed_at":"2026-10-21T12:04:01Z","effective_at":"2026-10-21T12:04:00Z","ingested_at":"2026-10-21T12:04:03Z","expires_at":null,"visibility":"internal","acl_policy_id":"orders-v3","source_system":"delivery-api","source_authority":"authoritative","origin_id":"delivery_api:event:893:status:4","parent_evidence_ids":[],"content_sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","embedding_model_version":null,"index_watermark":null,"retrieval_score":1.0,"rank":1,"source_location":{"table":"order_events","pk":"893-4"}}
```
### Plan
```json
{"plan_id":"00000000-0000-4000-8000-000000000002","query_id":"00000000-0000-4000-8000-000000000003","round_number":1,"strategy":"sql","backend":"postgres","reason_code":"exact_order_id","required_slots":["status","effective_at"],"allowed_tenant_id":"tenant_demo","policy_version":"orders-v3","as_of":"2026-10-21T12:05:00Z","max_age_seconds":3600,"top_k":10,"timeout_ms":300,"estimated_cost_units":1.0,"depends_on_evidence_ids":[]}
```
### VerifierResult
```json
{"query_id":"00000000-0000-4000-8000-000000000003","sufficient":true,"conflicts":[],"missing_slots":[],"accepted_evidence_ids":["00000000-0000-4000-8000-000000000001"],"rejected_evidence_ids":[],"independent_origin_ids":["delivery_api:event:893:status:4"],"policy_passed":true,"freshness_passed":true,"decision":"answer","reason_code":"authoritative_fresh_status"}
```
### QueryTrace
```json
{"trace_id":"00000000-0000-4000-8000-000000000004","query_id":"00000000-0000-4000-8000-000000000003","principal_subject_hash":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","tenant_id":"tenant_demo","query_sha256":"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc","started_at":"2026-10-21T12:05:00Z","finished_at":"2026-10-21T12:05:01Z","policy_version":"orders-v3","plan_ids":["00000000-0000-4000-8000-000000000002"],"returned_evidence_ids":["00000000-0000-4000-8000-000000000001"],"final_decision":"answered","store_calls":1,"elapsed_ms":12.4,"cpu_ms":3.1,"measured_usd":null,"error_codes":[]}
```

## Independent origin vs derived copy
An **independent origin** is a separately observed event or measurement produced by a separately controlled capture process, with independent upstream acquisition and auditable origin/lineage; two indexes, documents or models referring back to one initial claim are **not independent**, regardless of store count. Independence is claim-level and *not* inferred from differing database names, URIs or hashes. Unknown lineage is conservatively treated as correlated, not independent.

1. SQL order row → same row embedded in Qdrant → entity edge in Neo4j: **one origin**, three materializations; no independent corroboration.
2. Driver's scanner timestamp and separately operated depot camera capture: **potentially independent** for arrival time, provided device/event lineage distinct and clocks calibrated; physical event may still share common failure.
3. Two websites that republish the same press release with edited wording: **derived copies**, even with different URLs/hashes.
4. Support agent notes "customer says parcel arrived" and customer's original email: **derived** if note paraphrases email; **independent** only for the distinct fact "agent recorded statement", not parcel delivery truth.
5. Two separately trained models agree after reading the same PDF: **one document-origin evidence stream**; model diversity alone gives no factual independence. Edge case: two individually captured images with identical pixels may be separate captures or copies; require capture metadata and chain of custody, not hash equality alone.
