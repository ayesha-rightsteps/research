"""
Priority Arbitration Head (PAH) — the novel contribution of this thesis.

At every decision step, PAH takes three safety-relevant scalars for each drone
and outputs a dynamic weight α ∈ [0.1, 0.9], used inside MAPPO's actor loss as:

    w_adv = α · A_mission + (1 − α) · A_safety      (Option B, see below)

α → 1  means "follow the mission advantage" (push toward reaching the target)
α → 0  means "follow the safety advantage" (push toward avoiding collisions)

A fixed baseline uses α = constant (e.g. 0.5) always.  The thesis claim is
that a *learned*, *state-dependent* α produces better coordination.  PAH is
the mechanism that makes α state-dependent.

Implementation is Option B from docs/research/01_pah_design.md Section 9
(decided 2026-09-14, after Option A's naive form and an Option C detour both
turned out unsound — see that section and sessions/2026-09-14.md Part 2-3 for
why):
  - α weights two separate GAE advantage streams (A_mission, A_safety), not
    the raw scalar reward — this is what actually removes the reward-hacking
    path, because α now reweights *which direction the policy improves in*,
    not a return the agent can inflate by moving α
  - the advantage streams each have their OWN critic baseline (critic_m,
    critic_s in mappo.py) as of the 2026-09-17 two-head critic escalation —
    see docs/research/01_pah_design.md Section 9.2's closing note and
    sessions/2026-09-17.md Sections 13-15. They originally shared one critic
    ("Option B lite"), which matched the synopsis's "no extra critic params"
    more closely, but across 5 seeds that shared baseline let A_safety read
    as unreliable enough, in some seeds, for the actor loss to push α the
    wrong way near danger 34% of the time even with the prior below fighting
    it — so the second critic head was added despite the synopsis deviation
    (flagged to the supervisor per docs/research/04_open_questions_for_
    supervisor.md Q5)
  - α prior (compute_prior_loss below) pulls toward a τ-informed,
    danger-weighted target — NOT a flat 0.5 anymore. See that method's
    docstring for the full history (flat 0.5 → τ-informed → danger-weighted,
    2026-09-16/17) of why each version changed.
  - α clipped to [α_min, α_max] so neither objective is ever fully ignored
  - Inputs normalized before entering the MLP (critical for conditioning)
  - Full diagnostics built in (thesis figures come from here)
  - `code/algorithms/mappo.py::MAPPO.update()` (and its `_update_pah` helper)
    is where the actual α-weighted loss and two-head GAE computation live —
    this file only defines PAH itself (the network) and the input
    normalizer/wrapper around it.

The classes below (PAHNormalizer, PriorityArbitrationHead, PAHWrapper) are
unchanged by the two-head critic escalation — only how mappo.py's critic(s)
and GAE computation work around them changed.

Reference: docs/research/01_pah_design.md
"""

from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
from dataclasses import dataclass


# ══════════════════════════════════════════════════════════════════════
# 1. INPUT NORMALIZER
# ══════════════════════════════════════════════════════════════════════

@dataclass
class PAHNormalizer:
    """
    Scales the three raw PAH inputs to roughly [0, 1] before they enter the MLP.

    Without normalization, τ_collision (0–3 s) and d_target (0–140 units) are on
    wildly different scales — the MLP effectively ignores the small-scale input.

    Parameters
    ----------
    horizon     : look-ahead horizon H (same as ConflictGraph)
    d_max       : world diagonal ≈ sqrt(2) * world_size
    n_drones    : total drones (so n_conflict is divided by n_drones − 1)
    """
    horizon:  float = 3.0
    d_max:    float = 707.1   # sqrt(2) * 500  (500 m × 500 m world diagonal)
    n_drones: int   = 3

    def normalize(self, tau: torch.Tensor,
                  d_target: torch.Tensor,
                  n_conflict: torch.Tensor) -> torch.Tensor:
        """
        Parameters — all shape (B,) or scalar tensors on the same device.
        Returns shape (B, 3), normalized to [0, 1].

        Conventions:
            tau_norm    = 1 → safe (no imminent collision)
                        = 0 → collision happening right now
            d_norm      = 1 → target is at max distance
                        = 0 → already at target
            n_norm      = 1 → all other drones are conflict neighbors
                        = 0 → no conflicts
        """
        tau_norm = tau.clamp(0.0, self.horizon) / self.horizon
        d_norm   = d_target.clamp(0.0, self.d_max) / self.d_max
        denom    = max(self.n_drones - 1, 1)
        n_norm   = n_conflict.clamp(0.0, denom) / denom

        return torch.stack([tau_norm, d_norm, n_norm], dim=-1)   # (B, 3)


# ══════════════════════════════════════════════════════════════════════
# 2. PAH NETWORK
# ══════════════════════════════════════════════════════════════════════

