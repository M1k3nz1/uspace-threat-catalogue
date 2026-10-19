# Tables of Section 8.5 (computed)

## Table: alpha per dimension (columns: LLM A, LLM B, LLM C, LLM D, LLM E, All)
| Dimension | A | B | C | D | E | All |
|---|---|---|---|---|---|---|
| D | 0.88 | 0.89 | 0.86 | 0.91 | 0.94 | 0.82 |
| R | 0.89 | 0.81 | 0.79 | 0.89 | 0.92 | 0.81 |
| E | 0.90 | 0.82 | 0.84 | 0.93 | 0.93 | 0.77 |
| A | 0.88 | 0.75 | 0.80 | 0.91 | 0.92 | 0.79 |
| D2 | 0.91 | 0.84 | 0.92 | 0.91 | 0.89 | 0.82 |
| S | 0.91 | 0.93 | 0.93 | 0.91 | 0.94 | 0.86 |
| DREAD-S | 0.94 | 0.88 | 0.95 | 0.96 | 0.94 | 0.87 |

## Table: deviation from the published ratings

| Rater | Runs MAD | DREAD MAD | DREAD within 1 | S MAD | S within 1 | Mean DREAD-S |
|---|---|---|---|---|---|---|
| LLM A | 0.43 | 1.57 | 54% | 0.57 | 92% | 3.26 |
| LLM B | 0.70 | 1.57 | 55% | 0.65 | 92% | 3.28 |
| LLM C | 0.43 | 1.28 | 63% | 0.78 | 92% | 3.51 |
| LLM D | 0.47 | 1.53 | 55% | 0.65 | 98% | 3.33 |
| LLM E | 0.48 | 1.71 | 52% | 0.71 | 95% | 3.29 |
| All runs | 0.71 | 1.53 | 56% | 0.67 | 94% | 3.33 |
| Published | - | - | - | - | - | 3.71 |

## Table: ranking stability (range over the runs of each model)

| Rater | tau | Bands | Top-7 | INF-02 rank | Gov. | Runs with a Critical entry |
|---|---|---|---|---|---|---|
| LLM A | 0.52--0.61 | 10--11 | 0.57--0.71 | 4th--6th | 67%--100% | 0/3 |
| LLM B | 0.48--0.57 | 10--13 | 0.57--0.71 | 3rd--5th | 100% | 2/3 |
| LLM C | 0.46--0.50 | 7--8 | 0.57--0.71 | 5th--6th | 67% | 0/3 |
| LLM D | 0.40--0.60 | 12 | 0.57--0.71 | 2nd--3rd | 67%--100% | 3/3 |
| LLM E | 0.44--0.57 | 10--12 | 0.71 | 4th--6th | 67%--100% | 3/3 |
| Median of all 15 runs | 0.53 | 11 | 0.71 | 3rd | 100% | Critical |
