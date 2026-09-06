# docs/research/

Technical design worked out during implementation. These are **proposals to be
reviewed by the supervisor** before P0 sign-off, then the working spec.

| File | What it covers |
|------|----------------|
| `00_problem_formalization.md` | The Dec-POMDP: world, state, observation vector (exact fields + dims), action, transition, termination, the mission/safety reward terms with formulas, parameter table |
| `01_pah_design.md` | Priority Arbitration Head: fixed architecture, input normalization, the reward-hacking risk, 4 candidate training formulations, recommendation, thesis diagnostic figures |
| `02_assignment_and_conflict.md` | Hungarian cost matrix + thrashing + anti-thrashing options; conflict graph with the proper closest-point-of-approach math; how both feed the observation and PAH |
| `03_baseline_specs.md` | The 4 baselines (what's on/off); extracted DA-MAPPO and IGAT-MARL parameters; what we adopt vs change; why the cross-paper numbers are not directly comparable |
| `04_open_questions_for_supervisor.md` | Consolidated list needing written sign-off — synopsis deviations, PAH formulation, evaluation standards |

New notes (env design decisions, failure-case analysis, method breakdowns from other
papers) get added here as the work proceeds.

Grounding sources: `docs/paper/` (the synopsis) and the paper handbooks in `../../../bin/`
(DA-MAPPO = `91.`, IGAT-MARL = `9.`).
