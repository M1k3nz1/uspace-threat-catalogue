# Complete threat model

The complete layered threat model of the paper: all 21 assets of the U-Space ecosystem, each with its STRIDE categories, the PASTA scenario that refines them, and its DREAD-S rating. The files here are the source of the architecture figure and the worked example in the paper, and the full model behind them.

## Files

| File | What it is |
|---|---|
| `Threat_Model.png` | The complete layered threat model: four layers, 21 assets, each annotated with its primary risk, STRIDE categories and PASTA focus. Directed arrows show the dependencies along which a compromise propagates upward. |
| `threat_model_all_assets.csv` | The same model as data: one row per asset with STRIDE assignment, PASTA stage and scenario, attack types and vectors, vulnerabilities, affected parts, raw ratings, DREAD-S score and band, evidence confidence, cross-layer propagation and regulatory references. |
| `figures/fig_architecture.pdf` (`.png`) | Layered architecture of the paper (21 assets, DREAD-S score and severity band per asset). |
| `figures/fig_threat_model_complete.pdf` (`.png`) | The complete threat model on one page, as a clean vector figure: all 21 assets in four layers, each with its DREAD-S score and band, STRIDE categories, a representative attack type and the PASTA stage. Generated from `threat_model_all_assets.csv`. |
| `figures/fig_worked_example_INF-01.pdf` (`.png`) | Worked example for one asset, GNSS / navigation sources (INF-01): asset, STRIDE, PASTA, DREAD-S, result and propagation. |
| `source/` | Scripts that regenerate the three figures (`bash build_figures.sh`; needs `pdflatex` with TikZ). Edit `make_fig_worked_example.py` to draw the same view for another asset. |

## How to read the model

1. **Asset.** The 21 assets are the nodes of the architecture (governance and strategic, service, data and information, infrastructure and physical layers). An arrow `a -> b` means that asset `b` relies on `a`, so a compromise of `a` can propagate to `b`.
2. **STRIDE.** Each asset is evaluated against the six categories (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege); the model holds 51 assignments over the 21 assets.
3. **PASTA.** Each candidate is refined into an attacker-centric scenario: attack vector, exploited weakness, affected parts, and operational consequence.
4. **DREAD-S.** Five ratings (D, R, E, A, D2; 1-10) are normalized with `nu(x) = 1 + 4(x - 1)/9`, added to the Safety Impact `S` (1-5, calibrated to SORA SAIL and ARA), and divided by six. Bands: Minimal <= 1.8, Low <= 2.6, Medium <= 3.4, High <= 4.2, Critical > 4.2.
5. **Propagation.** The cross-layer footprint of each entry feeds the propagation graph (`../edges.csv`).

Worked example (INF-01): ratings D 9, R 7, E 7, A 8, D2 6 give a sum of `nu` of 19.22; with `S` = 4 the score is (19.22 + 4) / 6 = 3.87 (High).

## Data dictionary: `threat_model_all_assets.csv`

| Column | Meaning |
|---|---|
| `id`, `layer`, `asset` | Identifier (GOV-, SVC-, DAT-, INF-), layer and asset name |
| `stride` | STRIDE categories assigned to the asset (S, T, R, ID, D, EoP) |
| `pasta_stage_focus` | PASTA stages at which the entry was principally refined |
| `attack_types`, `attack_vectors`, `vulnerabilities`, `threat_scenario`, `affected_parts`, `potential_damage` | The PASTA refinement, written at the level of the asset class, not of a product |
| `D`, `R`, `E`, `A`, `D2`, `S` | Raw ratings and Safety Impact (identical to `../ratings.csv`) |
| `dreads`, `band` | DREAD-S score (Eq. 1 of the paper) and severity band |
| `evidence` | Evidence confidence: Strong, Moderate, Weak or None |
| `cross_layer_propagation` | Layers and assets the threat can affect |
| `regulatory_reference` | Regulation (EU) 2021/664 article, Part-IS obligation, SORA SAIL level |
| `references` | Literature behind the entry |

## Scope

The model describes threat classes and architectural scenarios. It contains no exploit code and reports no vulnerability in a specific product.

## License

Data and figures: Creative Commons Attribution 4.0 International (CC BY 4.0). Code: MIT, as in the repository root.
