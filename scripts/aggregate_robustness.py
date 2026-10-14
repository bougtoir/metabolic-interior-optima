"""Aggregate robust_{MODEL}_{cond}_{sel}_{mod}.csv -> results/robustness_matrix.csv.
Uses src/classify.classify with cfg thresholds (numeric tol AND biological_threshold)
so the matrix matches the manuscript's Type II definition."""
import sys, os, glob
sys.path.insert(0, 'src')
import pandas as pd
from utils import load_config
from metrics import METRIC_META
from classify import classify

cfg = load_config()
rows = []
for f in sorted(glob.glob('results/scans/robust_*.csv')):
    if f.endswith('_fva.csv'):
        continue
    tag = os.path.basename(f).replace('robust_', '').replace('.csv', '')
    model = tag.split('_')[0]
    config = tag.split('_', 1)[1]
    d = pd.read_csv(f)
    hits = []
    for rid in d.reaction_id.unique():
        g = d[d.reaction_id == rid].sort_values('modulation_fraction')
        u = g['modulation_fraction'].values
        for met, meta in METRIC_META.items():
            J = g[met].values.astype(float)
            Ji = -J if meta['orientation'] == 'lower' else J
            cls, u_opt, info = classify(Ji, u, cfg)
            if cls == 'II':
                hits.append(f'{rid}:{met}@{u_opt:.2f}')
    rows.append(dict(model=model, config=config, n_interior=len(hits), hits=';'.join(hits)))
df = pd.DataFrame(rows)
df.to_csv('results/robustness_matrix.csv', index=False)
print(df[['model', 'config', 'n_interior']].to_string(index=False))
