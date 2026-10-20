CREATE TABLE IF NOT EXISTS evidence (
 id TEXT PRIMARY KEY, text TEXT NOT NULL, tenant TEXT NOT NULL,
 classification INTEGER NOT NULL DEFAULT 0, observed_at BIGINT NOT NULL,
 source TEXT NOT NULL, parent TEXT, provenance TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS evidence_policy_idx ON evidence (tenant,classification,observed_at);
