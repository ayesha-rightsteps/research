"""
Conflict Graph — sparse collision-risk detection for multi-UAV coordination.

For each drone pair (i, j), we check whether they are on a collision course
within a look-ahead horizon H using Closest Point of Approach (CPA) math.
Only "at-risk" pairs get an edge — keeping the graph sparse and safety-relevant.

Reference: IGAT-MARL (Rezaee et al., 2026) + docs/research/02_assignment_and_conflict.md
"""

import numpy as np


# ══════════════════════════════════════════════════════════════════════
# CORE CPA MATH
# ══════════════════════════════════════════════════════════════════════

def time_to_closest_approach(pos_i, pos_j, vel_i, vel_j):
    """
    Compute the time at which two drones are closest to each other.

    Plain language:
        Imagine two drones flying in straight lines. At some point in the
        future they will be closest to each other — that moment is t*.
        If t* is negative, they are already moving apart (already passed).

    Math:
        p = relative position  (drone i seen from drone j)
        v = relative velocity
        t* = -(p · v) / (v · v)

    Returns
    -------
    t_star : float
        Time of closest approach. Negative = already separating.
    """
    p = pos_i - pos_j          # relative position  [2]
    v = vel_i - vel_j          # relative velocity  [2]
    vv = np.dot(v, v)

    if vv < 1e-8:              # nearly same velocity — constant separation
        return np.inf          # no future closest point

    t_star = -np.dot(p, v) / vv
    return t_star


def distance_at_closest_approach(pos_i, pos_j, vel_i, vel_j, horizon):
    """
    Compute the minimum distance between two drones within [0, horizon].

    Returns
    -------
    dcpa   : float  — distance at closest point of approach
    t_star : float  — when it happens (clamped to [0, horizon])
    """
    p = pos_i - pos_j
    v = vel_i - vel_j
    vv = np.dot(v, v)

    if vv < 1e-8:
        # Constant separation — DCPA is current distance
        return float(np.linalg.norm(p)), 0.0

    t_star = -np.dot(p, v) / vv
    t_clamped = float(np.clip(t_star, 0.0, horizon))
    dcpa = float(np.linalg.norm(p + v * t_clamped))

    return dcpa, t_star


# ══════════════════════════════════════════════════════════════════════
# CONFLICT GRAPH
# ══════════════════════════════════════════════════════════════════════

class ConflictGraph:
    """
    Sparse conflict graph for N drones.

    An edge (i, j) exists when:
        1. The drones will come within d_danger of each other, AND
        2. This happens within the look-ahead horizon H (in the future).

    Parameters
    ----------
    n_drones    : number of drones
    horizon     : look-ahead time window H (seconds / steps)
    d_danger    : distance threshold — pairs closer than this get an edge
    k_nbr       : max conflict neighbors kept per drone in the observation
                  (sorted by t* — most imminent first; zero-padded if fewer)
    """

    def __init__(self, n_drones: int, horizon: float = 3.0,
                 d_danger: float = 9.0, k_nbr: int = 4):
        self.n_drones = n_drones
        self.horizon  = horizon
        self.d_danger = d_danger
        self.k_nbr    = k_nbr

        # Updated every call to update()
        self.adjacency   = np.zeros((n_drones, n_drones), dtype=bool)
        self.t_star_mat  = np.full((n_drones, n_drones), np.inf)
        self.dcpa_mat    = np.full((n_drones, n_drones), np.inf)

    # ── main update ───────────────────────────────────────────────

    def update(self, drone_pos: np.ndarray, drone_vel: np.ndarray):
        """
        Recompute the conflict graph from current positions and velocities.

        Parameters
        ----------
        drone_pos : (n_drones, 2)
        drone_vel : (n_drones, 2)
        """
        n = self.n_drones
        self.adjacency[:]  = False
        self.t_star_mat[:] = np.inf
        self.dcpa_mat[:]   = np.inf

        for i in range(n):
            for j in range(i + 1, n):
                dcpa, t_star = distance_at_closest_approach(
                    drone_pos[i], drone_pos[j],
                    drone_vel[i], drone_vel[j],
                    self.horizon
                )
                self.dcpa_mat[i, j] = self.dcpa_mat[j, i] = dcpa
                self.t_star_mat[i, j] = self.t_star_mat[j, i] = t_star

                # Edge condition: close approach AND in the future within horizon
                if dcpa < self.d_danger and 0.0 <= t_star <= self.horizon:
                    self.adjacency[i, j] = self.adjacency[j, i] = True

    # ── per-drone outputs ─────────────────────────────────────────

    def n_conflict(self, i: int) -> int:
        """Number of conflict neighbors for drone i (PAH input 3)."""
        return int(self.adjacency[i].sum())

    def tau_collision(self, i: int) -> float:
        """
        Time to most imminent collision for drone i (PAH input 1).
        Returns horizon (normalized to 1 = safe) if no conflict edges.
        """
        neighbors = np.where(self.adjacency[i])[0]
        if len(neighbors) == 0:
            return self.horizon              # safe — no threat
        t_values = self.t_star_mat[i, neighbors]
        return float(np.min(t_values))

    def neighbor_obs(self, i: int,
                     drone_pos: np.ndarray,
                     drone_vel: np.ndarray) -> np.ndarray:
        """
        Build the fixed-length conflict-neighbor observation for drone i.

        Format per neighbor slot (5 numbers):
            [rel_pos_x, rel_pos_y, rel_vel_x, rel_vel_y, mask]
        mask = 1 if slot is occupied, 0 if zero-padded.

        Returns
        -------
        obs : (k_nbr * 5,)  — always same size regardless of actual neighbors
        """
        obs = np.zeros(self.k_nbr * 5, dtype=np.float32)

        neighbors = np.where(self.adjacency[i])[0]
        if len(neighbors) == 0:
            return obs

        # Sort by t* — most imminent threat first
        t_vals = self.t_star_mat[i, neighbors]
        order  = np.argsort(t_vals)
        neighbors = neighbors[order]

        for slot, j in enumerate(neighbors[:self.k_nbr]):
            base = slot * 5
            obs[base:base+2] = drone_pos[j] - drone_pos[i]   # relative position
            obs[base+2:base+4] = drone_vel[j] - drone_vel[i] # relative velocity
            obs[base+4] = 1.0                                  # mask = occupied

        return obs

    # ── summary ───────────────────────────────────────────────────

    def summary(self) -> dict:
        """Return a dict of graph stats for logging."""
        n_edges     = int(self.adjacency.sum()) // 2
        degrees     = self.adjacency.sum(axis=1)
        return {
            "n_edges":      n_edges,
            "max_degree":   int(degrees.max()),
            "mean_degree":  float(degrees.mean()),
        }
