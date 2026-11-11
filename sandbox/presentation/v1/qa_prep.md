# Questions to expect, and the honest answers (deck v1)

Numbers are the ones in `deck_v1.pptx`; all come from the repository result files. If a question is about a number that
is not here, look in `docs/research/11_thesis_reporting_notes.md` first.

## About the result

**Q1. The primary interval starts at +1.7. Is the 8.6-point gain real?**
By the rule fixed before training, yes: the whole 95 % interval is above zero and MAPPO + PAH was higher on 9 of 10 seed
indices. It is modest and uncertain, so we always quote the interval ("plausibly 2 to 15 points"). The lead is also
positive in all 31 test settings, but those use the same seeds, so they are not independent confirmations. A fresh-seed
replication is planned and has **not** been run.

**Q2. You changed PAH after seeing seed 42. Is that tuning on the test set?**
The change was made once, because of a mechanism: with policy-gradient training the gradient with respect to α is
A_mission − A_safety, and in danger A_safety is very negative, so α is pushed towards the mission (measured +0.200, the
maximum, at τ < 1). It was tested on synthetic data and a 300-episode smoke run, then frozen before the final runs.
Without seed 42 the main result is +7.9 [+0.7, +15.1]. On seed 42 itself the new PAH is slightly *below* the hand-coded
rule (79.5 vs 82.0 %), so the design was not shaped to win that seed.

**Q3. Is PAH just a learned version of the hand-coded τ-rule?**
Same three inputs, but PAH learns the risk from the safety cost that followed and reacts earlier (α 0.25 / 0.32 at
1 ≤ τ < 2 against 0.51 for the rule). At 8 drones it beats the rule by +11.3 [+4.6, +17.9]. At 5 drones the difference
is +2.0 [−2.6, +6.6], not settled, and we say so.

**Q4. Where does the large gap to DA-MAPPO (2D) come from?**
Mostly from the framework, not from PAH: conflict-graph observation +15.4, two value heads +30.0, PAH's α +8.6 (Stage 3,
controlled steps, roughly additive). We never present the 53.9-point gap as PAH's effect.

**Q5. Does PAH make drones keep more distance from each other?**
No. Loss of separation is similar (0.63 vs 0.55 for the fixed weight at 8 drones). PAH's advantage is in mission
success, which fits the diagnostics: most failures are obstacle collisions.

## About the comparison with the base papers

**Q6. Why are the base-paper numbers so much lower than in the papers?**
Different simulator (3D Gazebo vs 2D), 3 vs 8 drones, about 3 million steps with a curriculum vs 8,000 episodes, and our
shared settings were tuned on Plain MAPPO only. We compare the order of methods and the gain over MAPPO, not absolute
numbers. The base-paper methods keep one value head, as in the published methods.

**Q7. Were the baselines tuned fairly?**
They share exactly the same environment, budget, hyperparameters and seeds as our methods. Tuning was done once, on
Plain MAPPO, on separate seeds, and frozen. They were not tuned one by one; a reviewer can call that under-tuned, which
is why it is listed under limits.

**Q8. Why is RMAPPO missing?**
It did not learn under the shared settings: 0 % on 6 seeds at Stage 3; exploration noise collapsed; replay of the
stored sequences matches the stored values, so no implementation bug was found. A larger batch (its original setting)
was not tried. It is in the appendix with the reason rather than as a performance number. Re-running it takes about one
night.

**Q9. Why does everything get worse on static targets?**
We do not know. The models were trained only on moving targets and may rely on target motion; in the paper "dynamic"
means targets swap places, ours drift. Reported as an observation, not explained.

## About the synopsis

**Q10. The synopsis trains PAH through the policy gradient. Is the new PAH still PAH?**
Same name, same three inputs, same small network, same training loop; only its learning signal changed (regression on
the observed safety cost, no actor gradient). The policy-gradient version is kept as a finding with the mechanism.

**Q11. Where is the curriculum 3 → 5 → 8 drones?**
Not used in this study: each stage is trained from scratch with identical settings for every method. Stage 1
(3 drones, static targets) was run only in version 3. A curriculum could be added; it was not tested here.

**Q12. Why one factor at a time instead of 3 swarm sizes × 3 densities?**
It covers a wider range (density 10 to 50, swarm size 3 to 10) at lower cost; the price is that interactions between
the two are not measured.

**Q13. Why not PyBullet?**
The research question concerns α, not flight dynamics; a custom 2D environment allowed 186 trained models with 10 seeds
each on a laptop. No claims about 3D or hardware. *(Confirm that the supervisor agreed to this before presenting.)*

**Q14. The synopsis lists "target reassignments per episode" as a metric.**
Not measured yet; it is in the plan. The assignment itself is re-solved every step; the effect of re-assigning less often
is measured (every 50 steps: a small loss for every method).

## About method and rigour

**Q15. What does "success" mean?**
All drones reach their assigned targets, with no collision, within 500 steps (as in DA-MAPPO). A unit test checks that
the definition is the same for every assignment mode.

**Q16. Multiple comparisons?**
Only the Stage 3 comparison with Fixed-weight MAPPO was fixed in advance as primary. Everything else is labelled
secondary, and no correction was applied; this is stated on the slides.

**Q17. Is it reproducible?**
Ten seeds per method and stage, a fixed evaluation seed (7001), all 186 evaluations re-run with identical results,
tables and figures generated by script, settings recorded in each run's `config.json`.

**Q18. Why a mechanism check that found nothing?**
It was planned to show that PAH changes the actor's learning signal. It does not (92 to 99 % correlated with Plain MAPPO's
signal for every method), so we make no claim about *how* PAH helps. Reporting a negative check is better than leaving it
out.