class PriorityArbitrationHead(nn.Module):
    """
    A lightweight two-layer MLP that maps normalized (τ, d, n) → α.

    Architecture (from docs/research/01_pah_design.md §2):
        Linear(3 → hidden) → ReLU → Linear(hidden → 1) → Sigmoid

    Output is then clipped to [α_min, α_max] so neither objective is
    ever fully silenced during training.

    Parameter count: 3·hidden + hidden + hidden + 1 ≈ 130 for hidden=32.
    Consistent with "lightweight" in the synopsis.

    Parameters
    ----------
    hidden_dim : width of the single hidden layer
    alpha_min  : lower clip for α (default 0.1 — always some safety weight)
    alpha_max  : upper clip for α (default 0.9 — always some mission weight)
    prior_coef : coefficient for the τ-informed, danger-weighted α regularizer
                 in the loss (set to 0 to disable; see compute_prior_loss).
                 0.01 (flat-0.5 prior) -> 0.05 (τ-target, 2026-09-16, tested,
                 NOT enough — see compute_prior_loss docstring §2) -> 0.15
                 (danger-weighted, 2026-09-17). Each change is a reasoned
                 starting point, not a swept value — re-check against the
                 next verification run before trusting it.
    """

    def __init__(
        self,
        hidden_dim: int   = 32,
        alpha_min:  float = 0.1,
        alpha_max:  float = 0.9,
        prior_coef: float = 0.15,
    ):
        super().__init__()

        self.alpha_min  = alpha_min
        self.alpha_max  = alpha_max
        self.prior_coef = prior_coef

        self.net = nn.Sequential(
            nn.Linear(3, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

        self._init_weights()

    def _init_weights(self):
        """
        Initialise the final bias so that sigmoid(0) = 0.5 at the start —
        PAH begins neutral and moves from there based on experience.
        """
        nn.init.zeros_(self.net[-1].bias)
        nn.init.xavier_uniform_(self.net[-1].weight, gain=0.1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Parameters
        ----------
        x : (B, 3)  — already normalized inputs [τ_norm, d_norm, n_norm]

        Returns
        -------
        alpha : (B, 1) in [alpha_min, alpha_max]
        """
        raw   = self.net(x)                          # (B, 1)
        alpha = torch.sigmoid(raw)                   # (B, 1) in (0, 1)
        alpha = self.alpha_min + (self.alpha_max - self.alpha_min) * alpha
        return alpha                                  # (B, 1)

    def compute_prior_loss(self, alpha: torch.Tensor, tau_norm: torch.Tensor) -> torch.Tensor:
        """
        Regularizer: pull α toward a τ-informed target, weighted toward
        danger-close samples — not a flat 0.5, and not a uniform-weight
        τ-target either (see the 2026-09-17 update below).

        History (see docs/research/01_pah_design.md §9.2/§9.3,
        sessions/2026-09-16.md Sections 14-16):

        1. Originally (before 2026-09-16) this pulled α toward a flat 0.5.
           That left the advantage-mixing actor loss in mappo.py as the only
           signal shaping α's direction near danger, and that loss can push α
           the WRONG way there — A_safety is routinely more negative than
           A_mission in a near-collision state (the collision penalty is the
           sharpest negative signal in the reward), so minimizing the loss
           pushed α UP (mission-focus) exactly when it should drop.

        2. First fix (2026-09-16): switched the target from flat 0.5 to a
           τ-informed one (see alpha_target below) and raised prior_coef
           0.01 -> 0.05. Tested on a full 8000-episode Kaggle run — did NOT
           work: 11/19 danger-close eval samples were still wrong (vs 10/17
           before, statistically the same rate), still saturating at
           alpha_max. Root cause found by comparing logged loss magnitudes:
           pah_loss was consistently ~10-20x smaller than actor_loss. Danger-
           close states are also a small fraction of any training batch
           (only 19/76 eval checkpoints had ANY valid danger-close sample at
           all), so an unweighted mean((α − α_target)²) over the whole batch
           lets the rare danger samples get washed out by the much larger
           volume of safe samples — the correction barely reaches the exact
           samples it's meant to fix.

        3. This fix (2026-09-17): weight each sample's squared error by how
           dangerous it is, so danger-close samples dominate the mean instead
           of being diluted by it. prior_coef also raised 0.05 -> 0.15.
           NOT YET VERIFIED — this is reasoned from the logged-magnitude
           evidence above, not confirmed by a new run. If this still isn't
           enough, the next escalation is a full two-head critic (separate
           value baseline for A_safety — see §9.2's closing note).

        alpha_target = alpha_min + (alpha_max − alpha_min) · tau_norm
            tau_norm = 0 (colliding now)  -> target = alpha_min (safety-focus)
            tau_norm = 1 (no danger)      -> target = alpha_max (mission-focus)

        weight = 0.1 + 0.9 · (1 − tau_norm)
            tau_norm = 0 (colliding now)  -> weight = 1.0  (full correction)
            tau_norm = 1 (no danger)      -> weight = 0.1  (light touch — safe
                                              samples were not the problem)

        This keeps α policy-gradient-trained through the Option B pathway
        (still not Option C — the advantage-mixing loss still shapes α every
        step, and d_target/n_conflict influence α purely through that learned
        pathway, unconstrained by this prior).

        Loss term added to the PPO loss: prior_coef · mean(weight · (α − α_target)²)
        """
        if self.prior_coef == 0.0:
            return torch.tensor(0.0, device=alpha.device)
        alpha_target = self.alpha_min + (self.alpha_max - self.alpha_min) * tau_norm
        weight = 0.1 + 0.9 * (1.0 - tau_norm)
        return self.prior_coef * (weight * (alpha.squeeze(-1) - alpha_target).pow(2)).mean()


# ══════════════════════════════════════════════════════════════════════
# 3. PAH WRAPPER — connects PAH to the environment outputs
# ══════════════════════════════════════════════════════════════════════

class PAHWrapper:
    """
    Connects the PAH network to the environment.

    Responsibilities:
        1. Extract τ_collision, d_target, n_conflict from the conflict graph
           and the current observation.
        2. Normalize inputs via PAHNormalizer.
        3. Call PriorityArbitrationHead to get α.
        4. Combine r_mission and r_safety → r_combined.
        5. Log diagnostics for thesis figures.

    Parameters
    ----------
    pah        : PriorityArbitrationHead instance
    normalizer : PAHNormalizer instance
    device     : torch device
    """

    def __init__(
        self,
        pah:        PriorityArbitrationHead,
        normalizer: PAHNormalizer,
        device:     torch.device,
    ):
        self.pah        = pah
        self.normalizer = normalizer
        self.device     = device

        # Running diagnostics — cleared each episode for plotting
        self._diag: dict[str, list] = {
            "alpha":       [],
            "tau":         [],
            "d_target":    [],
            "n_conflict":  [],
        }

    @torch.no_grad()
    def compute_alpha(
        self,
        tau_np:       np.ndarray,   # (n_drones,)
        d_target_np:  np.ndarray,   # (n_drones,)
        n_conflict_np: np.ndarray,  # (n_drones,)
    ) -> np.ndarray:
        """
        Inference-time alpha computation (no gradients).
        Returns alpha as a numpy array of shape (n_drones,).
        """
        tau       = torch.tensor(tau_np,        dtype=torch.float32, device=self.device)
        d_target  = torch.tensor(d_target_np,   dtype=torch.float32, device=self.device)
        n_conflict = torch.tensor(n_conflict_np, dtype=torch.float32, device=self.device)

        x     = self.normalizer.normalize(tau, d_target, n_conflict)   # (n, 3)
        alpha = self.pah(x).squeeze(-1)                                 # (n,)

        alpha_np = alpha.cpu().numpy()

        # Log for diagnostics
        self._diag["alpha"].extend(alpha_np.tolist())
        self._diag["tau"].extend(tau_np.tolist())
        self._diag["d_target"].extend(d_target_np.tolist())
        self._diag["n_conflict"].extend(n_conflict_np.tolist())

        return alpha_np

    def combine_rewards(
        self,
        r_mission:  np.ndarray,   # (n_drones,)
        r_safety:   np.ndarray,   # (n_drones,)
        alpha:      np.ndarray,   # (n_drones,)
    ) -> np.ndarray:
        """
        r_combined = α · r_mission + (1 − α) · r_safety
        Shape: (n_drones,)
        """
        return alpha * r_mission + (1.0 - alpha) * r_safety

    def compute_alpha_gradient(
        self,
        tau_t:        torch.Tensor,   # (B,)
        d_target_t:   torch.Tensor,   # (B,)
        n_conflict_t: torch.Tensor,   # (B,)
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """
        Training-time alpha computation (with gradients — for PPO update).

        Returns (alpha, tau_norm):
            alpha    : (B, 1) — the arbitration weight
            tau_norm : (B,)   — the normalized tau used to compute it, needed
                       by PriorityArbitrationHead.compute_prior_loss's
                       τ-informed target. Returned rather than recomputed so
                       the caller doesn't duplicate the normalizer call.
        """
        x = self.normalizer.normalize(tau_t, d_target_t, n_conflict_t)
        return self.pah(x), x[..., 0]   # (B, 1), (B,)

    def reset_diagnostics(self):
        for key in self._diag:
            self._diag[key] = []

    def get_diagnostics(self) -> dict:
        """Return a snapshot of logged α data for plotting."""
        return {k: np.array(v) for k, v in self._diag.items()}
