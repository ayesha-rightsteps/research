# presentation / v1

`deck_v1.pptx` is the real deck (43 slides: 29 main + 14 appendix, speaker notes on every slide).
It replaces the markdown draft in `../v0/`. What was wrong with v0 and what changed: `review_of_v0.md`.

| File | What it is |
|---|---|
| `deck_v1.pptx` | The deck. Native shapes, tables and pictures; Arial; 16:9; speaker notes in the notes pane |
| `deck_v1.md` | Every slide's text and speaker notes as markdown (generated, do not edit by hand) |
| `qa_prep.md` | 18 likely questions with honest answers |
| `review_of_v0.md` | Deep review of v0 and the list of changes |
| `images/` | Every picture the deck uses (copied from the repo, so this folder is self-contained) |
| `src/` | The code that builds everything (below) |

## Before presenting (checklist)

1. **Open `deck_v1.pptx` in PowerPoint (or Keynote) once and flip through it.** It was checked here with a text-fit
   calculation and a drawing of every slide from the file's coordinates, but not in PowerPoint itself.
2. **Do not say the fresh-seed replication is done.** It is planned (10 new seeds, MAPPO + PAH and Fixed-weight MAPPO, no
   design change, reported separately); it has not been run. Running it would narrow the main interval.
3. **Confirm with the supervisor** that the redesign (four changes, new PAH learning signal) and the custom 2D environment
   instead of PyBullet were agreed. There is no written record in the repository, so the slides do not claim it.
4. Add the date to the title slide if the venue needs one.
5. RMAPPO: decide whether the appendix is enough or it should be re-run with its original large-batch setting.

## Timing

29 main slides is about 28 to 30 minutes. For 15 minutes use slides 1, 2, 3, 5, 6, 7, 9, 11, 12, 14, 15, 18, 24, 25,
26, 27, 28 and keep 29 for the questions.

## Rebuild

The numbers are read from the repository result files and the build stops if one is missing or a claim no longer holds
(for example "MAPPO + PAH is first at every density").

```
python3 -m venv venv && venv/bin/pip install numpy matplotlib scipy pillow python-pptx lxml torch
venv/bin/python src/make_figures.py      # the two new figures: env_illustration.png, v3_alpha_tie.png
venv/bin/python src/build_deck.py        # deck_v1.pptx + deck_v1.md, prints text-fit warnings
venv/bin/python src/preview.py out_dir   # optional: PNG of every slide drawn from the file (layout check)
```

`src/deck_lib.py` holds the layout helpers, `src/build_deck.py` the content of every slide and note.
