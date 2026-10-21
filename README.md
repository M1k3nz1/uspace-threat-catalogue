# U-Space Threat Catalogue: data and analysis code

Open supporting material for a paper on a layered threat model for U-Space
(currently under review; details withheld for double-anonymous review).

The repository contains the threat-catalogue ratings, the cross-layer propagation
graph, the complete threat model with its figures, and a script that recomputes every
quantitative result reported in the paper.

## Contents

| File | What it is |
|---|---|
| `ratings.csv` | The 21 catalogue entries: layer, raw DREAD ratings (D, R, E, A, D2; scale 1-10), Safety Impact S (1-5), evidence confidence (Strong / Moderate / Weak / None) |
| `edges.csv` | The 45 propagation edges: source, target, mechanism (Integrity / trust, Availability, Oversight), basis, resolution rule |
| `uspace_scoring_and_propagation.xlsx` | Workbook with three sheets: scoring (live Eq. 1 formula and severity bands), propagation edges, blast radius per asset |
| `reproduce.py` | Recomputes scores, bands, graph structure, chains, cuts, adjusted severity and the sensitivity analysis, and checks 14 values reported in the paper |
| `threat-model/` | The complete layered threat model: per-asset data for all 21 assets (`threat_model_all_assets.csv`), the complete one-page figure, the architecture figure, the INF-01 worked example, and the scripts that regenerate the figures. See its own README |
| `llm-rater-study/` | Prompts, raw responses, extracted ratings, analysis scripts and tables of the LLM-rater study |
| `LICENSE` | MIT license for the code |

## Quick start

    pip install numpy scipy networkx
    python3 reproduce.py

The script prints its results and ends with `14/14 self-checks passed`. It exits with
code 0 if every check passes and 1 otherwise. No other software or data is needed.
The sensitivity analysis uses fixed random seeds, so the output is identical on every run.

## Method in brief

Eq. 1 (DREAD-S): DREAD-S = ( sum over {D, R, E, A, D2} of [1 + 4/9 (x - 1)] + S ) / 6.
Each 1-10 rating is rescaled to 1-5, so the score lies in [1, 5].

Severity bands: Minimal <= 1.8, Low <= 2.6, Medium <= 3.4, High <= 4.2, Critical > 4.2.

Propagation graph: 19 assets as nodes, 45 directed edges ("a compromise of the source
can affect the target"). The two systemic entries, GOV-02 (regulatory framework) and
INF-07 (supply chain), declare reach into all layers and are not graph nodes.

## Data dictionary

`ratings.csv`

| Column | Meaning |
|---|---|
| `id` | Entry identifier: GOV-, SVC-, DAT-, INF- followed by a number (governance, service, data, infrastructure layer) |
| `layer`, `asset` | Layer and asset name |
| `D`, `R`, `E`, `A`, `D2` | DREAD ratings: damage, reproducibility, exploitability, affected users, discoverability (1-10) |
| `S` | Safety Impact, calibrated to the SORA SAIL and ARA categories (1-5) |
| `evidence` | Strength of the documented evidence behind the entry |

`edges.csv`

| Column | Meaning |
|---|---|
| `source`, `target` | Asset identifiers |
| `mechanism` | Integrity / trust, Availability, or Oversight |
| `basis` | `Footprint names asset` (named directly), `Scenario` (stated in the threat scenario), or `Mapped by rule` (resolved from a general phrase) |
| `rule` | `N` (named), `S` (scenario), or `R1` to `R5` (the five published resolution rules) |

## Changing the data

Edit a rating in `ratings.csv`, or add or remove a row in `edges.csv`, and run the
script again. Scores, bands, the core of the graph, chains, gates and the sensitivity
results update automatically. Some of the 14 self-checks will report `MISMATCH` after
a change, because they compare against the values published in the paper; this is
expected and shows what the change affected.

## Scope

The material describes threat classes and architectural scenarios. It contains no
exploit code and reports no vulnerability in a specific product.

## Versions

`v1.0.1` corresponds to the version of the paper submitted for review. It adds the
`threat-model/` folder to `v1.0.0`; the ratings, edges and analysis script are unchanged.
Later changes are recorded as new versions.

## License

Code: MIT (see `LICENSE`). Data files (`ratings.csv`, `edges.csv`, the workbook,
`threat-model/`): Creative Commons Attribution 4.0 International (CC BY 4.0),
https://creativecommons.org/licenses/by/4.0/
