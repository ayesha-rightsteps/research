# 08 — Literature Comparison Artifact (presentation record)

> **Accuracy note, 2026-10-05.** The artifact described below contains two statements that are now
> known to be misleading: (1) chart 2 and the finding callout set DA-MAPPO's 99-point swing (target
> removed from the observation) beside our α spread as if both were assignment ablations, and
> (2) the "0.2 points / 500× smaller" figure came from stochastic training logs; the deterministic
> 200-episode evaluation gives 1.5–2.0 points (about 10× smaller than the 20.5-point Hungarian
> effect). Corrected numbers and wording: `09_literature_comparison_report.md` and
> `code/notebooks/v3/results-table/`. The artifact could not be re-opened for editing from the
> session that found this, so the link above still shows the old version.

**Link:** https://claude.ai/artifact/GQTD3VBaacCbfNuvEh3cB6
**Title:** Multi-UAV Literature Comparison
**Built:** 2026-09-30, for Manish's supervisor meeting the same week.
**Source data:** identical to `docs/research/07_literature_comparison.md`
— every number below is copied from there, nothing computed separately
for the artifact. This file exists so the artifact's content survives even
if the link is ever lost, and so the thesis write-up has a plain-text
version of what the charts show.

---

## What's on the page

1. **Header** — project name, date, the three methods (B4/H/M), the two
   stages tested (5 drones, 8 drones).
2. **Headline numbers strip** — three big-number tiles: Stage 2 success
   (90.9%, inside DA-MAPPO's range), Stage 3 success (74.8%, below DA-
   MAPPO's hardest case), and DA-MAPPO's own ablation result (0%, assignment
   removed).
3. **Chart 1 — "All methods, one scale"**: horizontal bar chart, success
   rate sorted ascending, every method from DA-MAPPO's Table V ENV-1
   dynamic result (EGO-Planner v2 53%, NavRL 63%, IPPO 78%, MAPPO 83%,
   RMAPPO 85%, DA-MAPPO 99%) plus our Stage 3 (74.8%) and Stage 2 (91.0%),
   ours highlighted in a distinct color.
4. **Comparison table** — same DA-MAPPO numbers in table form, with a
   "Fit" column marking our Stage 2 as in-range and Stage 3 as below-range.
5. **Chart 2 — "Same axis, two very different effect sizes"**: two grouped
   bar-chart panels on a shared 0–100% y-axis. Left: DA-MAPPO with
   assignment (99%) vs without (0%) — a 99-point swing. Right: our three
   α-sources at Stage 2 — B4 (91.0%), H (90.8%), M (90.9%) — a 0.2-point
   spread. The visual point: the same 0–100 scale makes the size mismatch
   between the two effects immediate, without needing the reader to do the
   arithmetic themselves.
6. **The finding callout** — states the 99-point vs 0.2-point contrast in
   words, and the conclusion: the large effect in this problem family
   comes from the assignment mechanism, not from how α is chosen.
7. **IGAT-MARL section** — qualitative only (different metric family,
   explicitly not charted or number-matched), draws the one useful parallel:
   their action-distribution evidence of situational awareness is the same
   *kind* of evidence as our α-direction check, but in their case it also
   moved the outcome metrics; in ours it didn't.
8. **"What to say tomorrow"** — a three-paragraph script Manish can read
   or paraphrase directly to his supervisor.
9. **Caveat footer** — the environment-scale mismatch (their 30-50
   obstacles/N=3 vs our 5-10 obstacles/N=5-8), same wording as
   `07_literature_comparison.md`.

## Why a chart-based artifact, not just the markdown doc

Manish asked directly for this ("comparison dull nazar aaye kaise" — the
table-only version read as flat for an in-person presentation). The two
charts exist specifically to make the size of the assignment-ablation
effect vs the α-source effect immediately visible without the reader
mentally converting a table of percentages into a sense of scale.

## Basis for including DA-MAPPO specifically (asked and answered live,
2026-09-30, recorded here since the artifact doesn't spell this out)

Not just topical similarity — DA-MAPPO is methodologically closest on five
concrete points: same joint problem (assignment + collision avoidance),
same algorithm family (MAPPO), same assignment mechanism (Hungarian
algorithm, real-time), same primary metric (success/collision rate), and
it is literally the method our own experiment protocol's baseline **B2**
is modeled on (`docs/plans/02_experiment_protocol.md`'s method table).
IGAT-MARL is a design parallel; DA-MAPPO is one of our own planned
baselines.

## Update history

- 2026-09-30, v1: published with headline table only.
- 2026-09-30, v2: added the two SVG bar charts (per Manish's request).
