# LLM-rater study for the U-Space Threat Catalogue

This folder contains everything needed to reproduce the reliability study reported in Section 8.5 of the paper
("Reliability with LLM Raters"): the prompts, the ratings of every run, the published ratings used as the baseline,
the analysis script, and the computed results. It is organised to be copied into the GitHub repository as it is.

## Question
How far do the DREAD-S ratings of the catalogue depend on the individual assessor? Large language models from two providers act as
expert raters of the same 21 assets with the same rubric. Their runs are compared with each other and with the
published ratings. Agreement is read as evidence that the rubric can be applied consistently, not as evidence that
the ratings are correct.

## Protocol
- **Task.** Rate each of the 21 catalogue entries with the five DREAD ratings (1-10) and the Safety Impact S (1-5, calibrated to SORA SAIL and EUROCONTROL ARA).
- **Prompt.** Role statement, the six scales with anchors, the instruction to be discriminating, and the 21 entries (asset, attack types, vectors, vulnerabilities, threat scenario). It contains no published ratings, scores, bands or evidence confidence.
- **Runs.** K = 3 runs per model, each in a fresh session with no web access and no access to the published ratings. The entry order differs per run (`prompts/prompt_order1..3.txt`, orders in `prompts/entry_orders.json`). Run n of every model uses `prompt_order{n}.txt`.
- **Settings.** High reasoning effort for the five Claude models. For GPT-6 (LLM F) the reasoning level could not be selected in the chat interface and was left at its default. Sampling parameters are the defaults of each model and were not changed.
- **Output.** One JSON array with one object per entry (`id`, `D`, `R`, `E`, `A`, `D2`, `S`, `rationale`).

Prompt checksums (SHA-256):

| File | SHA-256 |
|---|---|
| prompts/prompt_order1.txt | 6a6f74316e57a5f4c305bf7ebac29bde816eeeb7ee544082f883b06a99739891 |
| prompts/prompt_order2.txt | a1e81ddf00e9980673bb803b4d8bf3ffe88b3844518a928657c4eae1933daf3c |
| prompts/prompt_order3.txt | 36a9022966902fb632ec5b587c9d92d385152fac24dd27b06c106cc1aef6b2dc |

## Models
| Label | Model | Effort | Runs | How run | Rationales stored |
|---|---|---|---|---|---|
| LLM A | Claude Sonnet 5.5 (`claude-sonnet-5-5`) | High | 3 | fresh agent sessions, October 2026 | no |
| LLM B | Claude Haiku 5.5 | High | 3 | fresh agent sessions, October 2026 | no |
| LLM C | Claude Opus 4.6 | High | 3 | new chat sessions, October 2026 | yes |
| LLM D | Claude Opus 5 | High | 3 | new chat sessions, October 2026 | yes |
| LLM E | Claude Opus 5.5 | High | 3 | new chat sessions, October 2026 | yes |
| LLM F | OpenAI GPT-6 (reasoning model) | not selectable (default) | 3 | new temporary chat per run, web search, memory, custom instructions, attachments, connectors and tools off; no API session; October 2026 | yes |

Six models, 18 runs and 378 ratings in total (five Claude models, 15 runs; one OpenAI model, 3 runs). Model versions are recorded as selected by the person running the session. A subagent cannot verify its own model identity.
Run n of every model used `prompts/prompt_order{n}.txt`, so all models saw the same three entry orders.

## Layout
```
README.md                    this file
HOWTO_RUN_OTHER_MODELS.md    how to run a further model and add its runs
input/published_ratings.csv  published ratings of the catalogue (baseline)
input/edges.csv              propagation edges (not used by this study)
prompts/                     the three prompts and the entry orders
raw_responses/               model responses as JSON, one file per run
ratings/ratings_all_runs.csv all ratings in long format (id, model, run, D, R, E, A, D2, S)
scripts/analyze.py           computes all statistics (numpy, scipy)
scripts/add_run.py           validates a JSON response and appends it to the ratings CSV
results/                     computed tables (summary.md and CSV files)
results/paper_tables.md      the numbers of the three LLM tables of Section 8.5
figures/                     three figures (PDF for LaTeX, PNG 300 dpi) and figures/data/*.csv (the numbers behind each panel)
scripts/make_figures.py      regenerates the figures (numpy, scipy, matplotlib)
```

