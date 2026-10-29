# Results: mistral-capped

## 1. Response quality
- 324 prompts, **100.0%** returned a usable number.

## 2. Validity check (does the score follow candidate quality?)
| profile   |   mean |   std |   count |
|:----------|-------:|------:|--------:|
| strong    |   9.46 |  0.43 |     108 |
| medium    |   8.31 |  0.27 |     108 |
| weak      |   4.35 |  1.02 |     108 |

- Ordering strong > medium > weak: **yes**.

## 3. Reliability
- **Repeat noise: average SD across repeats = 0.20 points** (the most direct measure of rating consistency).
- Test-retest ICC(1,1), all prompts: 0.98. Caution: this is inflated by the large score differences between strong, medium and weak profiles.
- Within-profile test-retest ICC(1,1) / repeat SD: strong = 0.85 / 0.08, medium = 0.50 / 0.10, weak = 0.73 / 0.43. Within a profile, prompts differ only by name and wording, so there is little true variance and low ICCs are expected.
- **Parallel-forms ICC(1,1): 0.91** (same content, different wording).
- Template means: T0 = 7.56, T1 = 7.48, T2 = 7.07
- Rough guide (Koo & Li, 2016): <0.50 poor, 0.50-0.75 moderate, 0.75-0.90 good, >0.90 excellent.

## 4. Group gaps (mean score minus group_A)
| profile   | group   |   gap_vs_group_A |   ci_low |   ci_high | ci_excludes_zero   |   p_permutation | analysis    |
|:----------|:--------|-----------------:|---------:|----------:|:-------------------|----------------:|:------------|
| strong    | group_B |            0.056 |    0     |     0.111 | False              |           0.314 | exploratory |
| strong    | group_C |            0.042 |   -0.042 |     0.111 | False              |           0.571 | exploratory |
| medium    | group_B |            0.069 |   -0.014 |     0.153 | False              |           0.343 | exploratory |
| medium    | group_C |            0.014 |   -0.069 |     0.083 | False              |           1     | exploratory |
| weak      | group_B |            0.431 |    0.111 |     0.709 | True               |           0.114 | exploratory |
| weak      | group_C |            0.153 |   -0.056 |     0.361 | False              |           0.343 | exploratory |
| all       | group_B |            0.185 |    0.069 |     0.296 | True               |           0.057 | primary     |
| all       | group_C |            0.069 |   -0.032 |     0.167 | False              |           0.371 | primary     |

- Same profiles, only the name changes, so a reliable gap points to a name/group effect.
- `ci_low`/`ci_high`: 95% cluster-bootstrap CI (resampling names). With only 4 names per group the bootstrap can be too narrow, so the exact name-level permutation test (`p_permutation`, 70 splits) is the main test.
- Rows by profile are **exploratory** (6 extra tests per model); only the `all` rows are the primary comparison.

## Figures
![Group means](fig_group_means.png)

![Reliability](fig_reliability.png)
