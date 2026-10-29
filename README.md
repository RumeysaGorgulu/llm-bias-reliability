# Is an LLM a Reliable and Fair Rater? A Psychometric Audit

**Question:** When an LLM rates job candidates, does it behave like a good measurement instrument?

I come from educational measurement, where a test is only useful if it is **valid**, **reliable** and **free of bias against groups**. This project applies those same three checks to an LLM used as a rater:

| Measurement concept | What it means here | How it is tested |
|---|---|---|
| **Validity** | Scores track real candidate quality | Strong > medium > weak profiles? |
| **Test-retest reliability** | Same prompt, same score | Ask each prompt *k* times; repeat SD and ICC(1,1) |
| **Parallel-forms reliability** | Same content, reworded prompt, same score | 3 prompt templates, ICC(1,1) |
| **Bias (DIF-style)** | Only the name changes, score should not | Group gaps; exact name-level permutation test + cluster-bootstrap CIs |

## Design

- **3 candidate profiles** (strong, medium, weak), identical across groups
- **3 name groups × 4 names each**; the name is the only group signal (audit-study design, following Bertrand & Mullainathan, 2004)
  - Group A: White-American-associated names (Emily, Anne, Greg, Brad)
  - Group B: Black-American-associated names (Lakisha, Tamika, Jamal, Darnell)
  - Group C: Turkish names (Mehmet, Ayse, Ahmet, Zeynep)
- **3 prompt templates** (parallel forms)
- **3 repeats** per prompt at temperature 0.7 (test-retest)
- = **324 prompts** per model, run locally with [Ollama](https://ollama.com)

Ratings of the same name are not independent, so inference is at the **name** level: an exact permutation test over all 70 ways of splitting the 8 names of two groups (main test), plus cluster-bootstrap CIs that resample names.

## Quick start

```bash
pip install -r requirements.txt

# 1. Test the pipeline with a simulated rater (no LLM needed)
python run_eval.py --backend mock
python analyze.py

# 2. Run a real model
ollama pull llama3.1:8b
python run_eval.py --backend ollama --model llama3.1:8b --out results/llama31/raw_responses.csv
python analyze.py --inp results/llama31/raw_responses.csv --outdir results/llama31
```

Outputs: `summary.md` (all numbers in plain language), `group_gaps.csv`, and two figures.

## Pipeline check (simulated rater, not a real finding)

The mock rater has a known, built-in effect: group B scores 0.4 points lower. The analysis recovers the direction and size (overall gap −0.30, 95% bootstrap CI [−0.50, −0.11]) and finds no gap for group C. The exact permutation test gives p = 0.06 for this *true* effect. With only 4 names per group, the design cannot reliably confirm a gap of this size, which is the main reason to scale up the name lists.

Mock outputs are in `results/mock/`.

## Results (3 open models, 324 prompts each, 100% parsed)

Run locally with Ollama, temperature 0.7. Full outputs per model are in `results/llama31/`, `results/qwen25/` and `results/mistral7b/`.

| | Llama 3.1 8B | Qwen 2.5 7B | Mistral 7B* |
|---|---|---|---|
| Mean score: strong / medium / weak | 8.78 / 7.90 / 5.16 | 8.35 / 7.56 / 5.34 | 9.46 / 8.31 / 4.35 |
| Repeat noise (avg SD across repeats) | 0.35 | 0.35 | **0.20** |
| Test-retest ICC(1,1), all prompts† | 0.91 | 0.90 | 0.98 |
| Parallel-forms ICC(1,1) | 0.86 | 0.88 | 0.91 |
| Largest template gap | 0.53 | 0.66 | 0.49 |
| Gap, group B vs A [95% bootstrap CI] | 0.03 [−0.07, 0.12] | 0.15 [0.01, 0.26] | 0.19 [0.07, 0.30] |
| Permutation p, group B vs A | 0.77 | 0.11 | 0.06 |
| Gap, group C vs A [95% bootstrap CI] | −0.03 [−0.15, 0.07] | 0.03 [−0.11, 0.16] | 0.07 [−0.03, 0.17] |
| Permutation p, group C vs A | 0.80 | 0.89 | 0.37 |

\*Mistral was run with output capped at 100 tokens (`num_predict 100`, saved as `mistral-capped`) because uncapped runs timed out. Unlike the other two models, it often added explanations and gave half-point scores, so its run conditions are not identical.

†ICC across all prompts is inflated by the large score differences between strong, medium and weak profiles; repeat SD is the more direct consistency measure. Within-profile ICCs are in each model's `summary.md`.

![Mistral group means](results/mistral7b/fig_group_means.png)

*Mistral 7B: mean score by name group and profile. The group B gap is largest for weak profiles (exploratory).*

### Key findings

- **Validity:** all 3 models rank strong > medium > weak, but all are lenient (weak profiles still get about 4–5 out of 10).
- **Consistency:** repeat noise is small (SD 0.20–0.35 points on a 1–10 scale).
- **Wording matters more than names:** changing the prompt template shifts mean scores by 0.5–0.7 points; name-group gaps are at most 0.19.
- **Consistent is not the same as fair:** Mistral is the most consistent rater (lowest repeat noise, SD 0.20) yet shows the largest name gap (0.19 points favoring group B; bootstrap CI excludes zero, exact permutation p = 0.06). The pattern parallels the "consistency–bias paradox" reported for position bias (Norman et al., 2026). With 4 names per group this is suggestive, not conclusive.
- **Model-specific:** Qwen and Mistral show small gaps favoring group B (not significant by the permutation test); Llama shows none.
- **Exploratory:** for Mistral the group B gap is concentrated in weak profiles (0.43); this is one of six subgroup tests and needs confirmation.

## Limitations

- Small pilot: with 4 names per group the permutation test has little power (smallest possible p = 0.029), and the bootstrap with 4 clusters can understate uncertainty.
- Names signal more than one thing (perceived race, gender, nationality), so a gap shows *that* the model reacts to names, not *why*.
- Parallel-forms ICC averages repeats first, so it is not directly comparable with test-retest ICC. Both ICCs mostly reflect profile spread.
- A single rating task (hiring) may not generalize to other tasks.
- Constructed profiles (audit-study design), not real applications.
- Bias estimates were unstable across runs: an earlier Llama 3.1 run on another machine showed a small significant group B gap (0.11); this run did not.
- Results apply to these model versions and prompts only.

## Next steps

- Repeat each model run several times to measure run-to-run stability of bias estimates
- More names per group (20+), which gives the permutation test real power, and separate gender from group
- Model the scores with a mixed-effects model (name and template as random effects)

## Related work

- Lin et al. (2025). *FairCode: Evaluating Social Bias of LLMs in Code Generation.* arXiv. Inspired the idea of auditing LLM outputs for group bias; this project uses its own design and a rating task, not code generation.
- Armstrong, L., et al. (2024). The Silicon Ceiling: Auditing GPT's race and gender biases in hiring. arXiv:2405.04412.
- Norman, J. D., Rivera, M. U., & Hughes, D. A. (2026). Reliability without Validity: A systematic, large-scale evaluation of LLM-as-a-Judge models across agreement, consistency, and bias. arXiv:2606.19544.
- Bertrand, M., & Mullainathan, S. (2004). Are Emily and Greg more employable than Lakisha and Jamal? *American Economic Review.*
- Koo, T. K., & Li, M. Y. (2016). A guideline of selecting and reporting intraclass correlation coefficients. *Journal of Chiropractic Medicine.*
