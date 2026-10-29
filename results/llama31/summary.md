# Results: llama3.1:8b

## 1. Response quality
- 324 prompts, **100.0%** returned a usable number.

## 2. Validity check (does the score follow candidate quality?)
| profile   |   mean |   std |   count |
|:----------|-------:|------:|--------:|
| strong    |   8.78 |  0.42 |     108 |
| medium    |   7.9  |  0.36 |     108 |
| weak      |   5.16 |  1.01 |     108 |

- Ordering strong > medium > weak: **yes**.

## 3. Reliability
- **Test-retest ICC(1,1): 0.91** (same prompt asked again; average SD across repeats = 0.35 points).
- **Parallel-forms ICC(1,1): 0.86** (same content, different wording).
- Template means: T0 = 6.98, T1 = 7.51, T2 = 7.34
- Rough guide (Koo & Li, 2016): <0.50 poor, 0.50-0.75 moderate, 0.75-0.90 good, >0.90 excellent.

## 4. Group gaps (mean score minus group_A, 95% cluster-bootstrap CI)
| profile   | group   |   gap_vs_group_A |   ci_low |   ci_high | ci_excludes_zero   |
|:----------|:--------|-----------------:|---------:|----------:|:-------------------|
| strong    | group_B |            -0.03 |    -0.14 |      0.11 | False              |
| strong    | group_C |            -0.22 |    -0.44 |      0    | False              |
| medium    | group_B |             0.03 |    -0.14 |      0.22 | False              |
| medium    | group_C |             0    |    -0.11 |      0.14 | False              |
| weak      | group_B |             0.08 |    -0.17 |      0.36 | False              |
| weak      | group_C |             0.14 |    -0.08 |      0.36 | False              |
| all       | group_B |             0.03 |    -0.07 |      0.12 | False              |
| all       | group_C |            -0.03 |    -0.15 |      0.07 | False              |

- Same profiles, only the name changes, so a reliable gap points to a name/group effect.
- With 4 names per group, CIs are wide. Treat this as a pilot, not a conclusion.
- A gap smaller than the test-retest noise above is hard to interpret.

## Figures
![Group means](fig_group_means.png)

![Reliability](fig_reliability.png)
