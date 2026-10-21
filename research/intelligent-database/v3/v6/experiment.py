"""PACE V6: prediction agreement as a cross-model verification signal.
Do not confuse model consensus with factual evidence or independent ground truth.
"""
import argparse, json, sys, time
from pathlib import Path
import numpy as np
from sklearn.metrics import accuracy_score
import importlib.util
_v5path=Path(__file__).resolve().parent/'reference_v5'/'experiment.py'
_spec=importlib.util.spec_from_file_location('pace_v5_experiment',_v5path)
_v5=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_v5)
prepare,make_models,run_fast,run_full,calibrate,SEED=(_v5.prepare,_v5.make_models,_v5.run_fast,_v5.run_full,_v5.calibrate,_v5.SEED)

def decide(f,u,s,threshold=.75,mode='loop'):
    """Precommit to escalation rules before testing, no access to target label."""
    f,u,s=[np.asarray(z) for z in (f,u,s)]
    fa,ua,sa=[int(np.argmax(z)) for z in (f,u,s)]
    # independent full-feature route used as cross-check; same training corpus, so not independent evidence
    agree=fa==ua
    if mode=='v5':
        if f.max()>=threshold: return fa,'fast',1,False
        if u.max()>=.57:return ua,'full',4,False
        return sa,'strong',12,False
    if agree and min(f.max(),u.max())>=threshold: return fa,'agree',4,False
    # fallback explicitly evaluates third model; disagreement => abstain rather than assert unsupported certainty
    if sa==ua or sa==fa: return sa,'verify',12,False
    return None,'abstain',12,True

def evaluate(name,seed=SEED,threshold=.75):
    x,y,meta,it,iv,ie=prepare(name,seed)
    pca,fast,full,strong=make_models(x,y,it,name)
    # Threshold selected ON VALIDATION only under minimum selective risk and minimum coverage criterion
    fv=run_fast(x[iv],pca,fast);uv=run_full(x[iv],full);sv=run_full(x[iv],strong)
    options=[]
    for th in [.55,.65,.75,.85,.95]:
        rr=[decide(a,b,c,th) for a,b,c in zip(fv,uv,sv)]
        accepted=[(pred,int(y[ix])) for ix,(pred,_,_,ab) in enumerate(rr) if not ab]
        selective=sum(p==actual for p,actual in accepted)/len(accepted) if accepted else 0
        coverage=len(accepted)/len(rr)
        options.append({'threshold':th,'selective_accuracy':selective,'coverage':coverage,'cost':float(np.mean([z[2] for z in rr]))})
    # predeclared target: near-best selective accuracy and at least 90% coverage; cheaper candidate wins
    candidates=[z for z in options if z['coverage']>=.9]
    if not candidates: candidates=options
    maxacc=max(z['selective_accuracy'] for z in candidates)
    picked=min((z for z in candidates if z['selective_accuracy']>=maxacc-.005),key=lambda z:(z['cost'],-z['coverage']))
    threshold=picked['threshold']
    f=run_fast(x[ie],pca,fast);u=run_full(x[ie],full);s=run_full(x[ie],strong)
    v5settings=calibrate(x,y,iv,pca,fast,full,strong)
    truth=y[ie];trace=[];v5=[]; v6=[]
    for j in range(len(ie)):
        pred,route,cost,abstain=decide(f[j],u[j],s[j],threshold)
        f5,route5,cost5,abstain5=decide(f[j],u[j],s[j],v5settings['t_fast'],'v5')
        # V5 uses independently learned second threshold
        if f[j].max()<v5settings['t_fast']:
            if u[j].max()>=v5settings['t_full']:f5,route5,cost5=int(u[j].argmax()),'full',4
            else:f5,route5,cost5=int(s[j].argmax()),'strong',12
        v5.append((f5,cost5));v6.append((pred,cost,abstain))
        trace.append({'sample_index':int(ie[j]),'true_label':int(truth[j]),'fast':int(f[j].argmax()),'full':int(u[j].argmax()),'strong':int(s[j].argmax()),'v5':f5,'v6':pred,'route':route,'abstained':bool(abstain),'correct':bool(pred is not None and pred==truth[j])})
    acc=lambda p:float(np.mean(np.asarray(p)==truth))
    accepted=[(p,int(truth[j])) for j,(p,_,ab) in enumerate(v6) if not ab]
    return {'dataset':meta,'seed':seed,'train':len(it),'validation':len(iv),'test':len(ie),'selected_threshold':threshold,'validation_candidates':options,
       'metrics':{'fast':{'accuracy':acc(f.argmax(axis=1))},'full':{'accuracy':acc(u.argmax(axis=1))},'strong':{'accuracy':acc(s.argmax(axis=1))},'v5':{'accuracy':acc([z[0] for z in v5]),'proxy_cost':float(np.mean([z[1] for z in v5]))},'v6':{'coverage':len(accepted)/len(ie),'selective_accuracy':sum(a==b for a,b in accepted)/len(accepted) if accepted else None,'end_to_end_accuracy_with_abstentions_wrong':sum(a==b for a,b in accepted)/len(ie),'abstentions':len(ie)-len(accepted),'proxy_cost':float(np.mean([z[1] for z in v6]))}},'traces':trace[:30], 'limitations':['V6 is prediction agreement of models trained on the same corpus, not independent verification of source evidence','Classification experiment only; no real multimodal question answering or database engine','No actual SQL/vector/graph service selection','Proxy compute cost is assigned units, not measured latency','Abstention counts as failure in end-to-end accuracy','Threshold calibrated on validation only; test labels never seen by router']}

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='results/v6.json');a=p.parse_args()
    result={n:evaluate(n) for n in ['digits','iris']};Path(a.out).parent.mkdir(exist_ok=True,parents=True);Path(a.out).write_text(json.dumps(result,indent=2));print(json.dumps({n:v['metrics'] for n,v in result.items()},indent=2))
if __name__=='__main__':main()
