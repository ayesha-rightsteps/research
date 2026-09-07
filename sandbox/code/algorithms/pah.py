"""
Priority Arbitration Head (PAH) — the novel contribution of this thesis.

At every decision step, PAH takes three safety-relevant scalars for each drone
and outputs a dynamic weight α ∈ [0.1, 0.9].

    r_combined = α · r_mission + (1 − α) · r_safety

α → 1  means "focus on reaching the target"
α → 0  means "focus on avoiding collisions"

A fixed baseline uses α = 0.5 always.  The thesis claim is that a *learned*,
*state-dependent* α produces better coordination.  PAH is the mechanism that
makes α state-dependent.

Implementation follows Option A from docs/research/01_pah_design.md:
  - α weights the scalar reward (matches the approved synopsis exactly)
  - α prior pulls toward 0.5 (reduces reward-hacking risk)
  - α clipped to [α_min, α_max] so neither objective is ever fully ignored
  - Inputs normalized before entering the MLP (critical for conditioning)
  - Full diagnostics built in (thesis figures come from here)

If reward hacking is observed during training, switch to Option B
(two-head advantage weighting) per the design doc.  That change is isolated
to MAPPO's update method — PAH itself stays the same.

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
    d_max:    float = 141.4   # sqrt(2) * 100
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
    prior_coef : coefficient for the α→0.5 regularizer in the loss
                 (set to 0 to disable; see compute_prior_loss)
    """

    def __init__(
        self,
        hidden_dim: int   = 32,
        alpha_min:  float = 0.1,
        alpha_max:  float = 0.9,
        prior_coef: float = 0.01,
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

    def compute_prior_loss(self, alpha: torch.Tensor) -> torch.Tensor:
        """
        Mild regularizer: pull α toward 0.5.

        Prevents α from collapsing to a constant extreme (a sign of
        reward hacking).  The coefficient prior_coef controls strength.

        Loss term added to the PPO loss: prior_coef · mean((α − 0.5)²)
        """
        if self.prior_coef == 0.0:
            return torch.tensor(0.0, device=alpha.device)
        return self.prior_coef * (alpha - 0.5).pow(2).mean()


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
    ) -> torch.Tensor:
        """
        Training-time alpha computation (with gradients — for PPO update).
        Returns alpha of shape (B, 1).
        """
        x = self.normalizer.normalize(tau_t, d_target_t, n_conflict_t)
        return self.pah(x)   # (B, 1)

    def reset_diagnostics(self):
        for key in self._diag:
            self._diag[key] = []

    def get_diagnostics(self) -> dict:
        """Return a snapshot of logged α data for plotting."""
        return {k: np.array(v) for k, v in self._diag.items()}


# ══════════════════════════════════════════════════════════════════════
# 4. REWARD SPLITTER — environment returns two separate components
# ══════════════════════════════════════════════════════════════════════

def split_reward(drone_pos, target_pos, assignment,
                 obstacle_pos, world_size, collision_radius) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute r_mission and r_safety separately for each drone.

    r_mission : progress reward — negative distance to target (normalized)
    r_safety  : collision penalty — −1 if any collision, else 0

    This function is called by the environment when PAH is active.
    Keeping the two components separate lets PAH combine them with learned α,
    and lets us log per-objective curves for thesis analysis.

    Returns
    -------
    r_mission : (n_drones,)
    r_safety  : (n_drones,)
    """
    n = len(drone_pos)
    r_mission = np.zeros(n, dtype=np.float32)
    r_safety  = np.zeros(n, dtype=np.float32)

    for i in range(n):
        # Mission: negative normalized distance to assigned target
        dist = np.linalg.norm(drone_pos[i] - target_pos[assignment[i]])
        r_mission[i] = -dist / world_size

        # Safety: flat collision penalty
        collided = False

        # drone–drone
        for j in range(n):
            if j == i:
                continue
            if np.linalg.norm(drone_pos[i] - drone_pos[j]) < collision_radius:
                collided = True
                break

        # drone–obstacle
        if not collided:
            for obs_pos in obstacle_pos:
                if np.linalg.norm(drone_pos[i] - obs_pos) < collision_radius:
                    collided = True
                    break

        r_safety[i] = -1.0 if collided else 0.0

    return r_mission, r_safety
