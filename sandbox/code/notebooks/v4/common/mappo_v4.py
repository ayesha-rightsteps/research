"""
mappo_v4.py -- the v4 MAPPO agent (Phase 1b, plan: v4/02-redesign/PLAN.md).

Reuses the frozen v3 classes unchanged (single copy, from v3_env.py): Critic (one head),
PAHNormalizer, PriorityArbitrationHead. The training Actor (with get_action / evaluate_action) is copied
verbatim below from the v3 Stage 2 training notebook -- v3_env.py only holds the inference-only Actor;
parameter names are identical, so checkpoints are interchangeable. New here:
  * Critic2   -- shared body, two heads: V_mission and V_safety.
  * HandCodedRule -- the v3 Hand-coded tau-rule (copied from the v3 h-baseline notebook, unchanged).
  * Buffer    -- stores per-step rewards and the value(s); GAE per head (same GAE formula as v3).
  * Agent     -- one class, configured by:
        heads        1 | 2         one shared critic (v3) or separate mission / safety value heads (v4)
        actor_adv    'mixed'       alpha*z(A_mission) + (1-alpha)*z(A_safety)      (v3 and v4 two-head methods)
                     'plain'       z(A_combined)                                   (Plain MAPPO)
        alpha_source 'fixed' | 'taurule' | 'pah'
    The PPO update (minibatching, clipping, entropy, gradient clipping, PAH prior loss) is the v3 update;
    the only changes are marked "v4:".

Methods (PLAN Section 2):
    Plain MAPPO              heads=1, actor_adv='plain', alpha_source='fixed', fixed_alpha=0.5
    Fixed-weight MAPPO       heads=2, actor_adv='mixed', alpha_source='fixed', fixed_alpha=0.5
    Hand-coded tau-rule MAPPO heads=2, actor_adv='mixed', alpha_source='taurule'
    MAPPO + PAH              heads=2, actor_adv='mixed', alpha_source='pah'
  (heads=1, actor_adv='mixed' is the v3 agent -- used only to test that the shared machinery is unchanged.)
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Normal

from v3_env import Critic, PAHNormalizer, PriorityArbitrationHead

DEVICE = torch.device('cpu')

# ---- training Actor, verbatim from v3/stage2/stage2-pah-v3-pah-change/var-alpha (cell 4) ----
class Actor(nn.Module):
    def __init__(self, obs_dim, act_dim, hidden=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden),  nn.Tanh(),
        )
        self.mu_head = nn.Linear(hidden, act_dim)
        self.log_std = nn.Parameter(torch.zeros(act_dim))

    def forward(self, x):
        h       = self.net(x)
        mu      = self.mu_head(h)
        log_std = self.log_std.clamp(-4.0, 1.5)   # safety net, see Stage 2 notes
        std     = log_std.exp().expand_as(mu)
        return Normal(mu, std)

    def get_action(self, obs):
        dist   = self(obs)
        action = dist.sample()
        log_p  = dist.log_prob(action).sum(-1)
        return action, log_p

    def evaluate_action(self, obs, action):
        dist    = self(obs)
        log_p   = dist.log_prob(action).sum(-1)
        entropy = dist.entropy().sum(-1)
        return log_p, entropy


METHODS = {
    'plain-mappo':        dict(heads=1, actor_adv='plain', alpha_source='fixed', fixed_alpha=0.5),
    'fixed-weight-mappo': dict(heads=2, actor_adv='mixed', alpha_source='fixed', fixed_alpha=0.5),
    'tau-rule-mappo':     dict(heads=2, actor_adv='mixed', alpha_source='taurule'),
    'mappo-pah':          dict(heads=2, actor_adv='mixed', alpha_source='pah'),            # risk-learning PAH (fix)
    'mappo-pah-v1-residual': dict(heads=2, actor_adv='mixed', alpha_source='pah-residual'),  # flawed v1, for the record
}
METHOD_NAMES = {'plain-mappo': 'Plain MAPPO', 'fixed-weight-mappo': 'Fixed-weight MAPPO',
                'tau-rule-mappo': 'Hand-coded τ-rule MAPPO', 'mappo-pah': 'MAPPO + PAH'}


class Critic2(nn.Module):
    """v4: centralized critic with a shared body and two heads (mission value, safety value).
    Same body as the v3 Critic (two Tanh layers of 64)."""
    def __init__(self, global_dim, hidden=64):
        super().__init__()
        self.body = nn.Sequential(nn.Linear(global_dim, hidden), nn.Tanh(),
                                  nn.Linear(hidden, hidden), nn.Tanh())
        self.head_m = nn.Linear(hidden, 1)
        self.head_s = nn.Linear(hidden, 1)

    def forward(self, global_state):
        h = self.body(global_state)
        return self.head_m(h).squeeze(-1), self.head_s(h).squeeze(-1)


class HandCodedRule:
    """Hand-coded tau-rule (verbatim behaviour of the v3 h-baseline notebook's HandCodedRule):
    alpha = alpha_min + (alpha_max - alpha_min) * tau_norm, nothing learned, delta = 0."""
    def __init__(self, alpha_min=0.1, alpha_max=0.9):
        self.alpha_min, self.alpha_max = alpha_min, alpha_max

    def __call__(self, x):
        tau_norm = x[..., 0]
        alpha = (self.alpha_min + (self.alpha_max - self.alpha_min) * tau_norm).clamp(self.alpha_min, self.alpha_max)
        return alpha, torch.zeros_like(alpha)


class RiskPAH(nn.Module):
    """v4 PAH (fix of 2026-10-13, see 02-redesign/PAH_FIX_PLAN.md). Same inputs (tau, d_target, n_conflict, normalized)
    and same 3 -> hidden -> 1 network as the v3 PAH; it predicts the risk p in (0,1) that safety costs are ahead and
    sets alpha = alpha_max - (alpha_max - alpha_min) * p. It is trained by regression onto the observed safety
    cost-to-go (Agent.update), never through the actor's PPO objective."""
    def __init__(self, hidden_dim=32, alpha_min=0.1, alpha_max=0.9):
        super().__init__()
        self.alpha_min, self.alpha_max = alpha_min, alpha_max
        self.net = nn.Sequential(nn.Linear(3, hidden_dim), nn.ReLU(), nn.Linear(hidden_dim, 1))

    def forward(self, x):
        p = torch.sigmoid(self.net(x).squeeze(-1))
        return self.alpha_max - (self.alpha_max - self.alpha_min) * p, p


def gae(rewards, values, last_val, dones, gamma, lam):
    """The v3 GAE (RolloutBuffer.compute_gae), written once for any reward stream.
    rewards (T,n); values (T,) one value per step shared by the drones; dones (T,)."""
    T, n = rewards.shape
    adv = np.zeros((T, n), dtype=np.float32)
    last = np.zeros(n, dtype=np.float32)
    for t in reversed(range(T)):
        next_val = last_val if t == T - 1 else values[t + 1]
        mask = 1.0 - dones[t]
        delta = rewards[t] + gamma * next_val * mask - values[t]
        last = delta + gamma * lam * mask * last
        adv[t] = last
    return adv


class Buffer:
    def __init__(self):
        self.clear()

    def clear(self):
        self.obs, self.acts, self.lps, self.dones = [], [], [], []
        self.r_m, self.r_s, self.rews = [], [], []
        self.v, self.v_m, self.v_s = [], [], []
        self.tau, self.d_target, self.n_conflict = [], [], []

    def add(self, obs, act, lp, done, r_m, r_s, rew, values, pah_inputs):
        self.obs.append(obs.copy()); self.acts.append(act.copy()); self.lps.append(lp.copy())
        self.dones.append(bool(done))
        self.r_m.append(r_m.copy()); self.r_s.append(r_s.copy()); self.rews.append(rew.copy())
        if len(values) == 1:
            self.v.append(values[0])
        else:
            self.v_m.append(values[0]); self.v_s.append(values[1])
        self.tau.append(pah_inputs['tau'].copy())
        self.d_target.append(pah_inputs['d_target'].copy())
        self.n_conflict.append(pah_inputs['n_conflict'].copy())

    def __len__(self):
        return len(self.obs)


class Agent:
    def __init__(self, n_drones, obs_dim, act_dim=2, heads=2, actor_adv='mixed', alpha_source='pah',
                 fixed_alpha=0.5, pah_hidden=32, alpha_min=0.1, alpha_max=0.9, pah_delta_scale=0.2,
                 pah_prior_coef=0.15, pah_horizon=3.0, pah_d_max=500.0 * 1.4142136,
                 lr=3e-4, gamma=0.99, lam=0.95, clip_eps=0.2, vf_coef=0.5, ent_coef=0.003,
                 n_epochs=10, batch_size=64, hidden=64, risk_scale=10.0, pah_coef=1.0):
        assert heads in (1, 2) and actor_adv in ('mixed', 'plain') and alpha_source in ('fixed', 'taurule', 'pah', 'pah-residual')
        assert alpha_source != 'pah' or heads == 2, 'the risk-learning PAH needs the safety value head'
        self.n_drones, self.heads, self.actor_adv, self.alpha_source = n_drones, heads, actor_adv, alpha_source
        self.fixed_alpha = fixed_alpha
        self.gamma, self.lam, self.clip_eps = gamma, lam, clip_eps
        self.vf_coef, self.ent_coef = vf_coef, ent_coef
        self.n_epochs, self.batch_size = n_epochs, batch_size
        self.risk_scale, self.pah_coef = risk_scale, pah_coef

        global_dim = n_drones * obs_dim
        self.actor = Actor(obs_dim, act_dim, hidden).to(DEVICE)          # hidden=64 is the v3 size
        self.critic = (Critic(global_dim, hidden) if heads == 1 else Critic2(global_dim, hidden)).to(DEVICE)
        params = list(self.actor.parameters()) + list(self.critic.parameters())
        self.normalizer = PAHNormalizer(pah_horizon, pah_d_max, n_drones)
        if alpha_source == 'pah':                     # risk-learning PAH (fix)
            self.pah = RiskPAH(pah_hidden, alpha_min, alpha_max).to(DEVICE)
            params += list(self.pah.parameters())
        elif alpha_source == 'pah-residual':          # v1 = v3 residual PAH (biased; kept for the record)
            self.pah = PriorityArbitrationHead(pah_hidden, alpha_min, alpha_max, pah_delta_scale, pah_prior_coef).to(DEVICE)
            params += list(self.pah.parameters())
        elif alpha_source == 'taurule':
            self.pah = HandCodedRule(alpha_min, alpha_max)
        else:
            self.pah = None
        self.params = params
        self.opt = optim.Adam(params, lr=lr)

    # ---------------------------------------------------------------- acting
    def _values(self, gs):
        out = self.critic(gs)
        return (out,) if self.heads == 1 else out

    @torch.no_grad()
    def get_actions(self, obs, deterministic=False):
        obs_t = torch.tensor(obs, dtype=torch.float32, device=DEVICE)
        if deterministic:
            act = self.actor(obs_t).mean
            lp = torch.zeros(obs_t.shape[0])
        else:
            act, lp = self.actor.get_action(obs_t)
        vals = tuple(v.item() for v in self._values(obs_t.flatten().unsqueeze(0)))
        return act.cpu().numpy(), lp.cpu().numpy(), vals

    def _alpha(self, tau_t, d_t, n_t):
        if self.alpha_source == 'fixed':
            return torch.full((tau_t.shape[0],), self.fixed_alpha, dtype=torch.float32, device=DEVICE), None
        x = self.normalizer.normalize(tau_t, d_t, n_t)
        return self.pah(x)

    @torch.no_grad()
    def compute_alpha(self, tau_np, d_np, n_np):
        t = lambda a: torch.tensor(a, dtype=torch.float32, device=DEVICE)
        return self._alpha(t(tau_np), t(d_np), t(n_np))[0].cpu().numpy()

    # ---------------------------------------------------------------- learning
    def update(self, buf, last_obs):
        with torch.no_grad():
            last = tuple(v.item() for v in self._values(torch.tensor(last_obs, dtype=torch.float32).flatten().unsqueeze(0)))
        dones = np.array(buf.dones, dtype=np.float32)
        r_m = np.array(buf.r_m, dtype=np.float32); r_s = np.array(buf.r_s, dtype=np.float32)
        rews = np.array(buf.rews, dtype=np.float32)
        if self.heads == 1:
            v = np.array(buf.v, dtype=np.float32)
            A = gae(rews, v, last[0], dones, self.gamma, self.lam)            # combined (critic target)
            A_m = gae(r_m, v, last[0], dones, self.gamma, self.lam)           # v3: both streams on the shared value
            A_s = gae(r_s, v, last[0], dones, self.gamma, self.lam)
            ret = A + v[:, None]
        else:                                                                  # v4: each stream on its own head
            v_m = np.array(buf.v_m, dtype=np.float32); v_s = np.array(buf.v_s, dtype=np.float32)
            A_m = gae(r_m, v_m, last[0], dones, self.gamma, self.lam)
            A_s = gae(r_s, v_s, last[1], dones, self.gamma, self.lam)
            A = None
            ret_m = A_m + v_m[:, None]; ret_s = A_s + v_s[:, None]

        obs_np = np.array(buf.obs, dtype=np.float32); T, N, D = obs_np.shape
        tens = lambda a: torch.tensor(np.asarray(a, dtype=np.float32).reshape(T * N, *np.asarray(a).shape[2:]), device=DEVICE)
        obs_flat, act_flat = tens(obs_np), tens(np.array(buf.acts))
        lp_flat = tens(np.array(buf.lps))
        tau_f, d_f, nc_f = tens(np.array(buf.tau)), tens(np.array(buf.d_target)), tens(np.array(buf.n_conflict))
        zn = lambda x: (x - x.mean()) / (x.std() + 1e-8)                      # as v3 (torch std, unbiased)
        z_m = zn(torch.tensor(A_m, device=DEVICE).reshape(-1))
        z_s = zn(torch.tensor(A_s, device=DEVICE).reshape(-1))
        z_c = zn(torch.tensor(A, device=DEVICE).reshape(-1)) if A is not None else None
        if self.heads == 1:
            ret_flat = torch.tensor(ret, device=DEVICE).reshape(-1)
        else:
            ret_m_flat = torch.tensor(ret_m, device=DEVICE).reshape(-1)
            ret_s_flat = torch.tensor(ret_s, device=DEVICE).reshape(-1)
        gs_exp = obs_flat.reshape(T, N * D).unsqueeze(1).expand(T, N, -1).reshape(T * N, -1)

        idx_all = np.arange(T * N)
        st = {k: [] for k in ('actor_loss', 'critic_loss', 'v_loss_m', 'v_loss_s', 'entropy', 'alpha', 'pah_loss', 'delta',
                              'risk_pred', 'risk_target')}
        for _ in range(self.n_epochs):
            np.random.shuffle(idx_all)
            for start in range(0, T * N, self.batch_size):
                idx = idx_all[start:start + self.batch_size]
                log_p, entropy = self.actor.evaluate_action(obs_flat[idx], act_flat[idx])
                alpha, delta = self._alpha(tau_f[idx], d_f[idx], nc_f[idx])
                if self.alpha_source == 'pah':                                 # fix: no actor-loss gradient into PAH
                    alpha = alpha.detach()
                if self.actor_adv == 'plain':
                    w_adv = z_c[idx]                                           # v4: Plain MAPPO
                else:
                    w_adv = alpha * z_m[idx] + (1.0 - alpha) * z_s[idx]
                ratio = (log_p - lp_flat[idx]).exp()
                a_loss = -torch.min(ratio * w_adv, ratio.clamp(1 - self.clip_eps, 1 + self.clip_eps) * w_adv).mean()
                if self.heads == 1:
                    v_loss = 0.5 * (self.critic(gs_exp[idx]) - ret_flat[idx]).pow(2).mean()
                else:                                                          # v4: one loss per head
                    pm, ps = self.critic(gs_exp[idx])
                    vl_m = 0.5 * (pm - ret_m_flat[idx]).pow(2).mean()
                    vl_s = 0.5 * (ps - ret_s_flat[idx]).pow(2).mean()
                    v_loss = vl_m + vl_s
                    st['v_loss_m'].append(vl_m.item()); st['v_loss_s'].append(vl_s.item())
                e_loss = -entropy.mean()
                loss = a_loss + self.vf_coef * v_loss + self.ent_coef * e_loss
                if self.alpha_source == 'pah':                                 # fix: PAH predicts the safety cost-to-go
                    risk_target = (-ret_s_flat[idx] / self.risk_scale).clamp(0.0, 1.0)
                    pah_loss = (delta - risk_target).pow(2).mean()             # here `delta` is the predicted risk p
                    loss = loss + self.pah_coef * pah_loss
                    st['pah_loss'].append(pah_loss.item()); st['risk_pred'].append(delta.detach().mean().item())
                    st['risk_target'].append(risk_target.mean().item())
                elif self.alpha_source == 'pah-residual':
                    prior = self.pah.compute_prior_loss(delta)
                    loss = loss + prior
                    st['pah_loss'].append(prior.item()); st['delta'].append(delta.detach().abs().mean().item())
                self.opt.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.params, 0.5)
                self.opt.step()
                st['actor_loss'].append(a_loss.item()); st['critic_loss'].append(v_loss.item())
                st['entropy'].append(-e_loss.item()); st['alpha'].append(alpha.detach().mean().item())
        out = {k: float(np.mean(v)) for k, v in st.items() if v}
        out['alpha_std'] = float(np.std(st['alpha']))
        return out

    # ---------------------------------------------------------------- save / load
    def save(self, path):
        ckpt = {'actor': self.actor.state_dict(), 'critic': self.critic.state_dict(),
                'config': dict(heads=self.heads, actor_adv=self.actor_adv, alpha_source=self.alpha_source,
                               fixed_alpha=self.fixed_alpha)}
        if self.alpha_source in ('pah', 'pah-residual'):
            ckpt['pah'] = self.pah.state_dict()
        torch.save(ckpt, path)

    def load(self, path):
        ckpt = torch.load(path, map_location=DEVICE, weights_only=False)
        self.actor.load_state_dict(ckpt['actor']); self.critic.load_state_dict(ckpt['critic'])
        if self.alpha_source in ('pah', 'pah-residual'):
            self.pah.load_state_dict(ckpt['pah'])
