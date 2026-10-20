"""Inspectable multimodal *retrieval* demonstration, not a database engine.
SQLite is the source of truth, TF-IDF is a vector-space baseline, edges model
relationships. Policy is enforced before ranking; audit contains provenance.
All data here are synthetic, with manually authored test cases.
"""
import argparse, hashlib, json, re, sqlite3, time
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SEED_RECORDS = [
# id, customer, kind, title, body, last_updated, sensitivity, edges
('R01','alice','card','Card delivery delayed','Your replacement debit card may arrive late; check delivery tracking.',100,'private',[]),
('R02','bob','card','Card delivery status','Your card delivery tracking indicates the courier has not arrived.',100,'private',[]),
('R03','alice','refund','Refund pending','Your merchant refund remains pending; settlement may take several days.',100,'private',['R01']),
('R04','alice','transfer','Transfer failed','Your international bank transfer has failed due to bank rejection.',100,'private',[]),
('R05','bob','refund','Refund pending','Your card purchase refund remains pending.',100,'private',[]),
('R06','public','policy','Card delivery policy','A new card can normally be tracked from the cards menu.',100,'public',[]),
('R07','public','policy','Transfer policy','International transfers may require extra compliance checks.',100,'public',[]),
('R08','alice','dispute','Card payment dispute','A merchant dispute is associated with a pending refund.',100,'private',['R03']),
('R09','alice','policy','Outdated card delivery guide','Old instructions: use the legacy portal for card tracking.',10,'public',[]),
('R10','public','policy','Current card delivery guide','Current instructions: select Cards then Track delivery in the app.',100,'public',[]),
('R11','bob','transfer','International transfer failed','The transfer was rejected due to mismatched recipient details.',100,'private',[]),
('R12','alice','card','Physical card activation','You can activate your replacement card in the app once delivered.',100,'private',[]),
]
TEST = [
('alice','delivery status on my replacement card','R01',0,None),
('bob','where is my card courier','R02',0,None),
('alice','merchant refund waiting','R03',0,None),
('bob','purchase refund pending','R05',0,None),
('alice','international transfer rejected','R04',0,None),
('bob','recipient error international transfer','R11',0,None),
('alice','merchant dispute','R08',0,None),
('public','track my card in the app','R10',50,None),
('public','card delivery help','R10',50,None),
('alice','related dispute for refund R03','R08',0,'R03'),
('alice','associated refund for dispute R08','R03',0,'R08'),
('alice','activation of my card','R12',0,None),
]

def make_db():
 db=sqlite3.connect(':memory:');db.execute('CREATE TABLE documents(id TEXT PRIMARY KEY, tenant TEXT, kind TEXT,title TEXT,body TEXT,updated INTEGER,visibility TEXT)');db.execute('CREATE TABLE edges(src TEXT,dst TEXT)');db.execute('CREATE TABLE audit(query TEXT,tenant TEXT,route TEXT,document_id TEXT,hash TEXT)');
 for id,tenant,kind,title,body,updated,vis,edges in SEED_RECORDS:
  db.execute('INSERT INTO documents VALUES(?,?,?,?,?,?,?)',(id,tenant,kind,title,body,updated,vis))
  for linked in edges: db.execute('INSERT INTO edges VALUES (?,?)',(id,linked))
 db.commit();return db

