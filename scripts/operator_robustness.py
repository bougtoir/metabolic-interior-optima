"""Gate-5 targeted operator robustness: asymmetric direction-aware restriction
(fva_directional) on the 4 primary targets only, aerobic medium, pFBA selector,
full u-grid. Output: results/qc/operator_robustness_primary.csv
"""
import sys, os, json
sys.path.insert(0, 'src')
import pandas as pd
from cobra.flux_analysis import flux_variability_analysis
from utils import load_config, load_model, apply_medium, set_objective
from feasibility import feasible
from state_selection import select_state
from metrics import evaluate
from scan import scan_reaction

TARGETS = {"human2": ["MAR04373", "MAR04368"], "recon3d": ["ENO", "PGM"]}
cfg = load_config()
step = cfg["modulation"].get("u_fine_step", 0.05)
u_grid = sorted(set(cfg["modulation"]["u_coarse"]) |
                {round(step * i, 6) for i in range(int(round(1 / step)) + 1)})
rows = []
for MODEL, rids in TARGETS.items():
    model, _ = load_model(MODEL, cfg)
    apply_medium(model, cfg, "aerobic")
    set_objective(model, cfg, "atp_demand")
    ok, st, obj = feasible(model)
    assert ok, st
    fluxes, _ = select_state(model, "pfba", reference=None)
    baseline = {"objective": obj, "fluxes": fluxes, "metrics": evaluate(model, fluxes, cfg)}
    fva = flux_variability_analysis(model, reaction_list=rids,
                                    fraction_of_optimum=cfg["modulation"]["fva_fraction"],
                                    processes=1)
    for rid in rids:
        span = (float(fva.loc[rid, "minimum"]), float(fva.loc[rid, "maximum"]))
        r = scan_reaction(model, rid, cfg, "aerobic", "pfba", "fva_directional",
                          baseline, u_grid, span)
        for row in r:
            row["model"] = MODEL
        rows += r
        print(MODEL, rid, "done", flush=True)
df = pd.DataFrame(rows)
os.makedirs("results/qc", exist_ok=True)
df.to_csv("results/qc/operator_robustness_primary.csv", index=False)
print(df.groupby(["model", "reaction_id"]).atp_per_glc.max())
