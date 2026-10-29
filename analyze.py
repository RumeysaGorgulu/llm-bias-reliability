"""
Analyze LLM ratings as measurements: validity, reliability, and group bias.

Reads results/raw_responses.csv (from run_eval.py) and writes:
  results/summary.md         plain-language summary of every number
  results/group_gaps.csv     group differences with bootstrap 95% CIs
  results/fig_group_means.png
  results/fig_reliability.png
"""

import argparse
from itertools import combinations
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REFERENCE_GROUP = "group_A"


def icc_oneway(wide: pd.DataFrame) -> float:
    """ICC(1,1): one-way random effects, single rating.
    Rows = targets (things being rated), columns = repeated ratings."""
    x = wide.dropna().to_numpy(dtype=float)
    n, k = x.shape
    if n < 2 or k < 2:
        return float("nan")
    grand = x.mean()
    ms_between = k * ((x.mean(axis=1) - grand) ** 2).sum() / (n - 1)
    ms_within = ((x - x.mean(axis=1, keepdims=True)) ** 2).sum() / (n * (k - 1))
    denom = ms_between + (k - 1) * ms_within
    return float((ms_between - ms_within) / denom) if denom > 0 else float("nan")


def cluster_bootstrap_gap(df, group, ref, n_boot=2000, seed=0):
    """Difference in mean score (group - ref), resampling *names* within each group,
    because ratings of the same name are not independent."""
    rng = np.random.default_rng(seed)
    by_name = df.groupby("name")["score"].apply(np.array)
    g_names = df.loc[df["group"] == group, "name"].unique()
    r_names = df.loc[df["group"] == ref, "name"].unique()
    point = df.loc[df["group"] == group, "score"].mean() - df.loc[df["group"] == ref, "score"].mean()
    gaps = []
    for _ in range(n_boot):
        g = np.concatenate([by_name[n] for n in rng.choice(g_names, len(g_names))])
        r = np.concatenate([by_name[n] for n in rng.choice(r_names, len(r_names))])
        gaps.append(g.mean() - r.mean())
    lo, hi = np.percentile(gaps, [2.5, 97.5])
    return point, lo, hi


