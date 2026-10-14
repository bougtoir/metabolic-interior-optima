import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
df = pd.read_csv('results/robustness_matrix.csv')
df[['cond','sel','mod']] = df['config'].str.extract(r'(aerobic|glucose_limited|oxygen_limited)_(pfba|moma_linear)_(fva_informed|bound_scaling)'.replace('()','()'), expand=True)
df = df.dropna(subset=['cond'])
piv = df.pivot_table(index=['model','cond','mod'], columns='sel', values='n_interior', aggfunc='first')
models = list(piv.reset_index()['model'].unique())
fig, axes = plt.subplots(1, len(models), figsize=(5.8, 3.2), sharey=False,
                         constrained_layout=True)
for ax, model in zip(np.atleast_1d(axes), models):
    sub = piv.loc[model]
    labels = [f"{c.replace('_',' ')}\n{'FVA-informed' if m=='fva_informed' else 'bound-scaling'}"
              for c, m in sub.index]
    M = sub[['pfba','moma_linear']].fillna(0).values
    im = ax.imshow(M, cmap='YlOrRd', vmin=0, vmax=12, aspect='auto')
    ax.set_xticks([0,1]); ax.set_xticklabels(['pFBA','L1-MOMA'], fontsize=7)
    ax.set_yticks(range(len(labels)))
    if ax is np.atleast_1d(axes)[0]:
        ax.set_yticklabels(labels, fontsize=6.5)
    else:
        ax.set_yticklabels([])
    ax.set_title(model, fontsize=8)
    for i in range(M.shape[0]):
        for j in range(2):
            ax.text(j, i, int(M[i,j]), ha='center', va='center', fontsize=8)
fig.suptitle('Interior-optimum combos per cell', fontsize=9)
fig.colorbar(im, ax=np.atleast_1d(axes).tolist(), shrink=0.7, pad=0.02)
fig.savefig('figures/fig5_robustness.png', dpi=300)
print('saved fig5')
