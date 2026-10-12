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
| 1 | — | Depends on Phase 0. Candidates: environment changes (obstacle sensing, PAH input, conflict density) | to discuss |
| 2 | — | Base papers' methods in our environment (plain MAPPO, IPPO, DA-MAPPO-style, IGAT-style) | to discuss |
| 3 | — | Base papers' experiments (obstacle-density sweep, swarm-size sweep, static vs dynamic targets, their metrics) | to discuss |

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
