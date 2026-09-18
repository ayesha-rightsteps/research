"""
MAPPO — Multi-Agent Proximal Policy Optimization
Shared actor + centralized critic + GAE + PPO clip + entropy bonus
~350 lines, written to be readable line by line.

TWO-HEAD CRITIC (2026-09-17): when PAH is active, this file now uses two
separate critic heads (critic_m, critic_s) instead of one shared critic —
see MAPPO.__init__ and the "PAH path" branch of MAPPO.update(). Stage 1
(pah_wrapper=None) is completely unaffected — same single shared critic as
before. See docs/research/01_pah_design.md Section 9.2's closing note for
why: a shared critic baseline for A_mission/A_safety could make A_safety
read as unreliable enough, in some seeds, for the advantage-mixing actor
loss to push alpha the wrong way near danger even with the weighted prior
(pah.py's compute_prior_loss) fighting it — verified across 5 seeds,
sessions/2026-09-17.md Sections 13-14 (34% wrong-direction rate with the
shared critic). This mirrors the same fix already ported into the Kaggle
notebooks (code/notebooks/v3/stage2/stage2-pah-v1-all/).
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Normal


# ══════════════════════════════════════════════════════════════════════
# 1. ACTOR — shared by all drones
# ══════════════════════════════════════════════════════════════════════

class Actor(nn.Module):
    """
    Every drone uses the same actor network (shared weights).
    Input : one drone's local observation  shape (obs_dim,)
    Output: a Gaussian distribution over actions
    """

    def __init__(self, obs_dim: int, action_dim: int, hidden: int = 64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden),  nn.Tanh(),
            nn.Linear(hidden, action_dim),
        )
        # log_std is a learnable parameter, not produced by the network
        self.log_std = nn.Parameter(torch.zeros(action_dim))

    def _dist(self, obs: torch.Tensor) -> Normal:
        mean = self.net(obs)
        std  = self.log_std.exp().expand_as(mean)
        return Normal(mean, std)

    def get_action(self, obs: torch.Tensor):
        """Sample an action and return (action, log_prob)."""
        dist    = self._dist(obs)
        action  = dist.sample()
        log_p   = dist.log_prob(action).sum(-1)   # sum over action dims
        return action, log_p

    def evaluate_action(self, obs: torch.Tensor, action: torch.Tensor):
        """Re-evaluate a stored action — used during PPO update."""
        dist    = self._dist(obs)
        log_p   = dist.log_prob(action).sum(-1)
        entropy = dist.entropy().sum(-1)
        return log_p, entropy


# ══════════════════════════════════════════════════════════════════════
# 2. CRITIC — centralized, sees all drones
# ══════════════════════════════════════════════════════════════════════

class Critic(nn.Module):
    """
    Centralized critic — gets the full global state (all drones' obs stacked).
    Input : global state  shape (n_drones * obs_dim,)
    Output: scalar value estimate

    Stage 1 (pah_wrapper=None): ONE instance, trained on the combined reward.
    PAH active: TWO instances (critic_m, critic_s), each trained on its own
    reward stream (r_mission, r_safety) — see MAPPO.__init__.
    """

    def __init__(self, global_dim: int, hidden: int = 64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(global_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden),     nn.Tanh(),
            nn.Linear(hidden, 1),
        )

    def forward(self, global_state: torch.Tensor) -> torch.Tensor:
        return self.net(global_state).squeeze(-1)   # (batch,)


# ══════════════════════════════════════════════════════════════════════
# 3. ROLLOUT BUFFER — stores one rollout of experience
# ══════════════════════════════════════════════════════════════════════

class RolloutBuffer:
    """
    Stores T steps of multi-drone experience and computes GAE.

    Two modes, selected by use_pah:

    use_pah=False (Stage 1) — unchanged from before:
        obs, actions, log_probs, done       : as always
        rewards   : (n_drones,)  combined reward
        values    : scalar  (shared centralized critic output)

    use_pah=True (Stage 2+, two-head critic) — no combined reward/value at
    all now; everything flows through the two component streams:
        r_mission, r_safety : (n_drones,)  reward components
        values_m, values_s  : scalar  (critic_m's / critic_s's own estimate)
        pah_tau, pah_d, pah_n : (n_drones,)  PAH's three inputs
    """

    def __init__(self, n_drones: int, obs_dim: int, action_dim: int, use_pah: bool = False):
        self.n_drones   = n_drones
        self.obs_dim    = obs_dim
        self.action_dim = action_dim
        self.use_pah    = use_pah
        self.clear()

    def clear(self):
        self.obs:       list = []
        self.actions:   list = []
        self.log_probs: list = []
        self.dones:     list = []
        if self.use_pah:
            self.r_mission: list = []
            self.r_safety:  list = []
            self.pah_tau:   list = []
            self.pah_d:     list = []
            self.pah_n:     list = []
            self.values_m:  list = []   # critic_m's own value estimate
            self.values_s:  list = []   # critic_s's own value estimate
        else:
            self.rewards: list = []
            self.values:  list = []

    def add(self, obs, actions, log_probs, done,
            rewards=None, value=None,
            r_mission=None, r_safety=None, pah_inputs=None,
            value_m=None, value_s=None):
        self.obs.append(obs.copy())
        self.actions.append(actions.copy())
        self.log_probs.append(log_probs.copy())
        self.dones.append(bool(done))
        if self.use_pah:
            self.r_mission.append(r_mission.copy())
            self.r_safety.append(r_safety.copy())
            self.pah_tau.append(pah_inputs["tau"].copy())
            self.pah_d.append(pah_inputs["d_target"].copy())
            self.pah_n.append(pah_inputs["n_conflict"].copy())
            self.values_m.append(float(value_m))
            self.values_s.append(float(value_s))
        else:
            self.rewards.append(rewards.copy())
            self.values.append(float(value))

    def __len__(self):
        return len(self.dones)

    def compute_gae(self, last_value: float, gamma: float, lam: float):
        """
        Stage 1 only. Compute per-drone advantages and returns using GAE
        against the single shared critic. UNCHANGED by the two-head fix.

        GAE formula (per drone i, per timestep t):
            delta_i(t) = r_i(t) + gamma * V(s_{t+1}) * (1-done) - V(s_t)
            A_i(t)     = delta_i(t) + gamma * lam * (1-done) * A_i(t+1)

        Returns
        -------
        advantages : (T, n_drones)
        returns    : (T, n_drones)   = advantages + V(s_t) broadcast
        """
        if self.use_pah:
            raise RuntimeError("compute_gae is the Stage-1 path; use compute_gae_components for PAH.")

        T       = len(self.rewards)
        n       = self.n_drones
        rewards = np.array(self.rewards, dtype=np.float32)   # (T, n)
        values  = np.array(self.values,  dtype=np.float32)   # (T,)
        dones   = np.array(self.dones,   dtype=np.float32)   # (T,)

        advantages = np.zeros((T, n), dtype=np.float32)
        last_gae   = np.zeros(n,      dtype=np.float32)

        for t in reversed(range(T)):
            next_val  = last_value if t == T - 1 else values[t + 1]
            mask      = 1.0 - dones[t]
            delta     = rewards[t] + gamma * next_val * mask - values[t]
            last_gae  = delta + gamma * lam * mask * last_gae
            advantages[t] = last_gae

        returns = advantages + values[:, np.newaxis]   # (T, n)
        return advantages, returns

    def compute_gae_components(self, last_value_m: float, last_value_s: float,
                                gamma: float, lam: float):
        """
        TWO-HEAD CRITIC (2026-09-17 escalation). Separate GAE for r_mission
        (baseline = critic_m's own values) and r_safety (baseline =
        critic_s's own values) — each stream is now fully independent, no
        shared baseline between them.

        Before this fix, both streams shared ONE critic's values as their
        baseline ("Option B lite") — see docs/research/01_pah_design.md
        Section 9.2's closing note for why that was replaced: the shared
        baseline let A_safety read as unreliable enough, in some seeds, for
        the advantage-mixing actor loss to push alpha the wrong way near
        danger even with the weighted prior fighting it (34% wrong-direction
        rate across 5 seeds — sessions/2026-09-17.md Sections 13-14).

        Returns
        -------
        adv_mission, adv_safety : (T, n_drones)  — advantages for the actor loss
        ret_mission, ret_safety : (T, n_drones)  — targets for the two value losses
        """
        if not self.use_pah:
            raise RuntimeError("compute_gae_components requires use_pah=True")

        T  = len(self.r_mission)
        n  = self.n_drones
        rm = np.array(self.r_mission, dtype=np.float32)   # (T, n)
        rs = np.array(self.r_safety,  dtype=np.float32)   # (T, n)
        vm = np.array(self.values_m,  dtype=np.float32)   # (T,)
        vs = np.array(self.values_s,  dtype=np.float32)   # (T,)
        dones = np.array(self.dones,  dtype=np.float32)   # (T,)

        adv_m = np.zeros((T, n), dtype=np.float32)
        adv_s = np.zeros((T, n), dtype=np.float32)
        gae_m = np.zeros(n, dtype=np.float32)
        gae_s = np.zeros(n, dtype=np.float32)

        for t in reversed(range(T)):
            next_vm = last_value_m if t == T - 1 else vm[t + 1]
            next_vs = last_value_s if t == T - 1 else vs[t + 1]
            mask    = 1.0 - dones[t]
            delta_m = rm[t] + gamma * next_vm * mask - vm[t]
            delta_s = rs[t] + gamma * next_vs * mask - vs[t]
            gae_m   = delta_m + gamma * lam * mask * gae_m
            gae_s   = delta_s + gamma * lam * mask * gae_s
            adv_m[t] = gae_m
            adv_s[t] = gae_s

        ret_m = adv_m + vm[:, np.newaxis]
        ret_s = adv_s + vs[:, np.newaxis]
        return adv_m, adv_s, ret_m, ret_s

    def to_tensors(self, device):
        """Return stored data as tensors on `device`."""
        obs       = torch.tensor(np.array(self.obs),       dtype=torch.float32, device=device)
        actions   = torch.tensor(np.array(self.actions),   dtype=torch.float32, device=device)
        log_probs = torch.tensor(np.array(self.log_probs), dtype=torch.float32, device=device)
        # shapes: (T,n,obs_dim), (T,n,act_dim), (T,n)

        if not self.use_pah:
            return obs, actions, log_probs, None

        pah_data = {
            "r_mission": torch.tensor(np.array(self.r_mission), dtype=torch.float32, device=device),
            "r_safety":  torch.tensor(np.array(self.r_safety),  dtype=torch.float32, device=device),
            "tau":       torch.tensor(np.array(self.pah_tau),   dtype=torch.float32, device=device),
            "d":         torch.tensor(np.array(self.pah_d),     dtype=torch.float32, device=device),
            "n":         torch.tensor(np.array(self.pah_n),     dtype=torch.float32, device=device),
        }
        return obs, actions, log_probs, pah_data


# ══════════════════════════════════════════════════════════════════════
# 4. MAPPO — puts it all together
# ══════════════════════════════════════════════════════════════════════

class MAPPO:
    """
    Multi-Agent Proximal Policy Optimization.

    How it works in plain language:
        1. Run the environment for `rollout_steps` steps, collect experience.
        2. Compute advantages (GAE): was each action better or worse than expected?
        3. Update actor: make good actions more likely (PPO-clipped so updates stay small).
        4. Update critic(s): make value predictions more accurate.
        5. Repeat until drones learn.

    Parameters
    ----------
    n_drones     : number of agents
    obs_dim      : size of each drone's local observation (e.g. 10)
    action_dim   : size of action vector (e.g. 2 for vx, vy)
    max_speed    : used to clip sampled actions
    lr           : learning rate for Adam optimizer
    gamma        : discount factor (future rewards are worth less)
    lam          : GAE lambda (smoothing factor for advantage estimate)
    clip_eps     : PPO clip range (how big a policy update is allowed)
    vf_coef      : how much the critic loss contributes to total loss
    ent_coef     : entropy bonus (encourages exploration)
    n_epochs     : how many passes over the rollout data per update
    batch_size   : mini-batch size for gradient updates
    pah_wrapper  : PAHWrapper instance, or None for Stage 1 (no PAH — single
                   shared critic). When given, MAPPO uses the two-head critic
                   (critic_m, critic_s) instead — see class docstring above.
    """

    def __init__(
        self,
        n_drones:    int,
        obs_dim:     int,
        action_dim:  int,
        max_speed:   float,
        lr:          float = 3e-4,
        gamma:       float = 0.99,
        lam:         float = 0.95,
        clip_eps:    float = 0.2,
        vf_coef:     float = 0.5,
        ent_coef:    float = 0.01,
        n_epochs:    int   = 10,
        batch_size:  int   = 64,
        pah_wrapper          = None,   # PAHWrapper instance or None (Stage 1 → None)
    ):
        self.n_drones    = n_drones
        self.obs_dim     = obs_dim
        self.action_dim  = action_dim
        self.max_speed   = max_speed
        self.gamma       = gamma
        self.lam         = lam
        self.clip_eps    = clip_eps
        self.vf_coef     = vf_coef
        self.ent_coef    = ent_coef
        self.n_epochs    = n_epochs
        self.batch_size  = batch_size
        self.pah_wrapper = pah_wrapper

        # Pick the best available device: M3 GPU → MPS, else CPU
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")

        global_dim = n_drones * obs_dim
        self.actor = Actor(obs_dim, action_dim).to(self.device)

        if pah_wrapper is not None:
            # Two-head critic (2026-09-17 escalation) — see module docstring.
            self.critic   = None
            self.critic_m = Critic(global_dim).to(self.device)
            self.critic_s = Critic(global_dim).to(self.device)

            pah_wrapper.pah    = pah_wrapper.pah.to(self.device)
            pah_wrapper.device = self.device

            params = (list(self.actor.parameters()) + list(self.critic_m.parameters())
                      + list(self.critic_s.parameters()) + list(pah_wrapper.pah.parameters()))
        else:
            # Stage 1 — single shared critic, unchanged.
            self.critic   = Critic(global_dim).to(self.device)
            self.critic_m = None
            self.critic_s = None
            params = list(self.actor.parameters()) + list(self.critic.parameters())

        self.optimizer = optim.Adam(params, lr=lr)

    # ── inference ──────────────────────────────────────────────────

    @torch.no_grad()
    def get_actions(self, obs_np: np.ndarray):
        """
        Given current observations, return actions, log_probs, and value(s).

        Parameters
        ----------
        obs_np : (n_drones, obs_dim)  numpy array from env.step / env.reset

        Returns
        -------
        Stage 1 (pah_wrapper=None):
            (actions, log_probs, value) — value is the shared critic's estimate
        PAH active:
            (actions, log_probs, value_m, value_s) — one estimate per head
        """
        obs_t = torch.tensor(obs_np, dtype=torch.float32, device=self.device)

        actions_t, log_p_t = self.actor.get_action(obs_t)
        actions_t = actions_t.clamp(-self.max_speed, self.max_speed)

        global_state = obs_t.flatten().unsqueeze(0)     # (1, global_dim)

        if self.pah_wrapper is not None:
            value_m = self.critic_m(global_state).item()
            value_s = self.critic_s(global_state).item()
            return actions_t.cpu().numpy(), log_p_t.cpu().numpy(), value_m, value_s
        else:
            value = self.critic(global_state).item()
            return actions_t.cpu().numpy(), log_p_t.cpu().numpy(), value

    # ── update ─────────────────────────────────────────────────────

    def update(self, buffer: RolloutBuffer, last_obs_np: np.ndarray) -> dict:
        """
        Run PPO update on the collected rollout. Two separate paths depending
        on whether PAH is active — see module docstring for why.

        Returns
        -------
        dict with mean actor_loss, critic_loss, entropy (+ pah_loss if PAH active)
        """
        last_obs_t = torch.tensor(last_obs_np, dtype=torch.float32, device=self.device)
        obs_t, actions_t, old_lp_t, pah_data = buffer.to_tensors(self.device)
        T, n, _ = obs_t.shape

        obs_flat    = obs_t.reshape(T * n, -1)
        act_flat    = actions_t.reshape(T * n, -1)
        old_lp_flat = old_lp_t.reshape(T * n)
        gs_t   = obs_t.reshape(T, -1)
        gs_exp = gs_t.unsqueeze(1).expand(T, n, -1).reshape(T * n, -1)

        total   = T * n
        indices = np.arange(total)

        if self.pah_wrapper is not None and pah_data is not None:
            return self._update_pah(buffer, last_obs_t, obs_flat, act_flat, old_lp_flat,
                                     gs_exp, pah_data, T, n, total, indices)
        else:
            return self._update_stage1(buffer, last_obs_t, obs_flat, act_flat, old_lp_flat,
                                        gs_exp, T, n, total, indices)

    def _update_stage1(self, buffer, last_obs_t, obs_flat, act_flat, old_lp_flat,
                        gs_exp, T, n, total, indices):
        """Stage 1 path — single shared critic. UNCHANGED by the two-head fix."""
        with torch.no_grad():
            gs         = last_obs_t.flatten().unsqueeze(0)
            last_value = self.critic(gs).item()

        advantages_np, returns_np = buffer.compute_gae(last_value, self.gamma, self.lam)
        adv_t = torch.tensor(advantages_np, dtype=torch.float32, device=self.device)
        ret_t = torch.tensor(returns_np,    dtype=torch.float32, device=self.device)

        adv_flat_all = adv_t.reshape(-1)
        adv_t = (adv_t - adv_flat_all.mean()) / (adv_flat_all.std() + 1e-8)
        adv_flat = adv_t.reshape(T * n)
        ret_flat = ret_t.reshape(T * n)

        actor_losses, critic_losses, entropies = [], [], []
        grad_params = list(self.actor.parameters()) + list(self.critic.parameters())

        for _ in range(self.n_epochs):
            np.random.shuffle(indices)
            for start in range(0, total, self.batch_size):
                idx = indices[start: start + self.batch_size]

                log_p, entropy = self.actor.evaluate_action(obs_flat[idx], act_flat[idx])

                v_pred = self.critic(gs_exp[idx])
                v_loss = 0.5 * (v_pred - ret_flat[idx]).pow(2).mean()
                e_loss = -entropy.mean()

                ratio  = (log_p - old_lp_flat[idx]).exp()
                surr1  = ratio * adv_flat[idx]
                surr2  = ratio.clamp(1 - self.clip_eps, 1 + self.clip_eps) * adv_flat[idx]
                a_loss = -torch.min(surr1, surr2).mean()
                loss   = a_loss + self.vf_coef * v_loss + self.ent_coef * e_loss

                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(grad_params, max_norm=0.5)
                self.optimizer.step()

                actor_losses.append(a_loss.item())
                critic_losses.append(v_loss.item())
                entropies.append(-e_loss.item())

        buffer.clear()
        return {
            "actor_loss":  float(np.mean(actor_losses)),
            "critic_loss": float(np.mean(critic_losses)),
            "entropy":     float(np.mean(entropies)),
        }

    def _update_pah(self, buffer, last_obs_t, obs_flat, act_flat, old_lp_flat,
                     gs_exp, pah_data, T, n, total, indices):
        """PAH path — TWO-HEAD CRITIC (2026-09-17 escalation). See module
        docstring and RolloutBuffer.compute_gae_components for why."""
        with torch.no_grad():
            gs_last     = last_obs_t.flatten().unsqueeze(0)
            last_value_m = self.critic_m(gs_last).item()
            last_value_s = self.critic_s(gs_last).item()

        adv_m_np, adv_s_np, ret_m_np, ret_s_np = buffer.compute_gae_components(
            last_value_m, last_value_s, self.gamma, self.lam
        )
        adv_m_t = torch.tensor(adv_m_np, dtype=torch.float32, device=self.device).reshape(-1)
        adv_s_t = torch.tensor(adv_s_np, dtype=torch.float32, device=self.device).reshape(-1)
        adv_m_flat = (adv_m_t - adv_m_t.mean()) / (adv_m_t.std() + 1e-8)
        adv_s_flat = (adv_s_t - adv_s_t.mean()) / (adv_s_t.std() + 1e-8)

        ret_m_flat = torch.tensor(ret_m_np, dtype=torch.float32, device=self.device).reshape(-1)
        ret_s_flat = torch.tensor(ret_s_np, dtype=torch.float32, device=self.device).reshape(-1)

        tau_flat = pah_data["tau"].reshape(T * n)
        d_flat   = pah_data["d"].reshape(T * n)
        nc_flat  = pah_data["n"].reshape(T * n)

        actor_losses, critic_losses, entropies, pah_losses = [], [], [], []
        grad_params = (list(self.actor.parameters()) + list(self.critic_m.parameters())
                       + list(self.critic_s.parameters()) + list(self.pah_wrapper.pah.parameters()))

        for _ in range(self.n_epochs):
            np.random.shuffle(indices)
            for start in range(0, total, self.batch_size):
                idx = indices[start: start + self.batch_size]

                log_p, entropy = self.actor.evaluate_action(obs_flat[idx], act_flat[idx])

                # α-weighted component advantages — PAH gradient flows through α.
                # High α → follow mission advantage, low α → follow safety advantage.
                alpha, tau_norm = self.pah_wrapper.compute_alpha_gradient(
                    tau_flat[idx], d_flat[idx], nc_flat[idx]
                )  # (B, 1), (B,)
                alpha_sq = alpha.squeeze(-1)   # (B,)

                w_adv  = alpha_sq * adv_m_flat[idx] + (1.0 - alpha_sq) * adv_s_flat[idx]
                ratio  = (log_p - old_lp_flat[idx]).exp()
                surr1  = ratio * w_adv
                surr2  = ratio.clamp(1 - self.clip_eps, 1 + self.clip_eps) * w_adv
                a_loss = -torch.min(surr1, surr2).mean()

                # Two independent value losses now — one per critic head.
                v_pred_m = self.critic_m(gs_exp[idx])
                v_pred_s = self.critic_s(gs_exp[idx])
                v_loss_m = 0.5 * (v_pred_m - ret_m_flat[idx]).pow(2).mean()
                v_loss_s = 0.5 * (v_pred_s - ret_s_flat[idx]).pow(2).mean()
                v_loss   = v_loss_m + v_loss_s

                e_loss = -entropy.mean()

                # Prior loss — pulls α toward a τ-informed, danger-weighted target.
                # See PriorityArbitrationHead.compute_prior_loss for the full
                # history of why this exists and how it's weighted.
                pah_prior = self.pah_wrapper.pah.compute_prior_loss(alpha, tau_norm)
                pah_losses.append(pah_prior.item())

                loss = a_loss + self.vf_coef * v_loss + self.ent_coef * e_loss + pah_prior

                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(grad_params, max_norm=0.5)
                self.optimizer.step()

                actor_losses.append(a_loss.item())
                critic_losses.append(v_loss.item())
                entropies.append(-e_loss.item())

        buffer.clear()
        result = {
            "actor_loss":  float(np.mean(actor_losses)),
            "critic_loss": float(np.mean(critic_losses)),
            "entropy":     float(np.mean(entropies)),
        }
        if pah_losses:
            result["pah_loss"] = float(np.mean(pah_losses))
        return result

    # ── save / load ────────────────────────────────────────────────

    def save(self, path: str):
        if self.pah_wrapper is not None:
            ckpt = {
                "actor":    self.actor.state_dict(),
                "critic_m": self.critic_m.state_dict(),
                "critic_s": self.critic_s.state_dict(),
                "pah":      self.pah_wrapper.pah.state_dict(),
            }
        else:
            ckpt = {
                "actor":  self.actor.state_dict(),
                "critic": self.critic.state_dict(),
            }
        torch.save(ckpt, path)

    def load(self, path: str):
        """Full load — expects a checkpoint saved by THIS same mode (Stage 1
        vs PAH/two-head). Use load_actor_only() to warm-start across modes
        (e.g. loading a Stage-1/Stage-2b actor into a PAH-active agent)."""
        ckpt = torch.load(path, map_location=self.device, weights_only=True)
        self.actor.load_state_dict(ckpt["actor"])
        if self.pah_wrapper is not None:
            self.critic_m.load_state_dict(ckpt["critic_m"])
            self.critic_s.load_state_dict(ckpt["critic_s"])
            if "pah" in ckpt:
                self.pah_wrapper.pah.load_state_dict(ckpt["pah"])
        else:
            self.critic.load_state_dict(ckpt["critic"])
        print(f"Loaded checkpoint from {path}")

    def load_actor_only(self, path: str):
        """Warm-start: load ONLY the actor from a checkpoint (e.g. Stage 2b's
        plain-MAPPO weights). Both critic heads (if PAH is active) and PAH
        itself always start fresh.

        SUPERSEDED as the default for PAH mode (2026-09-18) — see
        load_actor_and_dup_critic() below. Fresh-random critics paired with
        an already-converged actor caused a much worse failure than this was
        meant to fix (sessions/2026-09-18.md): entropy crashed extremely
        fast (~episode 2300 of 8000) from noisy early advantage estimates,
        and alpha locked into a uniformly WRONG pattern — 11/11 danger-close
        eval samples saturated at alpha_max on seed 42, worse than the 0/14
        wrong the single-shared-critic version had on the same seed. Kept
        here for Stage-1-style use (no PAH) and as a documented ablation
        point if needed later."""
        ckpt = torch.load(path, map_location=self.device, weights_only=True)
        self.actor.load_state_dict(ckpt["actor"])
        print(f"Warm-started actor only from {path}")

    def load_actor_and_dup_critic(self, path: str):
        """Warm-start: load the actor AND duplicate an old single-critic
        checkpoint's weights into BOTH new critic heads (critic_m, critic_s).

        Added 2026-09-18 after load_actor_only() (fresh-random critics)
        caused alpha to lock into a uniformly wrong direction near danger —
        see that method's docstring and sessions/2026-09-18.md for the full
        diagnosis. Duplicating the old critic's weights into both new heads
        gives them a reasonable starting point (mirroring what already works
        for the actor) instead of starting from scratch, while they still
        diverge from each other during training since each is trained on a
        different reward stream (r_mission vs r_safety) from that point on.

        Only meaningful when PAH is active and `path` has an old-style single
        'critic' key (e.g. Stage 2b's checkpoint). If PAH is inactive, this
        behaves like load() — loads the matching single critic normally."""
        ckpt = torch.load(path, map_location=self.device, weights_only=True)
        self.actor.load_state_dict(ckpt["actor"])
        if self.pah_wrapper is not None:
            if "critic" in ckpt:
                self.critic_m.load_state_dict(ckpt["critic"])
                self.critic_s.load_state_dict(ckpt["critic"])
                print(f"Warm-started actor + BOTH critic heads (duplicated from old single critic) from {path}")
            else:
                self.critic_m.load_state_dict(ckpt["critic_m"])
                self.critic_s.load_state_dict(ckpt["critic_s"])
                print(f"Warm-started actor + both critic heads (already two-head format) from {path}")
        else:
            self.critic.load_state_dict(ckpt["critic"])
            print(f"Warm-started actor + critic from {path}")
