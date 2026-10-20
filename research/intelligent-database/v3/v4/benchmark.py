"""Deterministic, synthetic V4 scenario benchmark. No publication-grade accuracy claim."""
import argparse,json,random,statistics,time
from pathlib import Path
from .auto_router import Doc,Store,AdaptiveRouter,ROUTES,COST

RNG=random.Random(19)
ITEMS=[("AX100","parcel","dispatch","driver"),( "BX200","card","delivery","courier"),("CX300","invoice","payment","finance"),("DX400","machine","maintenance","technician"),("EX500","product","return","support"),("FX600","license","renewal","compliance"),("GX700","vehicle","inspection","inspector"),("HX800","shipment","customs","agent"),("IX900","claim","approval","reviewer"),("JX110","report","audit","auditor")]
EXACT_TEMPLATES=["show status of {key}","lookup {key}","fetch record {key}","what happened to {key}","please retrieve {key}","get the entry {key}"]
SEM_TEMPLATES=["how do I resolve a {subject} {issue} problem", "guide for {subject} {issue}","what is the process for {subject} {issue}","help with {subject} {issue}","how is {subject} {issue} handled","explain {subject} {issue} procedure"]
GRAPH_TEMPLATES=["which {role} handled the {subject} {issue}","who was responsible for {subject} {issue}","trace the {subject} {issue} to the assigned {role}","which person owns {subject} {issue}","find the linked {role} for {subject} {issue}","what {role} is connected to {subject} {issue}"]

def corpus():
    docs=[];cases=[]
    for key,subject,issue,role in ITEMS:
        root=f"r-{key}";linked=f"l-{key}";policy=f"p-{key}"
        docs.extend([Doc(root,f"{subject} {issue} workflow. {subject} {issue} help and responsibility record",key=key,refs=(linked,)),
                     Doc(linked,f"assignment ledger entry {key} person F18",refs=(root,)),
                     Doc(policy,f"{subject} {issue} procedure instructions and troubleshooting")])
        for template in EXACT_TEMPLATES:cases.append((template.format(key=key),[root],"exact",template))
        for template in SEM_TEMPLATES:cases.append((template.format(subject=subject,issue=issue),[root],"semantic",template))
        for template in GRAPH_TEMPLATES:cases.append((template.format(subject=subject,issue=issue,role=role),[root,linked],"graph",template))
    docs.extend([Doc("private", "secret card delivery record", tenant="B",clearance=4),Doc("stale","historic card delivery record",updated=10)])
    # Split by query template, rather than random question, to avoid identical phrasing in train/test.
    training=[(q,g) for q,g,kind,t in cases if t in (EXACT_TEMPLATES[:4]+SEM_TEMPLATES[:4]+GRAPH_TEMPLATES[:4])]
    testing=[(q,g,kind) for q,g,kind,t in cases if t in (EXACT_TEMPLATES[4:]+SEM_TEMPLATES[4:]+GRAPH_TEMPLATES[4:])]
    RNG.shuffle(training);RNG.shuffle(testing)
    return docs,training,testing

def evaluate():
    docs,train,test=corpus();store=Store(docs);router=AdaptiveRouter();distribution=router.fit(train,store)
    methods=list(ROUTES)+["adaptive"]
    records={m:[] for m in methods};failures={m:[] for m in methods}
    for q,gold,kind in test:
        for method in methods:
            t=time.perf_counter_ns()
            if method=="adaptive":
                output=router.run(store,q); ids=output["ids"];route=output["route"]
            else:
                route=method;ids=store.retrieve(q,method)
            latency=(time.perf_counter_ns()-t)/1e6
            hit=set(gold).issubset(set(ids))
            row={"query":q,"family":kind,"selected":route,"gold":gold,"predicted":ids,"success":hit,"cost_units":COST[route],"latency_ms":latency}
            records[method].append(row)
            if not hit:failures[method].append(row)
    metrics={}
    for method,rows in records.items():
        metrics[method]={"n":len(rows),"all_required_evidence_recall":sum(r["success"] for r in rows)/len(rows),"mean_cost_units":statistics.mean(r["cost_units"] for r in rows),"median_ms":statistics.median(r["latency_ms"] for r in rows),"p95_ms":sorted(r["latency_ms"] for r in rows)[int(.95*(len(rows)-1))],"route_counts":{r:sum(x["selected"]==r for x in rows) for r in ROUTES},"by_query_family":{f:sum(r["success"] for r in rows if r["family"]==f)/sum(r["family"]==f for r in rows) for f in ROUTES}}
    return {"experiment":"PACE V4 learned routing","data":"Synthetic scenario corpus, 10 entities, 180 generated questions, template-held-out test=60","train_n":len(train),"test_n":len(test),"train_route_labels":distribution,"metrics":metrics,"failures":{m:v[:5] for m,v in failures.items()},"limitations":["Synthetic, template-generated queries; not independent human-labeled evaluation","Scores are retrieval-only, not answer correctness","Vector-style route is sparse character TF-IDF, not dense neural embeddings","Graph is in-process adjacency, exact route is an in-memory key lookup, not deployed database queries","Unit cost values are declared proxies, not monetary infrastructure cost","Single deterministic data split; no uncertainty intervals","Same source corpus for all methods; same tenant and freshness guard"]}

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='results/v4_synthetic.json');a=p.parse_args();result=evaluate();out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2));print(json.dumps({"train_n":result["train_n"],"test_n":result["test_n"],"metrics":result["metrics"]},indent=2))
if __name__=='__main__':main()
