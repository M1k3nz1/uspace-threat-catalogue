# LLM-rater study: computed results
Models: LLM A (Claude Sonnet 5.5), LLM B (Claude Haiku 5.5), LLM C (Claude Opus 4.6), LLM D (Claude Opus 5), LLM E (Claude Opus 5.5)
Published mean DREAD-S: 3.71

## LLM A (Claude Sonnet 5.5) (K=3 runs)
| Dim | alpha | ICC(2,1) | MAD vs published | within +-1 (DREAD-S: same band) |
|---|---|---|---|---|
| D | 0.88 | 0.88 | 1.35 | 0.57 |
| R | 0.89 | 0.89 | 1.16 | 0.68 |
| E | 0.90 | 0.90 | 1.87 | 0.46 |
| A | 0.88 | 0.88 | 1.57 | 0.59 |
| D2 | 0.91 | 0.92 | 1.89 | 0.38 |
| S | 0.91 | 0.91 | 0.57 | 0.92 |
| DREAD-S | 0.94 | 0.94 | 0.49 | 0.49 |

Run-to-run MAD (5 DREAD ratings): 0.43; MAD vs published: five ratings 1.57, S 0.57; signed mean (LLM - published) D,R,E,A,D2,S = [-1.22, -0.14, -1.81, -1.13, -0.94, -0.35]; mean DREAD-S 3.26

| Rater | tau | bands changed | bands raised | top-7 overlap | first | INF-02 rank | gov in 5 lowest | highest band |
|---|---|---|---|---|---|---|---|---|
| run 1 | 0.61 | 10 | 0 | 0.71 | INF-01 | 5 | 1.00 | High |
| run 2 | 0.52 | 11 | 0 | 0.57 | INF-01 | 4 | 0.67 | High |
| run 3 | 0.54 | 11 | 0 | 0.57 | INF-01 | 6 | 1.00 | High |
| median of runs | 0.54 | 10 | 0 | 0.71 | INF-01 | 3 | 0.67 | High |

## LLM B (Claude Haiku 5.5) (K=3 runs)
| Dim | alpha | ICC(2,1) | MAD vs published | within +-1 (DREAD-S: same band) |
|---|---|---|---|---|
| D | 0.89 | 0.90 | 1.21 | 0.71 |
| R | 0.81 | 0.81 | 1.19 | 0.65 |
| E | 0.82 | 0.83 | 1.62 | 0.49 |
| A | 0.75 | 0.75 | 1.46 | 0.62 |
| D2 | 0.84 | 0.84 | 2.37 | 0.27 |
| S | 0.93 | 0.93 | 0.65 | 0.92 |
| DREAD-S | 0.88 | 0.89 | 0.50 | 0.46 |

Run-to-run MAD (5 DREAD ratings): 0.70; MAD vs published: five ratings 1.57, S 0.65; signed mean (LLM - published) D,R,E,A,D2,S = [-1.05, 0.05, -1.4, -0.92, -1.6, -0.4]; mean DREAD-S 3.28

| Rater | tau | bands changed | bands raised | top-7 overlap | first | INF-02 rank | gov in 5 lowest | highest band |
|---|---|---|---|---|---|---|---|---|
| run 1 | 0.48 | 13 | 0 | 0.71 | INF-01 | 5 | 1.00 | High |
| run 2 | 0.57 | 10 | 1 | 0.71 | INF-01 | 4 | 1.00 | Critical |
| run 3 | 0.50 | 11 | 2 | 0.57 | INF-01 | 3 | 1.00 | Critical |
| median of runs | 0.50 | 11 | 1 | 0.71 | INF-01 | 4 | 1.00 | Critical |

## LLM C (Claude Opus 4.6) (K=3 runs)
| Dim | alpha | ICC(2,1) | MAD vs published | within +-1 (DREAD-S: same band) |
|---|---|---|---|---|
| D | 0.86 | 0.86 | 0.86 | 0.79 |
| R | 0.79 | 0.79 | 0.95 | 0.73 |
| E | 0.84 | 0.84 | 1.60 | 0.52 |
| A | 0.80 | 0.80 | 1.30 | 0.59 |
| D2 | 0.92 | 0.92 | 1.67 | 0.49 |
| S | 0.93 | 0.93 | 0.78 | 0.92 |
| DREAD-S | 0.95 | 0.95 | 0.34 | 0.65 |

Run-to-run MAD (5 DREAD ratings): 0.43; MAD vs published: five ratings 1.28, S 0.78; signed mean (LLM - published) D,R,E,A,D2,S = [-0.41, 0.22, -1.51, -0.41, -1.19, 0.27]; mean DREAD-S 3.51

