# Review of deck v0 and what v1 changes

Written 2026-11-11 after reading v0 end to end, the result files it cites, and the approved synopsis
(`docs/paper/synopsis_text.txt`). Every point below was fixed in v1 unless it says **open**.

## 1. What was wrong or weak in v0

**Form**
1. **It was not a deck.** v0 was a markdown draft. v1 is a real `deck_v1.pptx` with native shapes, tables, pictures
   and speaker notes in the notes pane.
2. **Topic titles instead of findings.** "Main result: all methods, both stages" tells the audience nothing; v1 titles
   state the finding ("MAPPO + PAH ranks first of nine methods at both stages").
3. **Too much text.** v0 set itself a limit of ~25 words per slide and broke it on about half the slides. In v1 the
   figure is the slide and the text is a short call-out.
4. **Wrong cross-references.** v0 said "RMAPPO: 6, see slide 22" (slide 22 was the 31-settings slide, RMAPPO was slide 24) and called the
   deck "22 main slides" while having 26. v1 has no slide-number references in the slide text.
5. **Internal notes on a panel-facing slide.** Slide 8 carried "(per Ayesha; there is no written record in the repo —
   confirm before saying it on stage)". That belongs in the checklist, not on a slide. Moved to `README.md`.
6. **Q&A mixed into the deck file.** Moved to `qa_prep.md`.

**Content that was missing**
7. **No objectives / answer-first slide.** The synopsis has three objectives; v1 opens with them and the short answer
   to each ("What we set out to do").
8. **No picture of the problem or the system.** v1 has a real layout drawn from the environment code ("Two decisions must be made together"), a
   pipeline diagram ("One framework") and a PAH diagram ("PAH turns the situation into a weight"), all as editable native shapes.
9. **The version 3 story had no usable figure.** The old v3 figures use the nicknames B4 / H / M. v1 regenerates the
   chart with full names from the v3 result tables (`src/make_figures.py`, "Version 3" slide).
10. **No table of exact numbers.** The teacher asked for actual values, not ranges; v1 has a results table ("The numbers behind the chart")
    built by parsing `eval_summary.md`.
11. **The base-paper experiments were seven separate slides with no overview.** v1 adds one table ("We repeated the base papers' experiments") with
    what each experiment is, where it comes from and what we found.
12. **No slide on differences from the approved synopsis.** This is the biggest gap, and the one a committee member is
    most likely to raise. The synopsis says PAH is trained through the policy gradient (we now use regression on the
    safety cost), obstacle readings in four directions (now 24 LiDAR rays), a 3 → 5 → 8 curriculum (not used),
    a "target reassignments per episode" metric (not measured), a 3 × 3 evaluation grid (we sweep one factor at a time)
    and PyBullet (custom 2D). the v1 slide "Where we differ from the approved synopsis" lists them with the reason for each.

**Accuracy and honesty tightening**
13. "First of 9 methods" is now "first of nine methods" with RMAPPO named as the tenth, absent method.
14. "31 of 31 settings" now carries the caveat that the same ten seeds are used in every setting, so the results are
    not independent ("MAPPO + PAH stays ahead … in all 31 test settings").
15. The hand-written LiDAR rule that reached 82 % was run in the dense Stage 2 setting; v1 says so ("Redesign" slide).
16. "Removing the assignment cost 20.5 points" now says "version 3, one seed" on the slide.
17. The loss-of-separation result (PAH is **not** safer by this metric) gets its own slide with an orange call-out
    instead of a sentence inside another slide ("Near-misses" slide).
18. The v3 collision-type figure moved to the appendix; the 94 to 100 % finding is a number on the slide.
19. The planned fresh-seed replication is shown as **planned**, never as done ("Limits … and what we plan next").

## 2. New in v1

- 29 main slides + 14 appendix slides (43 in all), five sections (problem and method, how we got here, results,
  base-paper experiments, claims and next steps).
- A "short path" of 17 slides for a 15-minute slot (see `README.md`).
- Speaker notes for every slide, written for a presenter who is new to RL: what to say, what to point at, and the
  honest answer to the question that slide is most likely to raise.
- Everything is rebuilt from `src/` in one command; all numbers are checked against the result files.

## 3. Open items (not fixable in the deck)

- **Open:** no written record that the supervisor agreed to the four redesign changes and to the custom 2D environment
  instead of PyBullet. The redesign slide, the synopsis-differences slide and the panel questions are worded so they do not claim an agreement.
- **Open:** the fresh-seed replication (10 new seeds, no design change) has not been run; it is the one piece of work
  that would most strengthen the primary-result slide.
- **Open:** RMAPPO re-run with its original large-batch setting (about one night), or keep it in the appendix.
- **Open:** the deck was checked here with a text-fit calculation and a macOS QuickLook render, not in PowerPoint.
  Open it once, flip through, and check the speaker notes before presenting.
