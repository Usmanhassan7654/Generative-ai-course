import json,time
from .core import Evidence,Principal,Request,Planner
now=int(time.time())
rows=[Evidence('a','The card was dispatched to the delivery service','A',0,now,'record','card','demo/a'),
      Evidence('b','The shipping provider tracking information is available','A',0,now,'document','card','demo/b'),
      Evidence('c','Your private financial record is secret','B',2,now,'record',None,'demo/c'),
      Evidence('d','Card dispatch status from two years ago','A',0,now-86400*730,'record',None,'demo/d')]
p=Planner(rows,[('a','b'),('a','c')]); q=Request('card dispatch',Principal('A',0),now,max_age_seconds=86400*30,requires_multihop=True)
print(json.dumps(p.run(q),indent=2))
