"""Repeated split experiment, no significance claim without independent datasets."""
import json,statistics
from pathlib import Path
from experiment import evaluate
S=(20261021,20261022,20261023)
all_runs={str(seed):{name:evaluate(name,seed) for name in ('digits','iris')} for seed in S}
summaries={}
for name in ('digits','iris'):
  summaries[name]={method:{'accuracy_mean':statistics.mean(all_runs[str(s)][name]['metrics'][method]['accuracy'] for s in S),'accuracy_std':statistics.stdev(all_runs[str(s)][name]['metrics'][method]['accuracy'] for s in S),'mean_proxy_cost':statistics.mean(all_runs[str(s)][name]['metrics'][method]['cost_proxy'] for s in S)} for method in ('fast_only','full_only','strong_only','single_route','loop')}
obj={'seeds':S,'summary':summaries,'runs':all_runs}
p=Path('results/repeated.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2));print(json.dumps(summaries,indent=2))
