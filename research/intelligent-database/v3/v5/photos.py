"""Image-to-image retrieval for real sample photographs shipped with scikit-image.
Uses only same-image augmentation retrieval: not general caption retrieval or VQA.
"""
import json, argparse, hashlib
from pathlib import Path
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from skimage import data

IMAGES=['astronaut','coffee','chelsea','rocket','camera','horse','moon','coins','page','hubble_deep_field','brick','grass','gravel','colorwheel']

def sources():
    out=[]
    for name in IMAGES:
        arr=getattr(data,name)()
        img=Image.fromarray(arr).convert('RGB').resize((96,96))
        out.append(img)
    return out

def features(img):
    color=np.asarray(img.resize((32,32)),dtype=np.float32)/255
    hist=np.concatenate([np.histogram(color[:,:,i],bins=12,range=(0,1),density=False)[0] for i in range(3)]).astype('float32')
    hist=hist/(np.linalg.norm(hist)+1e-9)
    gray=np.asarray(img.convert('L').resize((24,24)),dtype=np.float32).ravel()/255
    gray=(gray-gray.mean())/(gray.std()+1e-4)
    gray=gray/(np.linalg.norm(gray)+1e-9)
    return hist,gray

def transform(img,level,seed):
    rng=np.random.default_rng(seed)
    if level==0:return ImageEnhance.Brightness(img).enhance(float(rng.uniform(.8,1.2)))
    if level==1:return img.rotate(float(rng.uniform(-9,9)),resample=Image.Resampling.BILINEAR)
    if level==2:return img.filter(ImageFilter.GaussianBlur(radius=float(rng.uniform(.3,1.2))))
    if level==3:
        x=np.asarray(img).astype('float32'); x+=rng.normal(0,12,x.shape)
        return Image.fromarray(np.clip(x,0,255).astype('uint8'))
    raise ValueError(level)

def best(query,refs,kind):
    qh,qg=features(query)
    if kind=='color':
        scores=np.array([np.dot(qh,h) for h,g in refs])
    elif kind=='spatial':
        scores=np.array([np.dot(qg,g) for h,g in refs])
    else:
        scores=np.array([.35*np.dot(qh,h)+.65*np.dot(qg,g) for h,g in refs])
    order=np.argsort(-scores)
    return int(order[0]),float(scores[order[0]]-scores[order[1]])

def run():
    originals=sources();refs=[features(i) for i in originals]
    # Different augmentation seeds for threshold calibration and evaluation.
    validation=[(idx,transform(im,level,500+idx*10+level)) for idx,im in enumerate(originals) for level in range(4)]
    testing=[(idx,transform(im,level,900+idx*10+level)) for idx,im in enumerate(originals) for level in range(4)]
    candidates=[]
    for th in [0,.005,.01,.02,.04,.08,.12,.2,2]:
        ok=0;esc=0
        for truth,q in validation:
            first,margin=best(q,refs,'color')
            if margin>=th: pred=first
            else: pred,_=best(q,refs,'combined');esc+=1
            ok+=int(pred==truth)
        # tie break by lower cost: combined needs extra feature computation
        candidates.append((ok/len(validation),1+3*esc/len(validation),th))
    best_acc=max(x[0] for x in candidates)
    # least modeled cost within 2 percentage points of best validation accuracy
    chosen=min([c for c in candidates if c[0]>=best_acc-.02],key=lambda c:(c[1],-c[0]))
    threshold=chosen[2]
    rows=[]
    for truth,q in testing:
        c,margin=best(q,refs,'color')
        spatial,_=best(q,refs,'spatial')
        combined,_=best(q,refs,'combined')
        escalate=margin<threshold
        pred=combined if escalate else c
        rows.append({'truth':IMAGES[truth],'color':IMAGES[c],'spatial':IMAGES[spatial],'combined':IMAGES[combined],'loop':IMAGES[pred], 'escalated':escalate,'margin':margin,'valid':pred==truth})
    counts={name:sum(r[name]==r['truth'] for r in rows) for name in ['color','spatial','combined','loop']}
    result={'dataset':'scikit-image sample photographs and images','n_originals':len(originals),'n_validation_augmented':len(validation),'n_test_augmented':len(rows),'task':'retrieve SAME SOURCE image after transformations; not caption/image-semantic search','training_and_test_separation':'same image corpus; augmentation random seeds differ, so NOT held-out source photographs','threshold':threshold,'cost_proxy':{'color':1,'spatial':3,'combined':4,'loop':1+3*sum(r['escalated'] for r in rows)/len(rows)},'accuracy':{k:v/len(rows) for k,v in counts.items()},'escalations':sum(r['escalated'] for r in rows),'first_12_traces':rows[:12], 'limitations':['Same originals appear in reference set, this is near-duplicate image identification','Small sample and hand-defined image transformations','Color and spatial features are basic descriptors, not CLIP or a vision-language model','Confidence margin only detects score ambiguity, not factual truth','Modeled cost units, not measured compute or money']}
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default='results/photos.json');a=p.parse_args()
    r=run();dest=Path(a.out);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items() if k not in ('first_12_traces','limitations')},indent=2))
