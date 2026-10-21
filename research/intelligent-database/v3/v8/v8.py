"""PACE V8. Synthetic, audited evidence reconciliation with bounded escalation.

This prototype simulates SQL, searchable documents, graph edges, and immutable carrier events
as logical stores in SQLite. It is NOT a live multi-service database system.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sqlite3, statistics, time
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class Request:
    tenant: str
    order: str
    field: str             # status or driver
    now: int=1000
    max_age: int=100
    clearance: int=0

class EvidenceStore:
    def __init__(self):
        self.db=sqlite3.connect(':memory:')
        self.db.execute('CREATE TABLE evidence (eid TEXT PRIMARY KEY, oid TEXT, tenant TEXT, field TEXT, value TEXT, source TEXT, updated INTEGER, clearance INTEGER, event_key TEXT)')
    def put(self,eid,oid,tenant,field,value,source,updated=1000,clearance=0,event_key=''):
        self.db.execute('INSERT INTO evidence VALUES(?,?,?,?,?,?,?,?,?)',(eid,oid,tenant,field,value,source,updated,clearance,event_key))
    def read(self,q:Request,source:str):
        rows=self.db.execute('SELECT eid,oid,tenant,field,value,source,updated,clearance,event_key FROM evidence WHERE oid=? AND tenant=? AND field=? AND source=? ORDER BY updated DESC,eid',(q.order,q.tenant,q.field,source)).fetchall()
        return [dict(zip(['id','order','tenant','field','value','source','updated','clearance','event_key'],r)) for r in rows if r[7]<=q.clearance and 0<=q.now-r[6]<=q.max_age]
    def read_all(self,q,source):
        return self.read(q,source)

def h(record):
    return hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()

# Authority weights are fixed before benchmarking; can be tuned ONLY on validation data in later experiments.
RELIABILITY={'sql':0.90,'document':0.64,'graph':0.76,'event':0.95}
COST={'sql':1,'document':2,'graph':2,'event':3}

def decide(st:EvidenceStore,q:Request,method='v8'):
    trace=[]; used=[];units=0
    def fetch(src):
        nonlocal units
        records=st.read(q,src)
        units+=COST[src]
        trace.append({'store':src,'returned':len(records),'evidence_hashes':[h(x) for x in records]})
        used.extend(records)
        return records
    sql=fetch('sql')
    if not sql:
        return {'status':'abstain','answer':None,'reason':'no_authorized_fresh_sql','units':units,'trace':trace}
    primary=sql[0]
    if method=='sql':
        return {'status':'answered','answer':primary['value'],'reason':'sql_only','units':units,'trace':trace}
    doc=fetch('document')
    if method=='v7':
        if not doc or doc[0]['value']!=primary['value']:
            return {'status':'abstain','answer':None,'reason':'document_conflict_or_missing','units':units,'trace':trace}
        if q.field=='driver':
            graph=fetch('graph')
            if not graph or graph[0]['value']!=primary['value']:
                return {'status':'abstain','answer':None,'reason':'graph_conflict_or_missing','units':units,'trace':trace}
        return {'status':'answered','answer':primary['value'],'reason':'v7_consensus','units':units,'trace':trace}
    if method!='v8':raise ValueError(method)
    # First add domain-specific relationship evidence where relevant.
    graph=fetch('graph') if q.field=='driver' else []
    quorum=[primary]+doc[:1]+graph[:1]
    distinct={r['value'] for r in quorum}
    missing=len(quorum)<(3 if q.field=='driver' else 2)
    # A cheap consistent quorum returns immediately. Do not equate agreement with truth.
    if len(distinct)==1 and not missing:
        return {'status':'answered','answer':primary['value'],'reason':'verified_quorum','units':units,'trace':trace}
    # Reconcile by requesting an independently generated carrier-event record.
    events=fetch('event')
    if not events:
        return {'status':'abstain','answer':None,'reason':'no_fresh_event_to_reconcile','units':units,'trace':trace}
    newest=events[0]
    if len(events)>1 and events[1]['updated']==newest['updated'] and events[1]['value']!=newest['value']:
        return {'status':'abstain','answer':None,'reason':'event_log_inconsistent','units':units,'trace':trace}
    # Require independent corroboration for the event's value, not just its authority rank.
    supporting=[x for x in quorum if x['value']==newest['value']]
    if not supporting:
        return {'status':'abstain','answer':None,'reason':'event_uncorroborated','units':units,'trace':trace}
    # Records labeled as an event from the same external receipt cannot count twice.
    if newest['event_key'] and all(x['event_key']==newest['event_key'] for x in supporting):
        return {'status':'abstain','answer':None,'reason':'not_independent','units':units,'trace':trace}
    return {'status':'answered','answer':newest['value'],'reason':'event_reconciled','units':units,'trace':trace}

VALUES={'status':['processing','dispatched','delayed','delivered'],'driver':['Amir','Nadia','Imran','Sara']}
def wrong(value,field,rng):
    return rng.choice([v for v in VALUES[field] if v!=value])

def dataset(n=600,seed=42):
    rng=random.Random(seed);st=EvidenceStore();cases=[]
    for i in range(n):
        field='status' if i%2==0 else 'driver'
        tenant='A' if i%3 else 'B';order=f'ORD{i:06d}'
        truth=rng.choice(VALUES[field]); asof=1000
        sql_wrong=rng.random()<0.15
        doc_wrong=rng.random()<0.24
        graph_wrong=rng.random()<0.18
        event_wrong=rng.random()<0.06
        st.put(f'sql_{i}',order,tenant,field,wrong(truth,field,rng) if sql_wrong else truth,'sql',1000)
        st.put(f'doc_{i}',order,tenant,field,wrong(truth,field,rng) if doc_wrong else truth,'document',750 if rng.random()<0.07 else 994)
        if field=='driver':st.put(f'edge_{i}',order,tenant,field,wrong(truth,field,rng) if graph_wrong else truth,'graph',995)
        # Event is an independent synthetic record; event errors exist to prevent a perfect oracle.
        if rng.random()>=0.09:
            st.put(f'event_{i}',order,tenant,field,wrong(truth,field,rng) if event_wrong else truth,'event',999,0,f'carrier_{i}')
        # Roughly 1 in 8 are unauthorised (wrong tenant), others fully eligible.
        ask_tenant= ('B' if tenant=='A' else 'A') if i%8==0 else tenant
        cases.append((Request(ask_tenant,order,field,asof),truth,ask_tenant==tenant))
    st.db.commit()
    return st,cases

def evaluate(n=600,seed=42):
    st,cases=dataset(n,seed)
    result={'metadata':{'n':n,'seed':seed,'data':'synthetic','external_database_services':False,'models':'deterministic fixed-rule','evaluation':'single-run simulated multi-source reconciliation'},'methods':{},'examples':[]}
    for method in ('sql','v7','v8'):
        counts={'correct':0,'incorrect':0,'abstained':0,'unauthorized':0,'eligible_correct':0,'eligible_total':0,'cost':0};reasons={}
        for idx,(q,truth,allowed) in enumerate(cases):
            r=decide(st,q,method);counts['cost']+=r['units']
            if allowed:counts['eligible_total']+=1
            if r['status']=='answered':
                if not allowed:counts['unauthorized']+=1
                if r['answer']==truth:
                    counts['correct']+=1
                    if allowed:counts['eligible_correct']+=1
                else:counts['incorrect']+=1
            else:
                counts['abstained']+=1;reasons[r['reason']]=reasons.get(r['reason'],0)+1
            if method=='v8' and len(result['examples'])<5 and r['reason'] in ('event_reconciled','event_uncorroborated','no_fresh_event_to_reconcile'):
                result['examples'].append({'query':asdict(q),'truth':truth,'decision':r})
        ans=counts['correct']+counts['incorrect'];eligible=counts['eligible_total']
        result['methods'][method]={**counts,'coverage':round(ans/n,4),'answered_accuracy':round(counts['correct']/ans,4) if ans else None,'eligible_success':round(counts['eligible_correct']/eligible,4),'cost_per_query_modeled':round(counts['cost']/n,3),'abstention_reasons':reasons}
    return result

def repeated(seeds=range(40,45),n=600):
    runs=[evaluate(n,s) for s in seeds]
    return {'individual_runs':runs,'aggregate':{m:{metric:{'mean':round(statistics.mean(r['methods'][m][metric] for r in runs),4),'min':round(min(r['methods'][m][metric] for r in runs),4),'max':round(max(r['methods'][m][metric] for r in runs),4)} for metric in ('eligible_success','answered_accuracy','coverage','cost_per_query_modeled')} for m in ('sql','v7','v8')}}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='results/v8.json');parser.add_argument('--n',type=int,default=600);args=parser.parse_args()
    output=repeated(n=args.n);path=Path(args.out);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(output,indent=2));print(json.dumps(output['aggregate'],indent=2))
