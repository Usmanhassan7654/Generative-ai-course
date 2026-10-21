"""Cross-feature agreement on V5 photographic near-duplicate retrieval; not visual QA."""
import argparse,json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent/'reference_v5'))
from photos import sources,features,transform,IMAGES,best

def evaluate():
    original=sources();refs=[features(p) for p in original]
    testing=[(i,transform(im,level,900+i*10+level)) for i,im in enumerate(original) for level in range(4)]
    counts={'color':0,'spatial':0,'combined':0,'v6':0};errors=[];abstain=0;accepted=0
    for truth,q in testing:
        c,_=best(q,refs,'color');s,_=best(q,refs,'spatial');u,_=best(q,refs,'combined')
        for mode,p in [('color',c),('spatial',s),('combined',u)]:counts[mode]+=int(p==truth)
        # Agreement verification; if conflicting, use combined evidence but abstain unless two agree.
        votes=[c,s,u];candidate=max(set(votes),key=lambda j:(votes.count(j),-j))
        pred=candidate if votes.count(candidate)>=2 else None
        abstain+=pred is None;accepted+=pred is not None
        counts['v6']+=int(pred==truth) if pred is not None else 0
        if pred is None or pred!=truth:errors.append({'true':IMAGES[truth],'color':IMAGES[c],'spatial':IMAGES[s],'combined':IMAGES[u],'v6':None if pred is None else IMAGES[pred]})
    n=len(testing)
    return {'dataset':'14 scikit-image sample photographs with augmentation; source images occur in reference set','n':n,'counts':counts,'accuracy':{k:v/n for k,v in counts.items()},'coverage':accepted/n,'abstentions':abstain,'errors':errors,'limitations':['Same source images in gallery, augmented queries only','Feature agreement is not independent provenance and is not an image-language model','No train/test photo identity isolation','Images are loaded from scikit-image at runtime, not included in repository']}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default='results/photos_v6.json');args=p.parse_args();r=evaluate();Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items() if k!='errors'},indent=2))
