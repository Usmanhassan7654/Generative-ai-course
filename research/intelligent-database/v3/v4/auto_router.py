"""V4 experiment: learned strategy selection with shared policy guards.

This uses TF-IDF and graph neighbors, *not* production databases or dense embeddings.
Training learns the lowest-cost successful route on validation questions.
"""
from dataclasses import dataclass
import hashlib
import json
import time
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

ROUTES=("exact", "semantic", "graph")
COST={"exact":1.0,"semantic":2.0,"graph":3.5}

@dataclass(frozen=True)
class Doc:
    id:str
    text:str
    tenant:str="A"
    clearance:int=0
    updated:int=1000
    refs:tuple=()
    key:str=""

class Store:
    def __init__(self,docs):
        self.docs={d.id:d for d in docs}
        self.ids=list(self.docs)
        self.tfidf=TfidfVectorizer(analyzer="char_wb",ngram_range=(2,5),lowercase=True)
        self.X=self.tfidf.fit_transform([self.docs[i].text for i in self.ids])
    def allowed(self,tenant,clearance,as_of=1000,max_age=100):
        return {d.id for d in self.docs.values() if d.tenant==tenant and d.clearance<=clearance and 0<=as_of-d.updated<=max_age}
    def retrieve(self,q,route,tenant="A",clearance=0,k=3):
        allowed=self.allowed(tenant,clearance)
        if route=="exact":
            # exact keyed lookup, a relational primary-key analogue
            tokens=set(q.lower().replace('?',' ').replace(',',' ').split())
            ids=[id for id in self.ids if id in allowed and self.docs[id].key and self.docs[id].key.lower() in tokens]
            ids=ids[:k]
        else:
            sims=cosine_similarity(self.tfidf.transform([q]),self.X)[0]
            order=np.argsort(-sims,kind="stable")
            seeds=[self.ids[i] for i in order if self.ids[i] in allowed and sims[i]>0][:k]
            ids=list(seeds)
            if route=="graph":
                for id in seeds:
                    for ref in self.docs[id].refs:
                        if ref in allowed and ref not in ids:ids.append(ref)
        # Non-bypassable second guard
        ids=[id for id in ids if id in allowed]
        return ids[:k+3]

class AdaptiveRouter:
    def __init__(self):
        self.vectorizer=TfidfVectorizer(analyzer="char_wb",ngram_range=(2,4),min_df=1)
        self.model=LogisticRegression(max_iter=700,random_state=19)
        self.trained=False
    def fit(self,training,store):
        # Choose first successful method from ascending cost, otherwise the lowest-cost method.
        labels=[]
        for q,gold in training:
            success=[r for r in ROUTES if set(gold).issubset(set(store.retrieve(q,r)))]
            labels.append(min(success,key=lambda r:COST[r]) if success else "exact")
        self.model.fit(self.vectorizer.fit_transform([q for q,_ in training]),labels)
        self.trained=True
        return dict((x,labels.count(x)) for x in sorted(set(labels)))
    def predict(self,q):
        return self.model.predict(self.vectorizer.transform([q]))[0]
    def run(self,store,q,tenant="A",clearance=0,k=3):
        t=time.perf_counter_ns();route=self.predict(q);ids=store.retrieve(q,route,tenant,clearance,k)
        return {"route":route,"ids":ids,"cost_units":COST[route],"latency_ms":(time.perf_counter_ns()-t)/1e6,"query_hash":hashlib.sha256(q.encode()).hexdigest()}
