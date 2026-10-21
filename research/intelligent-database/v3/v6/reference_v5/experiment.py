"""PACE V5: closed-loop, held-out image routing. Public built-in data, no external APIs.

This is a research pilot using image classification as a proxy for choosing image-feature stores,
NOT a generic natural-language multimodal database or external PostgreSQL/Qdrant/Neo4j deployment.
"""
import argparse, hashlib, json, time
from pathlib import Path
import numpy as np
from sklearn.datasets import load_digits, load_iris
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

SEED=20261021

def entropy(probs):
    p=np.maximum(probs,1e-12)
    return -np.sum(p*np.log(p),axis=1)

def data_digits():
    x,y=load_digits(return_X_y=True)
    return x,y,{'dataset':'sklearn load_digits','real_images':True,'n':len(x),'image_size':'8x8 grayscale pixels','target':'handwritten digit label'}

def data_iris():
    x,y=load_iris(return_X_y=True)
    return x,y,{'dataset':'sklearn load_iris','real_images':False,'n':len(x),'target':'species','image_size':'no images; independent structured-data domain'}

def prepare(name,seed=SEED):
    x,y,metadata= data_digits() if name=='digits' else data_iris()
    idx=np.arange(len(y))
    it, ie=train_test_split(idx,test_size=.25,random_state=seed,stratify=y)
    itr, iv=train_test_split(it,test_size=.25,random_state=seed+1,stratify=y[it])
    return x,y,metadata,itr,iv,ie

def make_models(x,y,itr,name):
    dims=8 if name=='digits' else 2
    pca=PCA(n_components=dims,random_state=13).fit(x[itr]);
    fast=KNeighborsClassifier(n_neighbors=7,weights='uniform',n_jobs=1).fit(pca.transform(x[itr]),y[itr])
    full=KNeighborsClassifier(n_neighbors=5,weights='uniform',n_jobs=1).fit(x[itr],y[itr])
    strong=SVC(C=10,gamma='scale',kernel='rbf',probability=True,random_state=13).fit(x[itr],y[itr])
    return pca,fast,full,strong

def run_fast(x,pca,model): return model.predict_proba(pca.transform(x))
def run_full(x,model): return model.predict_proba(x)

def one_prediction(probs): return np.argmax(probs,axis=1)

def calibrate(x,y,iv,pca,fast,full,strong):
    # Validation labels used for threshold selection only; NEVER inspected at inference.
    f=run_fast(x[iv],pca,fast); u=run_full(x[iv],full); s=run_full(x[iv],strong)
    sacc=(one_prediction(s)==y[iv]).mean(); candidates=[]
    for a in [0.57,0.72,0.86,0.99,1.01]:
      for b in [0.57,0.72,0.86,0.99,1.01]:
        pf=np.max(f,axis=1);pu=np.max(u,axis=1)
        chosen=np.where((pf>=a)[:,None],f,np.where((pu>=b)[:,None],u,s))
        pred=one_prediction(chosen); accuracy=np.mean(pred==y[iv]);
        # proxy costs: fast=1, full=3, strong=8 (NOT real cloud price)
        cost=np.mean(np.where(pf>=a,1,np.where(pu>=b,4,12)))
        candidates.append((accuracy,cost,a,b))
    eligible=[c for c in candidates if c[0]>=sacc-.01]
    best=min(eligible or candidates,key=lambda c:(c[1],-c[0]))
    return {'t_fast':best[2],'t_full':best[3],'validation_accuracy':best[0], 'validation_strong_accuracy':float(sacc),'validation_proxy_cost':best[1], 'selection_objective':'minimum proxy cost while accuracy within 1pp of strong baseline on validation'}