def permutation_test_gap(df, group, ref):
    """Exact permutation test for the group gap at the *name* level.

    Each name's mean score is one observation. All ways of splitting the names
    of the two groups into two sets of the original sizes are enumerated (70 for
    4 + 4 names), so the p-value is exact and does not rely on a bootstrap with
    very few clusters. With 4 + 4 names the smallest possible two-sided p is
    2/70 = 0.029.
    """
    name_means = df[df["group"].isin([group, ref])].groupby(["group", "name"])["score"].mean()
    g_vals = name_means.loc[group].to_numpy()
    r_vals = name_means.loc[ref].to_numpy()
    pooled = np.concatenate([g_vals, r_vals])
    observed = g_vals.mean() - r_vals.mean()
    idx = range(len(pooled))
    stats = []
    for g_idx in combinations(idx, len(g_vals)):
        mask = np.zeros(len(pooled), bool)
        mask[list(g_idx)] = True
        stats.append(pooled[mask].mean() - pooled[~mask].mean())
    stats = np.array(stats)
    p = float(np.mean(np.abs(stats) >= abs(observed) - 1e-12))
    return p, len(stats)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inp", default="results/raw_responses.csv")
    ap.add_argument("--outdir", default="results")
    args = ap.parse_args()

    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(args.inp)
    parse_rate = raw["score"].notna().mean()
    df = raw.dropna(subset=["score"]).copy()
    model = df["model"].iloc[0]
    lines = [f"# Results: {model}", ""]
    if model == "mock":
        lines += ["> **Mock run.** These numbers come from a simulated rater with a built-in "
                  "effect, used only to test the pipeline. They are not findings about any LLM.", ""]

    # --- Data quality of the instrument itself -----------------------------
    lines += ["## 1. Response quality",
              f"- {len(raw)} prompts, **{parse_rate:.1%}** returned a usable number.", ""]

    # --- Validity: does the score track candidate quality? ------------------
    by_profile = df.groupby("profile")["score"].agg(["mean", "std", "count"]).reindex(["strong", "medium", "weak"])
    ordered = by_profile["mean"].is_monotonic_decreasing
    lines += ["## 2. Validity check (does the score follow candidate quality?)",
              by_profile.round(2).to_markdown(),
              "",
              f"- Ordering strong > medium > weak: **{'yes' if ordered else 'NO, interpret all results with caution'}**.",
              ""]

    # --- Reliability --------------------------------------------------------
    # Test-retest: same name, profile and template; columns = repeats
    retest = df.pivot_table(index=["name", "profile", "template"], columns="repeat", values="score")
    icc_retest = icc_oneway(retest)
    within_sd = retest.std(axis=1).mean()
    # ICC across all prompts is driven largely by the spread between strong,
    # medium and weak profiles. Within-profile ICCs remove that spread.
    icc_within = {p: icc_oneway(retest.xs(p, level="profile"))
                  for p in ["strong", "medium", "weak"]}
    sd_within = {p: retest.xs(p, level="profile").std(axis=1).mean()
                 for p in ["strong", "medium", "weak"]}

    # Parallel forms: average repeats first, then templates as columns
    forms = df.groupby(["name", "profile", "template"])["score"].mean().unstack("template")
    icc_forms = icc_oneway(forms)
    form_means = df.groupby("template")["score"].mean()

    lines += ["## 3. Reliability",
              f"- **Repeat noise: average SD across repeats = {within_sd:.2f} points** "
              "(the most direct measure of rating consistency).",
              f"- Test-retest ICC(1,1), all prompts: {icc_retest:.2f}. Caution: this is inflated by "
              "the large score differences between strong, medium and weak profiles.",
              "- Within-profile test-retest ICC(1,1) / repeat SD: " + ", ".join(
                  f"{p} = {icc_within[p]:.2f} / {sd_within[p]:.2f}" for p in icc_within)
              + ". Within a profile, prompts differ only by name and wording, so there is little true "
              "variance and low ICCs are expected.",
              f"- **Parallel-forms ICC(1,1): {icc_forms:.2f}** (same content, different wording).",
              f"- Template means: " + ", ".join(f"T{t} = {m:.2f}" for t, m in form_means.items()),
              "- Rough guide (Koo & Li, 2016): <0.50 poor, 0.50-0.75 moderate, 0.75-0.90 good, >0.90 excellent.",
              ""]

    # --- Bias ---------------------------------------------------------------
    gap_rows = []
    for profile in ["strong", "medium", "weak", "all"]:
        sub = df if profile == "all" else df[df["profile"] == profile]
        for group in sorted(df["group"].unique()):
            if group == REFERENCE_GROUP:
                continue
            point, lo, hi = cluster_bootstrap_gap(sub, group, REFERENCE_GROUP)
            p_perm, n_perm = permutation_test_gap(sub, group, REFERENCE_GROUP)
            gap_rows.append({"profile": profile, "group": group, "gap_vs_" + REFERENCE_GROUP: point,
                             "ci_low": lo, "ci_high": hi,
                             "ci_excludes_zero": bool(lo > 0 or hi < 0),
                             "p_permutation": p_perm,
                             "analysis": "primary" if profile == "all" else "exploratory"})
    gaps = pd.DataFrame(gap_rows)
    gaps.round(3).to_csv(out / "group_gaps.csv", index=False)

    lines += [f"## 4. Group gaps (mean score minus {REFERENCE_GROUP})",
              gaps.round(3).to_markdown(index=False),
              "",
              "- Same profiles, only the name changes, so a reliable gap points to a name/group effect.",
              "- `ci_low`/`ci_high`: 95% cluster-bootstrap CI (resampling names). With only 4 names per "
              "group the bootstrap can be too narrow, so the exact name-level permutation test "
              f"(`p_permutation`, {n_perm} splits) is the main test.",
              "- Rows by profile are **exploratory** (6 extra tests per model); only the `all` rows are "
              "the primary comparison.",
              ""]

    # --- Figures ------------------------------------------------------------
    groups = sorted(df["group"].unique())
    profiles = ["strong", "medium", "weak"]
    fig, ax = plt.subplots(figsize=(7, 4))
    width = 0.8 / len(groups)
    colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]
    for i, g in enumerate(groups):
        stats = df[df["group"] == g].groupby("profile")["score"].agg(["mean", "std", "count"]).reindex(profiles)
        se = stats["std"] / np.sqrt(stats["count"])
        x = np.arange(len(profiles)) + (i - (len(groups) - 1) / 2) * width
        ax.bar(x, stats["mean"], width, yerr=1.96 * se, capsize=3, label=g, color=colors[i % 4])
    ax.set_xticks(np.arange(len(profiles)), profiles)
    ax.set_ylabel("Mean suitability score (1-10)")
    ax.set_ylim(0, 10.5)
    ax.set_title(f"Ratings by candidate profile and name group ({model})")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(out / "fig_group_means.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5, 3.2))
    vals = [icc_retest, icc_forms]
    ax.barh(["Test-retest", "Parallel forms"], vals, color=["#4C72B0", "#DD8452"])
    for x0, label in [(0.5, "moderate"), (0.75, "good"), (0.9, "excellent")]:
        ax.axvline(x0, color="grey", lw=0.8, ls="--")
        ax.text(x0, 1.45, label, fontsize=8, ha="center", color="grey")
    for i, v in enumerate(vals):
        ax.text(v + 0.01, i, f"{v:.2f}", va="center")
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("ICC(1,1)")
    ax.set_title("How consistent is the model as a rater?")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(out / "fig_reliability.png", dpi=150)
    plt.close(fig)

    lines += ["## Figures", "![Group means](fig_group_means.png)", "", "![Reliability](fig_reliability.png)", ""]
    (out / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
