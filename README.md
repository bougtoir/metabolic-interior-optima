# metabolic-interior-optima

Reproduction materials for the manuscript *"Selection-rule-dependent interior modulation optima in human genome-scale metabolic networks"* (Onishi Tatsuki). The repository contains the analysis code, configuration, frozen result CSVs, figures, unit tests, and data provenance — no manuscript or submission files.

## Contents

- `src/` — pipeline modules (feasibility, state selection, modulation operators, metrics, scan driver, classification)
- `scripts/` — scan drivers, figure/table builders, `build_docx.py`, `operator_robustness.py`
- `config/config.yaml` — all parameters (media, grids, FVA fraction, thresholds, seeds)
- `results/` — robustness matrix, scan CSVs, QC outputs
- `figures/` — generated figure PNGs
- `data/` — acquisition ledger (model provenance, SHA-256), hit families, target–modulator map
- `tests/` — pytest suite (12 tests)

## Setup

    pip install -r requirements.txt

## Model files (not redistributed)

The frozen genome-scale models are not committed for licensing reasons. Re-acquire them exactly as recorded in `data/raw/acquisition_ledger.csv` (source URL, version, retrieval date, SHA-256) and place them at:

- `models/human2/Human-GEM.xml` (Human-GEM v2.0.1)
- `models/recon3d/Recon3DModel_301.xml` (Recon3D v301)

Verify each file's SHA-256 against the ledger before running.

## Reproduce

1. `python3 -m pytest tests/ -q` — expect 12/12 passing.
2. Figures: `python3 scripts/make_figures.py`, `make_fig1.py`, `make_fig2.py`, `make_fig5.py`.
3. Re-scan (requires model files): `python3 scripts/full_scan.py <model> aerobic pfba fva_informed`; targeted operator robustness: `python3 scripts/operator_robustness.py`.
4. All reported numbers are regenerated from result CSVs; nothing is hardcoded.

## Notes

- Screening is a prespecified conservative staged screen, not an exhaustive census (see manuscript STAR Methods).
- Solver: GLPK via cobra/optlang (swiglpk).

Citation: see the accompanying manuscript's availability statement (tag `v1.0-submission`).