| Rater | tau | bands changed | bands raised | top-7 overlap | first | INF-02 rank | gov in 5 lowest | highest band |
|---|---|---|---|---|---|---|---|---|
| run 1 | 0.48 | 8 | 0 | 0.57 | INF-01 | 5 | 0.67 | High |
| run 2 | 0.46 | 7 | 1 | 0.71 | INF-01 | 6 | 0.67 | High |
| run 3 | 0.50 | 7 | 0 | 0.71 | INF-01 | 5 | 0.67 | High |
| median of runs | 0.46 | 9 | 0 | 0.71 | INF-01 | 6 | 0.67 | High |

## LLM D (Claude Opus 5) (K=3 runs)
| Dim | alpha | ICC(2,1) | MAD vs published | within +-1 (DREAD-S: same band) |
|---|---|---|---|---|
| D | 0.91 | 0.91 | 1.13 | 0.67 |
| R | 0.89 | 0.89 | 1.19 | 0.65 |
| E | 0.93 | 0.94 | 1.79 | 0.46 |
| A | 0.91 | 0.91 | 1.54 | 0.57 |
| D2 | 0.91 | 0.92 | 2.00 | 0.41 |
| S | 0.91 | 0.91 | 0.65 | 0.98 |
| DREAD-S | 0.96 | 0.96 | 0.47 | 0.43 |

Run-to-run MAD (5 DREAD ratings): 0.47; MAD vs published: five ratings 1.53, S 0.65; signed mean (LLM - published) D,R,E,A,D2,S = [-0.97, -0.21, -1.7, -0.81, -1.49, 0.02]; mean DREAD-S 3.33

| Rater | tau | bands changed | bands raised | top-7 overlap | first | INF-02 rank | gov in 5 lowest | highest band |
|---|---|---|---|---|---|---|---|---|
| run 1 | 0.60 | 12 | 1 | 0.57 | INF-01 | 3 | 0.67 | Critical |
| run 2 | 0.40 | 12 | 1 | 0.57 | INF-01 | 2 | 0.67 | Critical |
| run 3 | 0.59 | 12 | 1 | 0.71 | INF-01 | 2 | 1.00 | Critical |
| median of runs | 0.56 | 12 | 1 | 0.71 | INF-01 | 2 | 0.67 | Critical |

## LLM E (Claude Opus 5.5) (K=3 runs)
| Dim | alpha | ICC(2,1) | MAD vs published | within +-1 (DREAD-S: same band) |
|---|---|---|---|---|
| D | 0.94 | 0.94 | 1.27 | 0.59 |
| R | 0.92 | 0.93 | 1.38 | 0.56 |
| E | 0.93 | 0.93 | 1.92 | 0.49 |
| A | 0.92 | 0.93 | 1.83 | 0.56 |
| D2 | 0.89 | 0.89 | 2.16 | 0.40 |
| S | 0.94 | 0.94 | 0.71 | 0.95 |
| DREAD-S | 0.94 | 0.94 | 0.51 | 0.48 |

Run-to-run MAD (5 DREAD ratings): 0.48; MAD vs published: five ratings 1.71, S 0.71; signed mean (LLM - published) D,R,E,A,D2,S = [-1.08, -0.08, -1.73, -1.29, -1.37, -0.08]; mean DREAD-S 3.29

| Rater | tau | bands changed | bands raised | top-7 overlap | first | INF-02 rank | gov in 5 lowest | highest band |
|---|---|---|---|---|---|---|---|---|
| run 1 | 0.57 | 10 | 1 | 0.71 | INF-01 | 4 | 1.00 | Critical |
| run 2 | 0.47 | 11 | 1 | 0.71 | INF-01 | 6 | 0.67 | Critical |
| run 3 | 0.44 | 12 | 1 | 0.71 | INF-01 | 5 | 0.67 | Critical |
| median of runs | 0.45 | 12 | 1 | 0.71 | INF-01 | 5 | 0.67 | Critical |

## All 15 runs pooled
| Dim | alpha | ICC(2,1) | MAD vs published | within +-1 |
|---|---|---|---|---|
| D | 0.82 | 0.83 | 1.16 | 0.67 |
| R | 0.81 | 0.82 | 1.17 | 0.65 |
| E | 0.77 | 0.78 | 1.76 | 0.49 |
| A | 0.79 | 0.80 | 1.54 | 0.58 |
| D2 | 0.82 | 0.83 | 2.02 | 0.39 |
| S | 0.86 | 0.87 | 0.67 | 0.94 |
| DREAD-S | 0.87 | 0.88 | 0.46 | 0.50 |

| Rater | tau | bands changed | bands raised | top-7 overlap | first | INF-02 rank | gov in 5 lowest | highest band |
|---|---|---|---|---|---|---|---|---|
| median of all runs | 0.53 | 11 | 1 | 0.71 | INF-01 | 3 | 1.00 | Critical |