class Engine:
 def __init__(self):
  self.db=make_db();self.docs={r[0]:dict(zip(['id','tenant','kind','title','body','updated','visibility'],r)) for r in self.db.execute('SELECT * FROM documents')}
  self.ids=list(self.docs); self.model=TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True).fit([self.docs[i]['title']+' '+self.docs[i]['body'] for i in self.ids]);self.vec=self.model.transform([self.docs[i]['title']+' '+self.docs[i]['body'] for i in self.ids]);
 def permitted(self,tenant,min_updated=0):
  return {i for i,d in self.docs.items() if (d['visibility']=='public' or d['tenant']==tenant) and d['updated']>=min_updated}
 def search(self,query,tenant='public',min_updated=0,related_to=None,mode='proposed'):
  begin=time.perf_counter();legal=self.permitted(tenant,min_updated)
  if mode=='proposed' and related_to and related_to not in legal: return dict(answer=None,route='denied',ms=(time.perf_counter()-begin)*1e3,denied=True)
  lexical={};semantic={};tokens=set(re.findall(r'[a-z0-9]+',query.lower()))
  for id in self.ids:
   d=self.docs[id]; words=set(re.findall(r'[a-z0-9]+',(d['title']+' '+d['body']).lower()));lexical[id]=len(tokens&words)/max(1,len(tokens))
  sim=cosine_similarity(self.model.transform([query]),self.vec)[0];semantic=dict(zip(self.ids,map(float,sim)))
  graph=set()
  if related_to:
   for a,b in self.db.execute('SELECT src,dst FROM edges'):
    if a==related_to: graph.add(b)
    if b==related_to: graph.add(a)
  # Baselines deliberately lack policies as an illustrative unsafe comparison;
  # also evaluate the full method's policy and routing ablations separately.
  if mode=='lexical':scores=lexical;eligible=set(self.ids)
  elif mode=='vector':scores=semantic;eligible=set(self.ids)
  elif mode in ('hybrid','policy_hybrid'): scores={id: .5*lexical[id]+.5*semantic[id] for id in self.ids};eligible=legal if mode=='policy_hybrid' else set(self.ids)
  else:
   scores={id: .5*lexical[id]+.5*semantic[id]+(1.0 if related_to and id in graph and mode!='no_graph' else 0) for id in self.ids}
   eligible=legal if mode!='no_policy' else set(self.ids)
   if related_to and mode!='no_graph': eligible=eligible&graph
  # full method never answers empty or ungrounded queries
  top=sorted(eligible,key=lambda i:(-scores[i],i))[0] if eligible else None
  route='graph+hybrid' if related_to and mode=='proposed' else 'hybrid+policy' if mode=='proposed' else mode
  if mode=='proposed':
   proof=hashlib.sha256(f'{query}|{tenant}|{min_updated}|{related_to}|{top}'.encode()).hexdigest()
   self.db.execute('INSERT INTO audit VALUES(?,?,?,?,?)',(query,tenant,route,top,proof));self.db.commit()
  return dict(answer=top,route=route,ms=(time.perf_counter()-begin)*1e3,denied=False,eligible=len(eligible))

def evaluate():
 methods=['lexical','vector','hybrid','policy_hybrid','no_graph','no_policy','proposed'];eng=Engine();rows=[];details=[]
 for method in methods:
  correct=0; leak=0;stale=0;lat=[]
  for tenant,q,expected,min_updated,edge in TEST:
   r=eng.search(q,tenant,min_updated,edge,method);good=r['answer']==expected;correct+=good;lat.append(r['ms'])
   if r['answer'] is not None and r['answer'] not in eng.permitted(tenant,min_updated):leak+=1
   if r['answer'] is not None and eng.docs[r['answer']]['updated']<min_updated:stale+=1
   details.append(dict(method=method,tenant=tenant,query=q,expected=expected,**r,correct=good))
  rows.append(dict(method=method,correct=correct,n=len(TEST),accuracy=round(correct/len(TEST),4),unauthorized_or_outdated_answers=leak,stale_answers=stale,median_ms=round(sorted(lat)[len(lat)//2],4)))
 return {'data':'12 synthetic records; 12 manually authored cases; no model APIs','rows':rows,'cases':details,'caveats':['Illustrative test authored for system paths; no independent held-out evaluation.','Baselines intentionally lack policy enforcement; comparisons do not establish superior retrieval algorithms.','TF-IDF is sparse lexical vector representation, not neural semantic embeddings.','Single machine in-memory latency is not deployable-system latency.']}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--out',default='results/multistore.json');args=parser.parse_args();res=evaluate();Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(res,indent=2));print(json.dumps(res['rows'],indent=2))
