"""Read-only banking-support triage demo. No customer accounts or payments touched."""
import argparse, json, sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from benchmark import DEMO, read_split


def build_model(demo=False):
    data=DEMO if demo else read_split('train',Path('data/raw'))
    x,y=zip(*data)
    vect=TfidfVectorizer(analyzer='char',ngram_range=(2,5),sublinear_tf=True)
    X=vect.fit_transform(x)
    clf=LogisticRegression(max_iter=700,random_state=42).fit(X,y)
    return vect,clf

def classify(message,vect,clf,threshold=.55):
    probs=clf.predict_proba(vect.transform([message]))[0]
    ix=int(np.argmax(probs)); score=float(probs[ix])
    intent=str(clf.classes_[ix])
    return {'trace_id':str(uuid.uuid4()),'intent':intent if score>=threshold else None,
            'confidence':round(score,4),'decision':'route_to_policy' if score>=threshold else 'human_review',
            'evidence':'char-ngram TF-IDF logistic model','customer_data_accessed':False}

def log_decision(db,question,result):
    with sqlite3.connect(db) as con:
        con.execute('CREATE TABLE IF NOT EXISTS audit (trace_id TEXT PRIMARY KEY, created_at TEXT, question TEXT, predicted_intent TEXT, decision TEXT, confidence REAL)')
        con.execute('INSERT INTO audit VALUES (?,?,?,?,?,?)',(
            result['trace_id'],datetime.now(timezone.utc).isoformat(),question,result['intent'],result['decision'],result['confidence']))

def main():
    p=argparse.ArgumentParser();p.add_argument('question');p.add_argument('--demo',action='store_true');p.add_argument('--threshold',type=float,default=.55);p.add_argument('--db',default='results/audit.sqlite3');a=p.parse_args()
    v,c=build_model(a.demo);result=classify(a.question,v,c,a.threshold)
    Path(a.db).parent.mkdir(parents=True,exist_ok=True);log_decision(a.db,a.question,result)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
