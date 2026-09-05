# docs/paper/

Ayesha's **approved synopsis** — the source of truth for the implementation.

| File | What |
|------|------|
| `Synopsis_CIIT-SP25-RCS-009-ATD.docx` | Original approved synopsis |
| `synopsis_text.txt` | Plain-text extract (for reading / grep) |

## Key points from the synopsis

- **Framework:** unified MAPPO; both objectives (assignment + collision avoidance) in one joint observation
- **Novel:** Priority Arbitration Head — learned `α ∈ [0,1]`, replaces fixed reward coefficients
- **Environment:** 2D, 3–8 drones (synopsis says PyBullet, but a custom env is better for 2D — justify in `docs/research/`)
- **Curriculum:** 3 static → 5 moving+obstacles → 8 dynamic+dense → unseen swarm sizes
- **Closest prior work:** DA-MAPPO (Sheng et al. 2026, per-step Hungarian in the observation) + IGAT-MARL (Rezaee et al. 2026, sparse conflict graph)
- **Primary metric:** mission success rate (all drones reach targets + zero collisions + within time limit)
- **Baselines:** standard MAPPO · DA-MAPPO-2D · IGAT-MARL-style · fixed-weight MAPPO

The paper PDFs are in `../../../bin/` in numbered folders (DA-MAPPO = `91.`, IGAT-MARL = `9.`).
