# v4

Started 2026-10-12. v4 exists because the v3 results raised questions that v3's setup cannot answer
(see `sessions/2026-10-12.md`, Sections 9–11): our numbers cannot be fairly compared with the base papers,
the base papers' experiments were never repeated in our environment, and PAH may have had too little to
arbitrate.

## Rule for v4: build only what the current step needs

Phases after the current one are **listed, not decided**. Their folders are created when the work starts,
not before. Each phase is decided from the previous phase's results by Ayesha, Manish and the supervisor.

| Phase | Folder | What | Status |
|---|---|---|---|
| 0 | `00-diagnostics/` | Read-only checks on the v3 models: collision kinds, how often safety matters, how much α moves, IGAT-MARL metrics | **done** — results in its README |
| 1a | `01-plain-mappo-check/` | Train Plain MAPPO (no mission/safety split) vs Fixed-weight MAPPO on the laptop, Stage 2, 5 seeds — tests Phase 0's explanation of the tie | **done** — inconclusive by the pre-set rule (Plain MAPPO 89.9 ± 1.4 vs Fixed-weight 88.2 ± 2.2, CI [−1.1, +4.5]); the mixing gives no measurable benefit; laptop reproduces Kaggle |
| 1b | `02-redesign/` | Environment / PAH redesign: separate mission and safety value heads, obstacle danger as PAH input, LiDAR-like sensing, sized and denser obstacles | **done** — 100 runs; MAPPO + PAH − Fixed-weight MAPPO at Stage 3 +8.6 [+1.7, +15.4] (`02-redesign/README.md`) |
| 2 | `03-base-paper-baselines/` | **Base papers' methods in the Phase 1b environment** (same environment, protocol, 10 seeds). From DA-MAPPO: IPPO (independent critics), MAPPO without assignment in the observation, a DA-MAPPO-style method (Hungarian assignment in the observation, no conflict-graph features); RMAPPO optional. From IGAT-MARL: an IGAT-style method (conflict graph + graph-attention encoder, no per-step Hungarian), MAPPO-based. NavRL and EGO-Planner v2 are not reproduced (not MARL; planner software) — stated in the thesis | **done** in `03-base-paper-baselines/` — 80 runs + RMAPPO (6 seeds, did not learn); MAPPO + PAH above every base-paper method (`REPORT.md`) |
| 3 | `04-base-paper-experiments/` | **Base papers' experiments**: obstacle-density sweep (e.g. 20 / 30 / 40 / 50 discs, like DA-MAPPO's ENV-1–3); static vs moving targets; assignment every step vs every 50 steps (DA-MAPPO ablation); swarm-size sweep 3 → 10 drones (IGAT-MARL); IGAT-MARL's metrics (loss-of-separation, active edges); learning curves with confidence bands; sensor-noise robustness; computation time vs number of drones | **plan written** (`04-base-paper-experiments/PLAN.md`), waiting for Manish |
| 4 | — | **Results package and writing**: tables and figures in the base papers' format, the comparison chapter (now same-environment, so fair), the story of v3 → v4 (what was found and why the design changed), then the finished work to the supervisor | planned (after 3) |

**Timeline (revised 2026-10-12 — training on the laptop takes hours, not days; time now goes to code,
tests, review and debugging):** Phase 1b 2–4 days (code + tests 1–1.5, sanity training and possible tuning
0.5–1.5, main training one night, evaluation half a day) · Phase 2 ~2 days (the graph-attention encoder is the
biggest piece) · Phase 3 1–2 days (mostly evaluation-only: density sweep, static targets, 3→10 drones work on
already-trained policies because each drone sees a fixed 4 neighbours) · Phase 4 4–5 days (mostly writing) →
**about 1.5–2 weeks**. Training of one phase runs overnight while the next phase's code is written. Biggest
risk: tuning in Phase 1b Step 3 (done on Plain MAPPO only, then applied to every method).

## Folder and naming rules (lessons from v3)

v3 ended up with `stage2-a`, `stage2-b`, `stage2-pah-v0…v3`, `output`, `output-seed42`, `seed-43/output`
and the same environment pasted into many notebooks. In v4:

1. **One copy of shared code**, in `common/`. Notebooks import it; they do not paste it.
   - `common/v3_env.py` — frozen copy of the v3 environment + networks, only for evaluating v3 models.
     If v4 changes the environment, that is a new file; this one is never edited.
   - `common/v3_registry.py` — the paths of all 18 trained v3 models, in one place.
2. **Every phase folder** = `NN-short-name/` with a `README.md` (question, method, results, caveats),
   the notebook, and `output/`.
3. **Every notebook starts with a gate** that checks it reproduces something already known before
   producing anything new.
4. **One evaluation protocol from day one:** deterministic policy, 200 episodes, an evaluation seed disjoint
   from training seeds; collision kind, loss-of-separation and active edges are logged together with
   success / collision / timeout / T_ave / L_ave.
5. Nothing in `v3/` is written by v4.
