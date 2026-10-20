"""Real external-store adapter paths. Must be tested with Docker services.

The policy gate remains in Python, not delegated to any vector database filter.
"""
from __future__ import annotations
from .core import Evidence

def postgresql_rows(dsn: str) -> list[Evidence]:
    import psycopg
    with psycopg.connect(dsn) as conn, conn.cursor() as cur:
        cur.execute('SELECT id,text,tenant,classification,observed_at,source,parent,provenance FROM evidence')
        return [Evidence(*r) for r in cur.fetchall()]

def qdrant_upsert(url: str, collection: str, rows: list[Evidence], encoder):
    """Encoder must return dense normalized vectors; pass a model with documented version."""
    from qdrant_client import QdrantClient,models
    client=QdrantClient(url=url)
    vectors=encoder([r.text for r in rows]); dims=len(vectors[0])
    if not client.collection_exists(collection):
        client.create_collection(collection,vectors_config=models.VectorParams(size=dims,distance=models.Distance.COSINE))
    client.upsert(collection,points=[models.PointStruct(id=i+1,vector=v, payload={"evidence_id":r.id,"tenant":r.tenant}) for i,(r,v) in enumerate(zip(rows,vectors))])
    return client

def neo4j_upsert(uri: str, user: str, password: str, edges: list[tuple[str,str]]):
    from neo4j import GraphDatabase
    with GraphDatabase.driver(uri,auth=(user,password)) as driver:
        with driver.session() as s:
            for a,b in edges:
                s.run('MERGE (a:Evidence {id:$a}) MERGE (b:Evidence {id:$b}) MERGE (a)-[:RELATED_TO]->(b)',a=a,b=b).consume()
