"""
MAPPO — Multi-Agent Proximal Policy Optimization
Shared actor  + centralized critic + GAE + PPO clip + entropy bonus
~350 lines, written to be readable line by line.
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

    Shapes stored per step:
        obs       : (n_drones, obs_dim)
        actions   : (n_drones, action_dim)
        rewards   : (n_drones,)
        value     : scalar   (centralized critic output)
        log_probs : (n_drones,)
        done      : bool

    When use_pah=True, also stores:
        r_mission  : (n_drones,)  — mission component of reward
        r_safety   : (n_drones,)  — safety component of reward
        pah_tau    : (n_drones,)  — τ_collision input to PAH
        pah_d      : (n_drones,)  — d_target input to PAH
        pah_n      : (n_drones,)  — n_conflict input to PAH
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
        self.rewards:   list = []
        self.values:    list = []
        self.log_probs: list = []
        self.dones:     list = []
        if self.use_pah:
            self.r_mission: list = []
            self.r_safety:  list = []
            self.pah_tau:   list = []
            self.pah_d:     list = []
            self.pah_n:     list = []

    def add(self, obs, actions, rewards, value, log_probs, done,
            r_mission=None, r_safety=None, pah_inputs=None):
        self.obs.append(obs.copy())
        self.actions.append(actions.copy())
        self.rewards.append(rewards.copy())
        self.values.append(float(value))
        self.log_probs.append(log_probs.copy())
        self.dones.append(bool(done))
        if self.use_pah and r_mission is not None:
            self.r_mission.append(r_mission.copy())
            self.r_safety.append(r_safety.copy())
            self.pah_tau.append(pah_inputs["tau"].copy())
            self.pah_d.append(pah_inputs["d_target"].copy())
            self.pah_n.append(pah_inputs["n_conflict"].copy())

    def __len__(self):
        return len(self.rewards)

    def compute_gae(self, last_value: float, gamma: float, lam: float):
        """
        Compute per-drone advantages and returns using GAE.

        GAE formula (per drone i, per timestep t):
            delta_i(t) = r_i(t) + gamma * V(s_{t+1}) * (1-done) - V(s_t)
            A_i(t)     = delta_i(t) + gamma * lam * (1-done) * A_i(t+1)

        V is the shared centralized value — same for all drones at a step.
        r_i differs per drone → advantages differ per drone.

        Returns
        -------
        advantages : (T, n_drones)
        returns    : (T, n_drones)   = advantages + V(s_t) broadcast
        """
        T       = len(self.rewards)
        n       = self.n_drones
        rewards = np.array(self.rewards,   dtype=np.float32)   # (T, n)
        values  = np.array(self.values,    dtype=np.float32)   # (T,)
        dones   = np.array(self.dones,     dtype=np.float32)   # (T,)

        advantages = np.zeros((T, n), dtype=np.float32)
        last_gae   = np.zeros(n,      dtype=np.float32)

        for t in reversed(range(T)):
            next_val  = last_value if t == T - 1 else values[t + 1]
            mask      = 1.0 - dones[t]
            # delta differs per drone (per-drone rewards, shared baseline)
            delta     = rewards[t] + gamma * next_val * mask - values[t]
            last_gae  = delta + gamma * lam * mask * last_gae
            advantages[t] = last_gae

        returns = advantages + values[:, np.newaxis]   # (T, n)
        return advantages, returns

    def compute_gae_components(self, last_value: float, gamma: float, lam: float):
        """
        Option B: separate GAE for r_mission and r_safety.

        Uses the combined-reward value function as a shared baseline so a
        second critic head is not needed.  This is principled (α shapes
        policy improvement direction, not accumulated reward) while keeping
        the architecture simple.

        Returns
        -------
        adv_mission : (T, n_drones)
        adv_safety  : (T, n_drones)
        """
        if not self.use_pah:
            raise RuntimeError("compute_gae_components requires use_pah=True")

        T      = len(self.rewards)
        n      = self.n_drones
        rm     = np.array(self.r_mission, dtype=np.float32)   # (T, n)
        rs     = np.array(self.r_safety,  dtype=np.float32)   # (T, n)
        values = np.array(self.values,    dtype=np.float32)   # (T,)
        dones  = np.array(self.dones,     dtype=np.float32)   # (T,)

        adv_m  = np.zeros((T, n), dtype=np.float32)
        adv_s  = np.zeros((T, n), dtype=np.float32)
        gae_m  = np.zeros(n,      dtype=np.float32)
        gae_s  = np.zeros(n,      dtype=np.float32)

        for t in reversed(range(T)):
            nv      = last_value if t == T - 1 else values[t + 1]
            mask    = 1.0 - dones[t]
            delta_m = rm[t] + gamma * nv * mask - values[t]
            delta_s = rs[t] + gamma * nv * mask - values[t]
            gae_m   = delta_m + gamma * lam * mask * gae_m
            gae_s   = delta_s + gamma * lam * mask * gae_s
            adv_m[t] = gae_m
            adv_s[t] = gae_s

        return adv_m, adv_s

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
        4. Update critic: make value predictions more accurate.
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

        global_dim  = n_drones * obs_dim
        self.actor  = Actor(obs_dim, action_dim).to(self.device)
        self.critic = Critic(global_dim).to(self.device)

        # PAH must live on the same device as actor/critic
        if pah_wrapper is not None:
            pah_wrapper.pah    = pah_wrapper.pah.to(self.device)
            pah_wrapper.device = self.device

        # Optimizer covers actor + critic always, plus PAH when active
        params = list(self.actor.parameters()) + list(self.critic.parameters())
        if pah_wrapper is not None:
            params += list(pah_wrapper.pah.parameters())
        self.optimizer = optim.Adam(params, lr=lr)

    # ── inference ──────────────────────────────────────────────────

    @torch.no_grad()
    def get_actions(self, obs_np: np.ndarray):
        """
        Given current observations, return actions, log_probs, value.

        Parameters
        ----------
        obs_np : (n_drones, obs_dim)  numpy array from env.step / env.reset

        Returns
        -------
        actions   : (n_drones, action_dim)  numpy, clipped to max_speed
        log_probs : (n_drones,)             numpy
        value     : float                   centralized value estimate
        """
        obs_t = torch.tensor(obs_np, dtype=torch.float32, device=self.device)

        actions_t, log_p_t = self.actor.get_action(obs_t)
        actions_t = actions_t.clamp(-self.max_speed, self.max_speed)

        global_state = obs_t.flatten().unsqueeze(0)     # (1, global_dim)
        value        = self.critic(global_state).item()

        return (
            actions_t.cpu().numpy(),
            log_p_t.cpu().numpy(),
            value,
        )

    # ── update ─────────────────────────────────────────────────────

    def update(self, buffer: RolloutBuffer, last_obs_np: np.ndarray) -> dict:
        """
        Run PPO update on the collected rollout.

        Parameters
        ----------
        buffer      : filled RolloutBuffer
        last_obs_np : observation at the end of rollout (for bootstrapping)

        Returns
        -------
        dict with mean actor_loss, critic_loss, entropy for logging
        """
        # Bootstrap value at end of rollout
        last_obs_t = torch.tensor(last_obs_np, dtype=torch.float32, device=self.device)
        with torch.no_grad():
            gs         = last_obs_t.flatten().unsqueeze(0)
            last_value = self.critic(gs).item()

        advantages_np, returns_np = buffer.compute_gae(last_value, self.gamma, self.lam)

        obs_t, actions_t, old_lp_t, pah_data = buffer.to_tensors(self.device)
        T, n, _ = obs_t.shape

        adv_t = torch.tensor(advantages_np, dtype=torch.float32, device=self.device)
        ret_t = torch.tensor(returns_np,    dtype=torch.float32, device=self.device)

        # Normalise combined advantages (zero mean, unit std) — training stability
        adv_flat = adv_t.reshape(-1)
        adv_t    = (adv_t - adv_flat.mean()) / (adv_flat.std() + 1e-8)

        # Flatten time × drones for mini-batch updates
        obs_flat    = obs_t.reshape(T * n, -1)
        act_flat    = actions_t.reshape(T * n, -1)
        old_lp_flat = old_lp_t.reshape(T * n)
        adv_flat    = adv_t.reshape(T * n)
        ret_flat    = ret_t.reshape(T * n)

        gs_t   = obs_t.reshape(T, -1)
        gs_exp = gs_t.unsqueeze(1).expand(T, n, -1).reshape(T * n, -1)

        # PAH tensors (None when PAH is inactive — Stage 1)
        tau_flat = d_flat = nc_flat = None
        if pah_data is not None:
            tau_flat = pah_data["tau"].reshape(T * n)
            d_flat   = pah_data["d"].reshape(T * n)
            nc_flat  = pah_data["n"].reshape(T * n)

        # Option B: separate component advantages for PAH (computed once, used in every epoch)
        # α weights which direction the policy improves — not which reward accumulates.
        # Gradient flows through α → genuine RL signal, no reward-hacking shortcut.
        adv_m_flat = adv_s_flat = None
        if self.pah_wrapper is not None and pah_data is not None:
            adv_m_np, adv_s_np = buffer.compute_gae_components(last_value, self.gamma, self.lam)
            adv_m_t    = torch.tensor(adv_m_np, dtype=torch.float32, device=self.device).reshape(-1)
            adv_s_t    = torch.tensor(adv_s_np, dtype=torch.float32, device=self.device).reshape(-1)
            adv_m_flat = (adv_m_t - adv_m_t.mean()) / (adv_m_t.std() + 1e-8)
            adv_s_flat = (adv_s_t - adv_s_t.mean()) / (adv_s_t.std() + 1e-8)

        total   = T * n
        indices = np.arange(total)

        actor_losses, critic_losses, entropies, pah_losses = [], [], [], []

        grad_params = list(self.actor.parameters()) + list(self.critic.parameters())
        if self.pah_wrapper is not None:
            grad_params += list(self.pah_wrapper.pah.parameters())

        for _ in range(self.n_epochs):
            np.random.shuffle(indices)
            for start in range(0, total, self.batch_size):
                idx = indices[start: start + self.batch_size]

                log_p, entropy = self.actor.evaluate_action(obs_flat[idx], act_flat[idx])

                # Value loss — critic trained on combined reward (same in both stages)
                v_pred = self.critic(gs_exp[idx])
                v_loss = 0.5 * (v_pred - ret_flat[idx]).pow(2).mean()

                # Entropy bonus
                e_loss = -entropy.mean()

                if self.pah_wrapper is not None and adv_m_flat is not None:
                    # ── Option B actor loss: α-weighted component advantages ──
                    # PAH outputs α; gradient flows through α into this loss.
                    # High α → follow mission advantage (get to target)
                    # Low  α → follow safety advantage (avoid collision)
                    # The critic baseline V is shared — α cannot inflate it.
                    alpha, tau_norm = self.pah_wrapper.compute_alpha_gradient(
                        tau_flat[idx], d_flat[idx], nc_flat[idx]
                    )  # (B, 1), (B,)
                    alpha_sq = alpha.squeeze(-1)   # (B,)

                    w_adv  = alpha_sq * adv_m_flat[idx] + (1.0 - alpha_sq) * adv_s_flat[idx]
                    ratio  = (log_p - old_lp_flat[idx]).exp()
                    surr1  = ratio * w_adv
                    surr2  = ratio.clamp(1 - self.clip_eps, 1 + self.clip_eps) * w_adv
                    a_loss = -torch.min(surr1, surr2).mean()

                    # Prior loss — pulls α toward a τ-informed target (low near
                    # danger, high when safe), not a flat 0.5. See
                    # PriorityArbitrationHead.compute_prior_loss for why this
                    # changed — the flat prior let the advantage-mixing loss
                    # above push α the wrong way near danger.
                    pah_prior = self.pah_wrapper.pah.compute_prior_loss(alpha, tau_norm)
                    pah_losses.append(pah_prior.item())

                    loss = a_loss + self.vf_coef * v_loss + self.ent_coef * e_loss + pah_prior

                else:
                    # ── Standard PPO actor loss (Stage 1 / no PAH) ──────────
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
        ckpt = {
            "actor":  self.actor.state_dict(),
            "critic": self.critic.state_dict(),
        }
        if self.pah_wrapper is not None:
            ckpt["pah"] = self.pah_wrapper.pah.state_dict()
        torch.save(ckpt, path)

    def load(self, path: str):
        ckpt = torch.load(path, map_location=self.device, weights_only=True)
        self.actor.load_state_dict(ckpt["actor"])
        self.critic.load_state_dict(ckpt["critic"])
        if self.pah_wrapper is not None and "pah" in ckpt:
            self.pah_wrapper.pah.load_state_dict(ckpt["pah"])
        print(f"Loaded checkpoint from {path}")
