"""HotpotQA dev-distractor *retrieval* benchmark; no gold facts in planner.

Reads original local JSON from official dataset, downloads explicitly only with --download.
Measures evidence passage-level recall, not answer correctness or multi-hop reasoning.
"""
from .core import Evidence, Principal, Request, Planner
import argparse, json, pathlib, time, urllib.request, statistics
URL='https://raw.githubusercontent.com/hotpotqa/hotpot/master/README.md'
# Official data download URL referenced in the original HotpotQA README.
DATA_URL='http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json'
def load(path, limit):
    with open(path,encoding='utf-8') as f: examples=json.load(f)
    return examples[:limit]
def run(examples,k=5):
    now=int(time.time()); hits={'lexical':0,'pace':0}; total=0; durations={'lexical':[],'pace':[]}
    for ex in examples:
        docs=[Evidence(f'{ex["_id"]}:{i}', ' '.join(sentences), 'public',0,now,title,provenance=f'hotpot:{ex["_id"]}:{title}') for i,(title,sentences) in enumerate(ex['context'])]
        # Relationships are deliberately NOT constructed from gold supporting facts.
        # Safe self-chosen links can later be added from independently predicted entities.
        planner=Planner(docs,[])
        query=Request(ex['question'],Principal('public',0),now,k=k)
        titles={t for t,_ in ex['supporting_facts']}
        if not titles:continue
        total+=1
        for method in hits:
            t=time.perf_counter(); out=planner.run(query,mode='pace' if method=='pace' else 'lexical'); durations[method].append((time.perf_counter()-t)*1000)
            found={d['source'] for d in out['evidence']}
            hits[method]+=titles.issubset(found)
    return {'dataset':'HotpotQA distractor dev','n':total,'passage_support_recall_at_k':{m:hits[m]/total if total else None for m in hits},'median_ms':{m:statistics.median(t) if t else None for m,t in durations.items()},'warning':'Document support recall ONLY; not QA accuracy; no external stores; baseline and PACE identical without independent graph.'}
def main():
    p=argparse.ArgumentParser(); p.add_argument('--path',default='datasets/hotpot_dev_distractor_v1.json');p.add_argument('--limit',type=int,default=100);p.add_argument('--k',type=int,default=5);p.add_argument('--out',default='results/hotpot_eval.json');p.add_argument('--download',action='store_true');args=p.parse_args()
    path=pathlib.Path(args.path)
    if args.download:
        path.parent.mkdir(parents=True,exist_ok=True)
        urllib.request.urlretrieve(DATA_URL,path)
    if not path.exists():raise SystemExit('Dataset not found. Download from official HotpotQA page; specify --path, or run --download in a networked environment.')
    results=run(load(path,args.limit),args.k);out=pathlib.Path(args.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
if __name__=='__main__':main()
