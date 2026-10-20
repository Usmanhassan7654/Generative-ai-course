"""Reproducible BANKING77 intent-routing benchmark (no proprietary models/APIs).

Research prototype: SQL metadata + lexical and character-semantic evidence,
uncertainty-aware gate with abstention. NOT a new DB engine.
"""
import argparse, csv, hashlib, io, json, random, statistics, time, urllib.request
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

SEED = 42
URL = 'https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/9d081458ff52e53cf7e848f414e6e9344e4e6696/banking_data/'
HASHES = {'train': 'b06e26ac675513959a63135f11b94ea7786ed02da65db93a5650d8838cbc664b',
          'test': 'd12d6e3bc4c3103966ae786dc435913c0c563dfa328f5a3646d0e62cfeeb474d'}
DEMO = [('How do I locate my card?','card_arrival'),('I ordered a card but it has not arrived.','card_arrival'),('When will I get my card?','card_arrival'),('How do I track my card?','card_arrival'),('My card has not arrived yet.','card_arrival'),('I am still waiting on my card.','card_arrival'),('Where is my new card?','card_arrival'),('Why has my new card not been delivered?','card_arrival'),
('Where do I link the new card?','card_linking'),('How do I add a card to my account?','card_linking'),('How do I link a new card?','card_linking'),('I want to connect an existing card to the app.','card_linking'),('Can I reactivate my lost card?','card_linking'),('How do I sync my card to my app?','card_linking'),('I received my card, how do I link it?','card_linking'),('Where can I add the new card in the app?','card_linking'),
('I need to know your exchange rates.','exchange_rate'),('What exchange rates do you offer?','exchange_rate'),('How are exchange rates calculated?','exchange_rate'),('What is the current exchange rate?','exchange_rate'),('Where do you get your exchange rates from?','exchange_rate'),('Can you explain the exchange rate policy?','exchange_rate'),('How often do your exchange rates change?','exchange_rate'),('What is the rate for exchanging currencies?','exchange_rate')]

def read_split(name, cache):
    f = cache / (name+'.csv')
    if not f.exists():
        cache.mkdir(parents=True,exist_ok=True)
        urllib.request.urlretrieve(URL+name+'.csv',f)
    raw=f.read_bytes(); observed=hashlib.sha256(raw).hexdigest()
    if observed != HASHES[name]:
        raise RuntimeError(f'{name}: SHA256 mismatch: {observed}; do not use unverified data')
    return [(r['text'],r['category']) for r in csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))]

def top_class(probs, classes):
    i=np.argmax(probs,axis=1); return np.asarray(classes)[i], np.max(probs,axis=1)

def best_gate(validation_predictions, validation_confidences, yval, classes):
    # Select per-route confidence rules using validation only; test never used here.
    candidates=[0.,.35,.45,.55,.65,.75,.85,.95]
    best=None
    for word_t in candidates:
        for char_t in candidates:
            pw,pc,pl=validation_predictions
            cw,cc,cl=validation_confidences
            pred=np.where(cw>=word_t,pw,np.where(cc>=char_t,pc,pl))
            score=float(np.mean(pred==yval))
            key=(score,-word_t-char_t)
            if best is None or key>best[0]:best=(key,(word_t,char_t))
    return best[1]

