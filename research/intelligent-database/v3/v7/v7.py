"""PACE-DB V7: independent record, text, and relation evidence; strict policy & provenance.
All data synthetic; verification is deterministic and limited to authored cases.
"""
import json, sqlite3, hashlib, re, random, time, argparse
from dataclasses import dataclass
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

@dataclass(frozen=True)
class Query:
    tenant: str
    order: str
    question: str
    as_of: int=1000
    clearance: int=0
    max_age: int=100

# Structured, document, and edges maintained as distinct stores, all permission checked.
class Stores:
    def __init__(self):
        self.db=sqlite3.connect(':memory:')
        self.db.execute('CREATE TABLE orders (id TEXT, tenant TEXT, customer TEXT, state TEXT, driver TEXT, updated INTEGER, clearance INTEGER)')
        self.db.execute('CREATE TABLE docs (id TEXT, tenant TEXT, oid TEXT, text TEXT, updated INTEGER, clearance INTEGER)')
        self.db.execute('CREATE TABLE edges (tenant TEXT, src TEXT, dst TEXT, rel TEXT, updated INTEGER, clearance INTEGER)')
        self.docrows=[];self.vectors=None;self.model=TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True)
    def add(self, oid,tenant,state,driver,ts, note_state=None, note_time=None, edge_driver=None, clearance=0):
        self.db.execute('INSERT INTO orders VALUES (?,?,?,?,?,?,?)',(oid,tenant,'customer_'+oid,state,driver,ts,clearance))
        note_state=note_state or state;note_time=note_time if note_time is not None else ts
        self.db.execute('INSERT INTO docs VALUES (?,?,?,?,?,?)',(f'doc_{oid}',tenant,oid,f'Order {oid} delivery status {note_state}; carrier notice for {oid}',note_time,clearance))
        self.db.execute('INSERT INTO edges VALUES (?,?,?,?,?,?)',(tenant,oid,edge_driver or driver,'assigned_to',ts,clearance))
    def finish(self):
        self.db.commit()
        self.docrows=self.db.execute('SELECT * FROM docs ORDER BY id').fetchall()
        self.vectors=self.model.fit_transform([r[3] for r in self.docrows])
    @staticmethod
    def permit(tenant,updated,clearance,q):return tenant==q.tenant and clearance<=q.clearance and 0<=q.as_of-updated<=q.max_age
    def sql(self,q):
        rows=self.db.execute('SELECT * FROM orders WHERE id=? AND tenant=?',(q.order,q.tenant)).fetchall()
        return [{'source':'sql','state':r[3],'driver':r[4],'updated':r[5],'id':r[0]} for r in rows if self.permit(r[1],r[5],r[6],q)]
    def vector(self,q):
        sims=cosine_similarity(self.model.transform([q.question+' '+q.order]),self.vectors)[0]
        matches=[]
        for idx in np.argsort(-sims)[:8]:
            r=self.docrows[int(idx)]
            if r[2]==q.order and self.permit(r[1],r[4],r[5],q):
                mm=re.search(r'delivery status (.*?);',r[3]);matches.append({'source':'vector','state':mm.group(1),'updated':r[4],'id':r[0],'similarity':float(sims[idx])})
        return matches[:1]
    def graph(self,q):
        rows=self.db.execute('SELECT * FROM edges WHERE src=? AND tenant=?',(q.order,q.tenant)).fetchall()
        return [{'source':'graph','driver':r[2],'updated':r[4],'id':r[1]+'->'+r[2]} for r in rows if self.permit(r[0],r[4],r[5],q)]

def fingerprint(item):return hashlib.sha256(json.dumps(item,sort_keys=True).encode()).hexdigest()

def answer(st,q,mode='verified'):
    trace=[]
    def fetch(channel):
        records=getattr(st,channel)(q);trace.append({'step':channel,'count':len(records),'ids':[r['id'] for r in records]});return records
    sql=fetch('sql')
    if not sql:return {'answer':None,'status':'abstain','trace':trace,'reason':'no_authorized_current_record','units':1}
    ref=sql[0]; asks_driver='driver' in q.question.lower() or 'assigned' in q.question.lower()
    if mode=='sql_only':
        return {'answer':ref['driver'] if asks_driver else ref['state'],'status':'answered','trace':trace,'units':1}
    docs=fetch('vector')
    if mode=='one_shot':
        return {'answer':docs[0]['state'] if docs else None,'status':'answered' if docs else 'abstain','trace':trace,'units':3}
    edges=fetch('graph') if asks_driver else []
    units=1+2+(2 if asks_driver else 0)
    if not docs:return {'answer':None,'status':'abstain','reason':'missing_independent_document','trace':trace,'units':units}
    if docs[0]['state']!=ref['state']:
        return {'answer':None,'status':'abstain','reason':'sql_document_disagreement','trace':trace,'units':units,'evidence_hashes':[fingerprint(x) for x in (ref,docs[0])]}
    if asks_driver:
        if not edges or edges[0]['driver']!=ref['driver']:
            return {'answer':None,'status':'abstain','reason':'sql_graph_disagreement','trace':trace,'units':units}
    return {'answer':ref['driver'] if asks_driver else ref['state'],'status':'answered','trace':trace,'units':units,'evidence_hashes':[fingerprint(x) for x in [ref,docs[0]]+edges]}

def experiment(n=240,seed=41):
    rng=random.Random(seed);st=Stores();truth={};questions=[]
    states=['dispatched','processing','delayed','delivered'];drivers=['Amir','Nadia','Imran','Sara']
    for i in range(n):
        oid=f'O{i:05d}';tenant=['A','B'][i%2];state=states[i%4];driver=drivers[i%4]
        corrupt=rng.random()<0.16;stale=rng.random()<0.12;graph_corrupt=rng.random()<0.11
        # Corrupt independent text/graph sources without changing SQL truth.
        st.add(oid,tenant,state,driver,1000,note_state=states[(i+1)%4] if corrupt else state,note_time=790 if stale else 1000,edge_driver=drivers[(i+1)%4] if graph_corrupt else driver)
        truth[oid]=(tenant,state,driver)
        if i%6==0:
            questions.append(Query('B' if tenant=='A' else 'A',oid,f'What is the status for {oid}?'))
        elif i%4==0:
            questions.append(Query(tenant,oid,f'Who is assigned driver for order {oid}?'))
        else:
            questions.append(Query(tenant,oid,f'Please tell me latest order delivery status {oid}'))
    st.finish();out={'setup':{'records':n,'queries':len(questions),'seed':seed,'data':'synthetic','real_external_databases':False},'methods':{},'failures':{}}
    for method in ['sql_only','one_shot','verified']:
        correct=answered=abstained=violations=cost=0;causes={}
        for q in questions:
            result=answer(st,q,method);cost+=result['units'];is_auth=truth[q.order][0]==q.tenant
            if result['status']=='answered':
                answered+=1
                expected=truth[q.order][2] if 'driver' in q.question.lower() else truth[q.order][1]
                correct+=result['answer']==expected
                violations+=not is_auth
            else:
                abstained+=1;why=result.get('reason','unknown');causes[why]=causes.get(why,0)+1
        out['methods'][method]={'correct':correct,'answered':answered,'abstained':abstained,'unauthorized_answers':violations,'selective_accuracy':round(correct/answered,4) if answered else None,'end_to_end_success':round(correct/len(questions),4),'coverage':round(answered/len(questions),4),'mean_modeled_cost':round(cost/len(questions),3),'abstention_causes':causes}
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default='results/v7.json');p.add_argument('--n',type=int,default=240);args=p.parse_args()
    result=experiment(args.n);path=Path(args.out);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
