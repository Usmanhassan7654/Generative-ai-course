"""PACE-DB V3 experimental core: policy-constrained evidence planning.

No LLM is trusted to enforce access policies. All evidence is revalidated before output.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib, json, math, re, time
from collections import Counter
from typing import Iterable

@dataclass(frozen=True)
class Evidence:
    id: str
    text: str
    tenant: str
    classification: int
    observed_at: int
    source: str
    parent: str | None = None
    provenance: str = ""

@dataclass(frozen=True)
class Principal:
    tenant: str
    clearance: int

@dataclass(frozen=True)
class Request:
    query: str
    principal: Principal
    as_of: int
    max_age_seconds: int = 86400 * 365
    k: int = 5
    requires_multihop: bool = False

class Guard:
    @staticmethod
    def permitted(e: Evidence, q: Request):
        return (e.tenant == q.principal.tenant
                and e.classification <= q.principal.clearance
                and 0 <= q.as_of - e.observed_at <= q.max_age_seconds)

class SparseIndex:
    """Auditable sparse TF-IDF retrieval fallback, not dense embeddings."""
    @staticmethod
    def tokens(s): return re.findall(r"\b[a-z0-9]+\b", s.lower())
    def __init__(self, rows: list[Evidence]):
        self.rows = rows
        self.counts = [Counter(self.tokens(r.text)) for r in rows]
        self.df = Counter()
        for c in self.counts: self.df.update(c.keys())
        self.n = len(rows)
    def search(self, query: str, allowed_ids: set[str], k=10):
        qc = Counter(self.tokens(query)); out=[]
        for row,c in zip(self.rows,self.counts):
            if row.id not in allowed_ids: continue
            score=0.0
            for word, n in qc.items():
                if word in c:
                    score += (1+math.log(c[word]))*(1+math.log((self.n+1)/(self.df[word]+1)))
            if score: out.append((row.id,score))
        return sorted(out,key=lambda x:(-x[1],x[0]))[:k]

class GraphIndex:
    def __init__(self, edges: list[tuple[str,str]]):
        self.adj={}
        for a,b in edges:
            self.adj.setdefault(a,set()).add(b)
            self.adj.setdefault(b,set()).add(a)
    def expand(self, ids: Iterable[str], allowed: set[str], hops=1):
        seen=set(ids)&allowed; frontier=set(seen)
        for _ in range(hops):
            frontier={n for x in frontier for n in self.adj.get(x,set()) if n in allowed}-seen
            seen|=frontier
        return seen

class Planner:
    def __init__(self, rows: list[Evidence], edges: list[tuple[str,str]]):
        self.rows={r.id:r for r in rows}; self.index=SparseIndex(rows); self.graph=GraphIndex(edges)
    def run(self, req: Request, mode="pace"):
        started=time.perf_counter_ns()
        allowed={id for id,e in self.rows.items() if Guard.permitted(e,req)}
        candidates=self.index.search(req.query,allowed, max(10,req.k))
        seed=[id for id,_ in candidates[:req.k]]
        if mode=="pace" and req.requires_multihop:
            expanded=self.graph.expand(seed,allowed,1)
            ids=seed+sorted(expanded-set(seed))
        elif mode=="lexical_all":
            # Diagnostic ONLY: deliberately unsafe baseline; never use for serving users.
            ids=[id for id,_ in self.index.search(req.query,set(self.rows),req.k)]
        else:
            ids=seed
        # NON-BYPASSABLE final guard, including graph expansion and unsafe diagnostics.
        included=[self.rows[id] for id in ids if Guard.permitted(self.rows[id],req)][:req.k*3]
        evidence=[dict(asdict(e),sha256=hashlib.sha256(e.text.encode()).hexdigest()) for e in included]
        audit={"query_sha256":hashlib.sha256(req.query.encode()).hexdigest(),"tenant":req.principal.tenant,
               "candidate_count":len(candidates),"allowed_count":len(allowed),"returned_ids":[e.id for e in included],
               "abstained":not bool(evidence),"policy_checked":True,"mode":mode,
               "elapsed_ms":round((time.perf_counter_ns()-started)/1e6,4)}
        return {"evidence":evidence,"audit":audit,"answer":None if not evidence else "Evidence retrieved; generation not implemented"}
