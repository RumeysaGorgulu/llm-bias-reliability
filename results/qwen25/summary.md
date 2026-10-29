# Results: qwen2.5:7b

## 1. Response quality
- 324 prompts, **100.0%** returned a usable number.

## 2. Validity check (does the score follow candidate quality?)
| profile   |   mean |   std |   count |
|:----------|-------:|------:|--------:|
| strong    |   8.35 |  0.48 |     108 |
| medium    |   7.56 |  0.5  |     108 |
| weak      |   5.34 |  0.69 |     108 |

- Ordering strong > medium > weak: **yes**.

## 3. Reliability
- **Repeat noise: average SD across repeats = 0.35 points** (the most direct measure of rating consistency).
- Test-retest ICC(1,1), all prompts: 0.90. Caution: this is inflated by the large score differences between strong, medium and weak profiles.
- Within-profile test-retest ICC(1,1) / repeat SD: strong = 0.36 / 0.26, medium = 0.29 / 0.30, weak = 0.39 / 0.48. Within a profile, prompts differ only by name and wording, so there is little true variance and low ICCs are expected.
- **Parallel-forms ICC(1,1): 0.88** (same content, different wording).
- Template means: T0 = 7.28, T1 = 7.32, T2 = 6.66
- Rough guide (Koo & Li, 2016): <0.50 poor, 0.50-0.75 moderate, 0.75-0.90 good, >0.90 excellent.

## 4. Group gaps (mean score minus group_A)
| profile   | group   |   gap_vs_group_A |   ci_low |   ci_high | ci_excludes_zero   |   p_permutation | analysis    |
|:----------|:--------|-----------------:|---------:|----------:|:-------------------|----------------:|:------------|
| strong    | group_B |            0.222 |    0.028 |     0.417 | True               |           0.2   | exploratory |
| strong    | group_C |            0.083 |   -0.056 |     0.222 | False              |           0.514 | exploratory |
| medium    | group_B |            0.222 |    0.056 |     0.389 | True               |           0.114 | exploratory |
| medium    | group_C |            0.056 |   -0.111 |     0.25  | False              |           0.857 | exploratory |
| weak      | group_B |            0     |   -0.333 |     0.306 | False              |           1     | exploratory |
| weak      | group_C |           -0.056 |   -0.361 |     0.222 | False              |           0.914 | exploratory |
| all       | group_B |            0.148 |    0.009 |     0.259 | True               |           0.114 | primary     |
| all       | group_C |            0.028 |   -0.111 |     0.157 | False              |           0.886 | primary     |

- Same profiles, only the name changes, so a reliable gap points to a name/group effect.
- `ci_low`/`ci_high`: 95% cluster-bootstrap CI (resampling names). With only 4 names per group the bootstrap can be too narrow, so the exact name-level permutation test (`p_permutation`, 70 splits) is the main test.
- Rows by profile are **exploratory** (6 extra tests per model); only the `all` rows are the primary comparison.

## Figures
![Group means](fig_group_means.png)

![Reliability](fig_reliability.png)
