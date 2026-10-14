import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

p = pd.read_csv('manuscript/table1_primary_nopm.csv')
short = {'enolase': 'ENO', 'phosphoglycerate mutase': 'PGM'}
labels = [f"{m}-{short.get(n, n)}\n{e.replace('atp_per_', 'ATP/')}" for m, n, e in zip(p.model, p.name, p.endpoint)]
x = np.arange(len(p)); w = 0.27
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.bar(x - w, p['J(0)'], w, label='J(0) unperturbed', color='#9ecae1')
ax.bar(x, p['J(u*)'], w, label='J(u*) interior optimum', color='#08519c')
ax.bar(x + w, p['J(1)'], w, label='J(1) full restriction', color='#c7e9c0')
for xi, (u, js) in enumerate(zip(p['u*'], p['J(u*)'])):
    ax.annotate(f"u*={u}", (xi, js), textcoords='offset points', xytext=(0, 3), ha='center', fontsize=7)
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=7)
ax.axvspan(3.5, len(p) - 0.5, color='grey', alpha=0.06)
ax.text(1.5, ax.get_ylim()[1] * 0.95, 'Human-GEM (mid-glycolysis)', ha='center', fontsize=8, style='italic')
ax.text(5.5, ax.get_ylim()[1] * 0.95, 'Recon3D (mid-glycolysis)', ha='center', fontsize=8, style='italic')
ax.set_ylabel('Endpoint value J')
ax.set_title('Primary independent interior optima: mid-glycolysis family replicates across models')
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig('figures/fig2_family_map.png', dpi=200)
print('saved figures/fig2_family_map.png')