## Main findings
- Within a model the runs agree closely for both providers (alpha 0.73-0.94 per rated dimension, at least 0.88 for DREAD-S).
- Against the published ratings the offset depends on the provider: the five Claude models rate Exploitability and Discoverability lower (0.9-1.8 points), GPT-6 is close on those but rates Reproducibility 1.5 points and S 0.5 points higher.
- Models of the same provider agree most (Kendall tau 0.78-0.85 between Claude models, 0.60-0.76 between GPT-6 and a Claude model, 0.48-0.55 between a model and the published ranking).
- No model reproduces the exact scores, the bands or the first place of INF-02 (never first in any of the 18 runs). The Safety impact S is reproduced within one level for 92 % of the 378 ratings.

See `results/summary.md` and `results/paper_tables.md` for the numbers.

## Reproduce
```
cd scripts
python3 analyze.py        # writes ../results/summary.md and ../results/*.csv
```

## Measures
- Krippendorff's alpha (interval scale) and ICC(2,1) across the runs of a model, per dimension and for DREAD-S.
- Mean absolute deviation (MAD) from the published rating, and the share within +-1 of it (for DREAD-S, the share of entries that stay in their band).
- DREAD-S = (sum of nu(x) over D, R, E, A, D2, plus S) / 6 with nu(x) = 1 + 4(x-1)/9. Bands: Minimal <= 1.8, Low <= 2.6, Medium <= 3.4, High <= 4.2, Critical > 4.2.
- Ranking effect: Kendall's tau with the published ranking, number of entries that change band, top-7 overlap, whether INF-02 ranks first, and the share of the three governance entries among the five lowest.
- Between models: Pearson correlation and MAD of the run means, Kendall's tau between DREAD-S rankings, and a comparison of pairs from the same provider (Claude vs Claude) with pairs from different providers (Claude vs GPT-6). Pooled statistics are given for the 15 Claude runs and for all 18 runs.

## Known limits
- The responses of LLM A and LLM B are stored as ratings only; their one-sentence rationales were not retained. The responses of LLM C, D, E and F include the rationales.
- Five of the six models come from one provider (Anthropic) and one from OpenAI, so a provider effect rests on a single OpenAI model; the study measures consistency, not validity. Model size and release date differ together, so their effects cannot be separated. The reasoning level of GPT-6 could not be selected.
- LLM A and B were run as agent sessions and LLM C to F as chat sessions; the prompt text is identical.
- Results depend on the prompt wording and on model versions that change over time.

## Figures
| File | Content |
|---|---|
| `figures/fig1_overview` | a) consistency of each model (alpha); b) bias against the published ratings per dimension; c) closest model; d) band distribution; e) ranking agreement (tau); f) rank of INF-02; g) Safety-impact agreement |
| `figures/fig2_where_models_disagree` | a) mean LLM minus published, every entry and rating; b) the twelve largest gaps with each model's mean |
| `figures/fig3_models_vs_published` | a) tau between models and against the published ranking; b) deviation between two Claude models, between GPT-6 and a Claude model, and between each model and the published ratings |

Colour: each LLM keeps one colour in every panel (blue A, orange B, aqua C, yellow D, magenta E, green F). Aqua, yellow and magenta have low contrast on white, so every
mark is also identified by a label, a legend or a row name, and `figures/data/*.csv` is the table view of each chart.
Regenerate with `cd scripts && python3 make_figures.py` (needs matplotlib, numpy, pandas and the Inter font; without Inter, change `font.family` at the top of the script).

## Licence
Data (prompts, responses, ratings, results, figures) are released under the Creative Commons Attribution 4.0 International
licence (CC BY 4.0), and the scripts under the MIT licence, the same terms as the rest of this repository.