def build_and_eval(train,val,test,seed=42):
    tx=np.asarray([x for x,y in train]); ty=np.asarray([y for x,y in train]);
    vx=np.asarray([x for x,y in val]); vy=np.asarray([y for x,y in val]);
    qx=np.asarray([x for x,y in test]); qy=np.asarray([y for x,y in test]);
    word=TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True,min_df=1)
    char=TfidfVectorizer(analyzer='char',ngram_range=(2,5),sublinear_tf=True,min_df=1)
    Xw=word.fit_transform(tx); Xc=char.fit_transform(tx)
    Vw=word.transform(vx); Vc=char.transform(vx)
    Qw=word.transform(qx); Qc=char.transform(qx)
    mw=LogisticRegression(max_iter=700,random_state=seed).fit(Xw,ty)
    mc=LogisticRegression(max_iter=700,random_state=seed).fit(Xc,ty)
    # Equal class ordering, no label ordering assumptions.
    assert np.array_equal(mw.classes_,mc.classes_)
    vw=mw.predict_proba(Vw); vc=mc.predict_proba(Vc)
    qw=mw.predict_proba(Qw); qc=mc.predict_proba(Qc)
    # Logistic late fusion as a strong conventional hybrid baseline.
    hybrid_val=(vw+vc)/2; hybrid_test=(qw+qc)/2
    pv=[];cv=[];pt=[];ct=[]
    for arrv,arrt in ((vw,qw),(vc,qc),(hybrid_val,hybrid_test)):
        a,b=top_class(arrv,mw.classes_);pv.append(a);cv.append(b)
        a,b=top_class(arrt,mw.classes_);pt.append(a);ct.append(b)
    thresholds=best_gate(pv,cv,vy,mw.classes_)
    wth,cth=thresholds
    def gate(preds,confs):
        return np.where(confs[0]>=wth,preds[0],np.where(confs[1]>=cth,preds[1],preds[2]))
    # Confidence gated ensemble. Its utility must be measured against hybrid.
    adaptive=gate(pt,ct)
    # Independent selective prediction: choose reliable labels or abstain.
    # Threshold tuned on VALIDATION for >=90% selective accuracy, maximize coverage.
    pv_gate=gate(pv,cv)
    gate_score=np.maximum.reduce([cv[0],cv[1],cv[2]])
    thresholds_coverage=np.linspace(0,1,101)
    choices=[]
    for t in thresholds_coverage:
        eligible=gate_score>=t
        if eligible.any() and np.mean(pv_gate[eligible]==vy[eligible])>=.90:
            choices.append((np.mean(eligible),-t,t))
    safe_threshold=max(choices)[2] if choices else 1.01
    test_conf=np.maximum.reduce([ct[0],ct[1],ct[2]])
    accepted=test_conf>=safe_threshold
    def row(name,pred):
        return {'method':name,'n':len(qy),'accuracy':round(float(accuracy_score(qy,pred)),6),'macro_f1':round(float(f1_score(qy,pred,average='macro',zero_division=0)),6)}
    rows=[row('word_tfidf_logistic',pt[0]),row('char_tfidf_logistic',pt[1]),row('hybrid_mean_probabilities',pt[2]),row('validation_gated_router',adaptive)]
    selective={'threshold':float(safe_threshold),'coverage':float(np.mean(accepted)),
               'accuracy_accepted':float(np.mean(adaptive[accepted]==qy[accepted])) if accepted.any() else None,
               'n_accepted':int(accepted.sum()),'n_total':int(len(qy))}
    # Paired bootstrap CI on accuracy difference adaptive - hybrid; not across datasets.
    rng=np.random.default_rng(seed)
    diff=(adaptive==qy).astype(float)-(pt[2]==qy).astype(float)
    idx=rng.integers(0,len(diff),size=(1500,len(diff)))
    ci=np.percentile(diff[idx].mean(axis=1),[2.5,97.5]).tolist()
    return {'results':rows,'paired_gain':float(diff.mean()),'bootstrap_95_ci':ci,
            'validation_gate_thresholds':{'word':wth,'char':cth},'selective':selective,
            'labels':len(set(ty)),'data':{'train':len(tx),'validation':len(vx),'test':len(qx)},
            'caveats':['Classification benchmark, not end-to-end SQL/vector/graph query execution.',
                       'TF-IDF character features are not dense neural embeddings.',
                       'Abstention confidence is not calibrated and may fail under distribution shift.',
                       'No public benchmark establishes novelty of this approach.']}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--demo',action='store_true');ap.add_argument('--out',default='results/banking77.json');a=ap.parse_args()
    if a.demo:
        # Smoke test ONLY: three classes, small manually copied real sample with minor edits.
        X,y=zip(*DEMO);xtrain,xtest,ytrain,ytest=train_test_split(X,y,test_size=.25,stratify=y,random_state=SEED)
        xtrain,xval,ytrain,yval=train_test_split(xtrain,ytrain,test_size=.33,stratify=ytrain,random_state=SEED)
        train=list(zip(xtrain,ytrain));val=list(zip(xval,yval));test=list(zip(xtest,ytest))
    else:
        full=read_split('train',Path('data/raw'));test=read_split('test',Path('data/raw'))
        texts,labels=zip(*full)
        xtrain,xval,ytrain,yval=train_test_split(texts,labels,test_size=.2,random_state=SEED,stratify=labels)
        train=list(zip(xtrain,ytrain));val=list(zip(xval,yval))
    result=build_and_eval(train,val,test)
    result['mode']='SMOKE_TEST_3_INTENTS_NOT_PUBLISHABLE' if a.demo else 'OFFICIAL_BANKING77_TEST'
    p=Path(a.out);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