## Between-model agreement (means of each model's runs)

LLM A (Claude Sonnet 5.5) vs LLM B (Claude Haiku 5.5)
| Dim | Pearson r | MAD of run means |
|---|---|---|
| D | 0.91 | 0.43 |
| R | 0.91 | 0.44 |
| E | 0.87 | 0.73 |
| A | 0.84 | 0.65 |
| D2 | 0.88 | 0.89 |
| S | 0.96 | 0.24 |
| DREAD-S tau | 0.84 | 0.15 |

LLM A (Claude Sonnet 5.5) vs LLM C (Claude Opus 4.6)
| Dim | Pearson r | MAD of run means |
|---|---|---|
| D | 0.93 | 0.81 |
| R | 0.90 | 0.59 |
| E | 0.75 | 0.81 |
| A | 0.93 | 0.75 |
| D2 | 0.88 | 0.57 |
| S | 0.94 | 0.62 |
| DREAD-S tau | 0.80 | 0.26 |

LLM A (Claude Sonnet 5.5) vs LLM D (Claude Opus 5)
| Dim | Pearson r | MAD of run means |
|---|---|---|
| D | 0.94 | 0.44 |
| R | 0.94 | 0.51 |
| E | 0.91 | 0.49 |
| A | 0.92 | 0.57 |
| D2 | 0.93 | 0.65 |
| S | 0.96 | 0.37 |
| DREAD-S tau | 0.80 | 0.16 |

LLM A (Claude Sonnet 5.5) vs LLM E (Claude Opus 5.5)
| Dim | Pearson r | MAD of run means |
|---|---|---|
| D | 0.93 | 0.56 |
| R | 0.95 | 0.63 |
| E | 0.92 | 0.49 |
| A | 0.92 | 0.63 |
| D2 | 0.95 | 0.59 |
| S | 0.93 | 0.40 |
| DREAD-S tau | 0.80 | 0.16 |

LLM B (Claude Haiku 5.5) vs LLM C (Claude Opus 4.6)
| Dim | Pearson r | MAD of run means |
|---|---|---|
| D | 0.89 | 0.70 |
| R | 0.89 | 0.59 |
| E | 0.60 | 0.78 |
| A | 0.89 | 0.67 |
| D2 | 0.89 | 0.79 |
| S | 0.94 | 0.70 |
| DREAD-S tau | 0.80 | 0.25 |

LLM B (Claude Haiku 5.5) vs LLM D (Claude Opus 5)
| Dim | Pearson r | MAD of run means |
|---|---|---|
| D | 0.93 | 0.46 |
| R | 0.96 | 0.51 |
| E | 0.94 | 0.56 |
| A | 0.90 | 0.59 |
| D2 | 0.90 | 0.52 |
| S | 0.96 | 0.41 |
| DREAD-S tau | 0.85 | 0.14 |

LLM B (Claude Haiku 5.5) vs LLM E (Claude Opus 5.5)
| Dim | Pearson r | MAD of run means |
|---|---|---|
| D | 0.87 | 0.67 |
| R | 0.92 | 0.63 |
| E | 0.78 | 0.87 |
| A | 0.88 | 0.78 |
| D2 | 0.90 | 0.65 |
| S | 0.92 | 0.41 |
| DREAD-S tau | 0.78 | 0.15 |

LLM C (Claude Opus 4.6) vs LLM D (Claude Opus 5)
| Dim | Pearson r | MAD of run means |
|---|---|---|
| D | 0.94 | 0.65 |
| R | 0.94 | 0.75 |
| E | 0.77 | 0.83 |
| A | 0.93 | 0.65 |
| D2 | 0.90 | 0.68 |
| S | 0.96 | 0.32 |
| DREAD-S tau | 0.81 | 0.25 |

LLM C (Claude Opus 4.6) vs LLM E (Claude Opus 5.5)
| Dim | Pearson r | MAD of run means |
|---|---|---|
| D | 0.90 | 0.76 |
| R | 0.96 | 0.87 |
| E | 0.88 | 0.76 |
| A | 0.93 | 1.00 |
| D2 | 0.87 | 0.71 |
| S | 0.93 | 0.38 |
| DREAD-S tau | 0.81 | 0.25 |

LLM D (Claude Opus 5) vs LLM E (Claude Opus 5.5)
| Dim | Pearson r | MAD of run means |
|---|---|---|
| D | 0.95 | 0.43 |
| R | 0.96 | 0.35 |
| E | 0.91 | 0.48 |
| A | 0.92 | 0.70 |
| D2 | 0.97 | 0.35 |
| S | 0.96 | 0.25 |
| DREAD-S tau | 0.85 | 0.11 |