def evaluate(name='digits',seed=SEED):
    x,y,meta,itr,iv,ie=prepare(name,seed)
    pca,fast,full,strong=make_models(x,y,itr,name)
    setting=calibrate(x,y,iv,pca,fast,full,strong)
    f=run_fast(x[ie],pca,fast);u=run_full(x[ie],full);s=run_full(x[ie],strong)
    t1,t2=setting['t_fast'],setting['t_full']
    # Loop: cheap index -> verify posterior confidence -> escalate feature index -> verify -> model fallback.
    result=[]; counts={'fast':0,'full':0,'strong':0}
    predictions={m:[] for m in ['fast_only','full_only','strong_only','loop','single_route']}
    route_log=[]
    # one-shot classifier uses cheap confidence only, no retry
    for j,index in enumerate(ie):
       for m,probs in [('fast_only',f[j]),('full_only',u[j]),('strong_only',s[j])]:predictions[m].append(int(probs.argmax()))
       # one-shot: choose fast unless confidence very low; else full, no outcome verification
       one='fast' if f[j].max()>=t1 else 'full'
       predictions['single_route'].append(int((f[j] if one=='fast' else u[j]).argmax()))
       attempts=[{'store':'pca_knn','confidence':float(f[j].max()),'accepted':bool(f[j].max()>=t1)}]
       if f[j].max()>=t1:route='fast';probs=f[j];cost=1
       else:
         attempts.append({'store':'pixel_knn','confidence':float(u[j].max()),'accepted':bool(u[j].max()>=t2)})
         if u[j].max()>=t2:route='full';probs=u[j];cost=4
         else:
           attempts.append({'store':'rbf_svc','confidence':float(s[j].max()),'accepted':True})
           route='strong';probs=s[j];cost=12
       counts[route]+=1
       guess=int(probs.argmax());predictions['loop'].append(guess)
       route_log.append({'sample_index':int(index),'image_sha256':hashlib.sha256(x[index].astype('float64').tobytes()).hexdigest(),'selected_route':route,'attempts':attempts,'predicted':guess,'correct':bool(guess==y[index])})
    cost={'fast_only':1,'full_only':3,'strong_only':8,'single_route':None,'loop':None}
    loop_cost=np.mean([{'fast':1,'full':4,'strong':12}[r['selected_route']] for r in route_log])
    oneshot_cost=np.mean([1 if f[j].max()>=t1 else 3 for j in range(len(ie))]);cost['loop']=loop_cost;cost['single_route']=oneshot_cost
    metrics={m:{'accuracy':float(accuracy_score(y[ie],p)), 'correct':int(np.sum(y[ie]==p)), 'n':len(ie),'cost_proxy':float(cost[m])} for m,p in predictions.items()}
    # paired outcome differences, not inferential significance
    paired={m:{'loop_wins':int(sum(a==z and b!=z for a,b,z in zip(predictions['loop'],predictions[m],y[ie]))),'loop_losses':int(sum(a!=z and b==z for a,b,z in zip(predictions['loop'],predictions[m],y[ie])))} for m in ['fast_only','full_only','strong_only','single_route']}
    return {'metadata':meta,'seed':seed,'split':{'train':len(itr),'validation':len(iv),'test':len(ie),'stratified':True},'calibration':setting,'metrics':metrics,'paired':paired,'route_counts':counts,'traces':route_log[:15],'limitations':['Image classification is a PROXY for image-store routing, not SQL/vector/graph query selection','RBF SVC is a classifier, not an independent image database','Verifier uses classifier posterior confidence, not factual grounding or image-content authentication','All three models train on the same data; routes correspond to feature/index computation','Proxy cost units are hand-assigned, not measured latency or cloud cost','Dataset digits images are 8x8 grayscale and iris has no images','Confidence threshold calibrated on validation, no true prediction correctness visible to loop','Dataset was available locally; public multimodal VQA datasets not run','Single source catalog, no authorization policy in this stage']}

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='results/results.json');p.add_argument('--seed',type=int,default=SEED);a=p.parse_args()
    r={d:evaluate(d,a.seed) for d in ['digits','iris']};path=Path(a.out);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(r,indent=2));print(json.dumps({d:{'n':a['split']['test'],'metrics':a['metrics'],'route_counts':a['route_counts'],'calibration':a['calibration']} for d,a in r.items()},indent=2))
if __name__=='__main__':main()
