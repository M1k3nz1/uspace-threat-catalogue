# Calibrated validation results

## 1. Rating perturbation: paper scheme vs disagreement observed between raters
pm1: tau=0.87 bands_changed=2.5 top7=0.94 INF-02_first=0.74 INF-02_top3=0.96 gov_in_lowest5=0.99
pool_independent: tau=0.51 bands_changed=9.1 top7=0.64 INF-02_first=0.06 INF-02_top3=0.35 gov_in_lowest5=0.86
one_rater: tau=0.53 bands_changed=9.2 top7=0.65 INF-02_first=0.04 INF-02_top3=0.27 gov_in_lowest5=0.85

Tier membership (independent rater-pool draws): P(asset in top 11 of 21)
  SVC-04 published 3.87 rank 8  P(top11)=1.00  P(keeps published band)=0.87
  INF-01 published 3.87 rank 8  P(top11)=1.00  P(keeps published band)=0.47
  DAT-01 published 4.09 rank 7  P(top11)=1.00  P(keeps published band)=0.98
  SVC-03 published 4.11 rank 6  P(top11)=1.00  P(keeps published band)=0.97
  INF-02 published 4.41 rank 1  P(top11)=1.00  P(keeps published band)=0.03
  DAT-02 published 4.26 rank 2  P(top11)=0.99  P(keeps published band)=0.02
  DAT-06 published 4.17 rank 4  P(top11)=0.98  P(keeps published band)=1.00
  SVC-02 published 4.17 rank 4  P(top11)=0.98  P(keeps published band)=1.00
  SVC-05 published 3.48 rank 15  P(top11)=0.93  P(keeps published band)=0.98
  INF-07 published 4.19 rank 3  P(top11)=0.56  P(keeps published band)=0.60
  INF-03 published 3.65 rank 13  P(top11)=0.51  P(keeps published band)=0.59
  INF-05 published 3.72 rank 12  P(top11)=0.38  P(keeps published band)=0.49
  DAT-03 published 3.41 rank 16  P(top11)=0.28  P(keeps published band)=0.44
  DAT-05 published 3.78 rank 10  P(top11)=0.13  P(keeps published band)=0.17
  INF-04 published 3.11 rank 18  P(top11)=0.10  P(keeps published band)=0.83
  SVC-01 published 3.78 rank 10  P(top11)=0.10  P(keeps published band)=0.21
  GOV-02 published 2.87 rank 21  P(top11)=0.04  P(keeps published band)=0.89
  INF-06 published 3.19 rank 17  P(top11)=0.02  P(keeps published band)=0.95
  DAT-04 published 3.63 rank 14  P(top11)=0.00  P(keeps published band)=0.00
  GOV-01 published 3.09 rank 19  P(top11)=0.00  P(keeps published band)=0.38
  GOV-03 published 3.09 rank 19  P(top11)=0.00  P(keeps published band)=0.04
stable upper tier (>=0.8): 9 ['SVC-04', 'INF-01', 'DAT-01', 'SVC-03', 'INF-02', 'DAT-02', 'DAT-06', 'SVC-02', 'SVC-05']
stable lower tier (<=0.2): 8 ['GOV-01', 'GOV-03', 'DAT-04', 'INF-06', 'GOV-02', 'SVC-01', 'INF-04', 'DAT-05']
uncertain: 4 ['DAT-03', 'INF-03', 'INF-05', 'INF-07']
published top 11: ['DAT-01', 'DAT-02', 'DAT-05', 'DAT-06', 'INF-01', 'INF-02', 'INF-07', 'SVC-01', 'SVC-02', 'SVC-03', 'SVC-04']
published side of the top-11 cut reproduced in >=80% of draws: 14 ['GOV-01', 'GOV-02', 'GOV-03', 'SVC-02', 'SVC-03', 'SVC-04', 'DAT-01', 'DAT-02', 'DAT-04', 'DAT-06', 'INF-01', 'INF-02', 'INF-04', 'INF-06']
contradicted in >=80% of draws: 3 ['SVC-01', 'SVC-05', 'DAT-05']
uncertain: 4 ['DAT-03', 'INF-03', 'INF-05', 'INF-07']
mean share of assets on the same side of the top-11 cut as the published ranking: 0.78

## 2. Agreement of the published ratings with the LLM panel
consensus (mean of 7 models) vs published: tau=0.54 rho=0.78  top11 overlap=0.82
leave-one-out tau with the mean of the other raters: published 0.54; LLM models 0.69-0.87
per-dimension Spearman rho, published vs consensus: D 0.74, R 0.57, E 0.55, A 0.36, D2 0.16, S 0.75
Krippendorff alpha with published as 8th rater (model means): D 0.73, R 0.63, E 0.55, A 0.66, D2 0.54, S 0.84
dropping D2: tau(published, consensus) 0.54 -> 0.63
Kendall's W of the DREAD-S rankings: 7 models (mean of runs) 0.92 (p=8.3e-18); all 21 runs 0.87 (p=3.6e-65); 7 models plus published as 8th rater 0.88
Kendall's W per model over its 3 runs: A 0.95, B 0.94, C 0.95, D 0.95, E 0.95, F 0.89, G 0.89

## 3. Alternative aggregation schemes on the published ratings (vs Eq. 1)
  S only                       tau=0.81 rho=0.91 top7=0.86
  mean of five nu (no S)       tau=0.84 rho=0.95 top7=1.00
  L x I (L=R,E,D2; I=D,A,S)    tau=0.98 rho=1.00 top7=1.00
  mean five nu x S             tau=0.94 rho=0.99 top7=1.00
  max                          tau=0.82 rho=0.91 top7=0.86
  ordinal 5x5 matrix           tau=0.88 rho=0.95 top7=0.86
  z-score mean                 tau=0.92 rho=0.98 top7=1.00
  PC1                          tau=0.97 rho=1.00 top7=1.00
  PC1 explains 61% of variance

## 4. Propagation graph: structure vs score, and edge noise
Spearman rho of DREAD-S with downstream reach -0.17, with out-degree 0.39
baseline core 8, within two hops of a catastrophic asset: 16 of 16
  p=0.1 delete: core size mean 7.1, P(core>=6)=0.86, core members kept 0.89, SVC-03 and DAT-02 both in core 0.95, mean assets within 2 hops 14.7 of 16
  p=0.1 rewire: core size mean 9.2, P(core>=6)=0.97, core members kept 0.94, SVC-03 and DAT-02 both in core 0.98, mean assets within 2 hops 15.0 of 16
  p=0.2 delete: core size mean 6.1, P(core>=6)=0.65, core members kept 0.76, SVC-03 and DAT-02 both in core 0.84, mean assets within 2 hops 13.2 of 16
  p=0.2 rewire: core size mean 10.7, P(core>=6)=0.97, core members kept 0.90, SVC-03 and DAT-02 both in core 0.95, mean assets within 2 hops 14.2 of 16
  p=0.3 delete: core size mean 5.0, P(core>=6)=0.41, core members kept 0.62, SVC-03 and DAT-02 both in core 0.68, mean assets within 2 hops 11.6 of 16
  p=0.3 rewire: core size mean 11.8, P(core>=6)=0.97, core members kept 0.88, SVC-03 and DAT-02 both in core 0.92, mean assets within 2 hops 13.5 of 16
