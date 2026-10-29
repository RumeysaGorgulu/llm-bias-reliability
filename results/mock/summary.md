# Results: mock

> **Mock run.** These numbers come from a simulated rater with a built-in effect, used only to test the pipeline. They are not findings about any LLM.

## 1. Response quality
- 324 prompts, **100.0%** returned a usable number.

## 2. Validity check (does the score follow candidate quality?)
| profile   |   mean |   std |   count |
|:----------|-------:|------:|--------:|
| strong    |   7.87 |  0.82 |     108 |
| medium    |   5.99 |  0.91 |     108 |
| weak      |   3.48 |  0.89 |     108 |

- Ordering strong > medium > weak: **yes**.

## 3. Reliability
- **Test-retest ICC(1,1): 0.81** (same prompt asked again; average SD across repeats = 0.77 points).
- **Parallel-forms ICC(1,1): 0.93** (same content, different wording).
- Template means: T0 = 5.75, T1 = 5.80, T2 = 5.80
- Rough guide (Koo & Li, 2016): <0.50 poor, 0.50-0.75 moderate, 0.75-0.90 good, >0.90 excellent.

## 4. Group gaps (mean score minus group_A, 95% cluster-bootstrap CI)
| profile   | group   |   gap_vs_group_A |   ci_low |   ci_high | ci_excludes_zero   |
|:----------|:--------|-----------------:|---------:|----------:|:-------------------|
| strong    | group_B |            -0.19 |    -0.42 |      0.03 | False              |
| strong    | group_C |            -0.03 |    -0.47 |      0.33 | False              |
| medium    | group_B |            -0.36 |    -0.58 |     -0.14 | True               |
| medium    | group_C |            -0.25 |    -0.53 |      0    | False              |
| weak      | group_B |            -0.33 |    -0.64 |     -0.06 | True               |
| weak      | group_C |             0.03 |    -0.28 |      0.39 | False              |
| all       | group_B |            -0.3  |    -0.5  |     -0.11 | True               |
| all       | group_C |            -0.08 |    -0.23 |      0.06 | False              |

- Same profiles, only the name changes, so a reliable gap points to a name/group effect.
- With 4 names per group, CIs are wide. Treat this as a pilot, not a conclusion.
- A gap smaller than the test-retest noise above is hard to interpret.

## Figures
![Group means](fig_group_means.png)

![Reliability](fig_reliability.png)
