"""
baselines_v4.py -- the base paper's comparison methods for v4 Phase 2 (plan: v4/03-base-paper-baselines/PLAN.md).

MAPPO and DA-MAPPO (2D) need no new agent code: they are the Phase 1b "Plain MAPPO" agent (mappo_v4.Agent with
one value head and the combined 0.5 / 0.5 reward) run in a different environment setting:
    MAPPO          assignment='fixed-at-reset', teammates='all'
    DA-MAPPO (2D)  assignment='every-step',     teammates='all'
This file adds the three methods that need a different network or critic:
    IPPO             critic sees only the drone's own observation (no shared critic information)
    RMAPPO           GRU actor and GRU critic, PPO on chunks of consecutive steps
    IGAT-style MAPPO actor = encoder + 2 IGAT blocks x 2 graph-attention layers over the conflict graph
Everything else is the Plain MAPPO update of mappo_v4.Agent: one value head, combined reward, the combined
advantage z-normalized over the batch, PPO clip 0.2, entropy, value loss 0.5, gradient clip 0.5, Adam 3e-4,
10 epochs, minibatches of 64 drone-steps.

Interface used by the training / evaluation loops (same as mappo_v4.Agent, plus two optional hooks):
    get_actions(obs, deterministic=False, adj=None) -> actions (n,2), log-probs (n,), values tuple
    reset_episode()          RMAPPO: zero the hidden states (called after every env.reset())
    get_state() / set_state(s)  RMAPPO: save / restore hidden states around a training-time evaluation
    uses_graph = True        IGAT: the loop passes adj = env.cg.adj (conflict graph of the current state)
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Normal

from v3_env import Critic
from mappo_v4 import Actor, gae, DEVICE

KINDS = ('ippo', 'rmappo', 'igat')


# ------------------------------------------------------------------------------------------------- networks
class GRUActor(nn.Module):
    """RMAPPO actor: Linear+Tanh -> GRU cell -> mean head; state-independent log std (as Actor)."""
    def __init__(self, obs_dim, act_dim, hidden=64):
        super().__init__()
        self.fc = nn.Sequential(nn.Linear(obs_dim, hidden), nn.Tanh())
        self.gru = nn.GRUCell(hidden, hidden)
        self.mu_head = nn.Linear(hidden, act_dim)
        self.log_std = nn.Parameter(torch.zeros(act_dim))
        self.hidden = hidden

    def step(self, x, h):
        h = self.gru(self.fc(x), h)
        mu = self.mu_head(h)
        std = self.log_std.clamp(-4.0, 1.5).exp().expand_as(mu)
        return Normal(mu, std), h


class GRUCritic(nn.Module):
    """RMAPPO centralized critic: Linear+Tanh -> GRU cell -> value."""
    def __init__(self, global_dim, hidden=64):
        super().__init__()
        self.fc = nn.Sequential(nn.Linear(global_dim, hidden), nn.Tanh())
        self.gru = nn.GRUCell(hidden, hidden)
        self.v = nn.Linear(hidden, 1)
        self.hidden = hidden

    def step(self, x, h):
        h = self.gru(self.fc(x), h)
        return self.v(h).squeeze(-1), h


class GATLayer(nn.Module):
    """One multi-head graph-attention layer with residual + LayerNorm (IGAT-MARL Section 3): linear transform,
    pairwise score LeakyReLU(a_src.Wh_i + a_dst.Wh_j), non-neighbours masked out, softmax over neighbours,
    weighted sum, heads concatenated, then LayerNorm(x + ELU(out))."""
    def __init__(self, dim, heads=4):
        super().__init__()
        assert dim % heads == 0
        self.h, self.dh = heads, dim // heads
        self.W = nn.Linear(dim, dim, bias=False)
        self.a_src = nn.Parameter(torch.randn(heads, self.dh) * 0.1)
        self.a_dst = nn.Parameter(torch.randn(heads, self.dh) * 0.1)
        self.ln = nn.LayerNorm(dim)

    def forward(self, x, mask):
        """x (B,n,dim); mask (B,n,n) bool, mask[b,i,j] = drone i may attend to drone j (self always True)."""
        B, n, _ = x.shape
        wh = self.W(x).view(B, n, self.h, self.dh)
        score = F.leaky_relu((wh * self.a_src).sum(-1).unsqueeze(2) + (wh * self.a_dst).sum(-1).unsqueeze(1), 0.2)
        score = score.masked_fill(~mask.unsqueeze(-1), float('-inf'))          # (B, i, j, heads)
        att = torch.softmax(score, dim=2)
        out = torch.einsum('bijh,bjhd->bihd', att, wh).reshape(B, n, -1)
        return self.ln(x + F.elu(out))


class IGATActor(nn.Module):
    """IGAT-style actor: own observation -> Linear+Tanh -> 2 IGAT blocks x 2 GAT layers over the conflict graph
    -> mean head; state-independent log std."""
    def __init__(self, obs_dim, act_dim, hidden=64, heads=4, blocks=2, layers_per_block=2):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(obs_dim, hidden), nn.Tanh())
        self.gat = nn.ModuleList([GATLayer(hidden, heads) for _ in range(blocks * layers_per_block)])
        self.mu_head = nn.Linear(hidden, act_dim)
        self.log_std = nn.Parameter(torch.zeros(act_dim))

    def forward(self, x, adj):
        """x (B,n,obs_dim); adj (B,n,n) bool conflict graph (diagonal ignored, self-attention always on)."""
        mask = adj | torch.eye(x.shape[1], dtype=torch.bool, device=x.device).unsqueeze(0)
        h = self.enc(x)
        for layer in self.gat:
            h = layer(h, mask)
        mu = self.mu_head(h)
        std = self.log_std.clamp(-4.0, 1.5).exp().expand_as(mu)
        return Normal(mu, std)


# ------------------------------------------------------------------------------------------------- buffer
class BaselineBuffer:
    def __init__(self):
        self.clear()

    def clear(self):
        self.obs, self.acts, self.lps, self.dones, self.rews, self.vals = [], [], [], [], [], []
        self.adj, self.h_a, self.h_c = [], [], []

    def add(self, obs, act, lp, done, rew, vals, adj=None, h_a=None, h_c=None):
        self.obs.append(obs.copy()); self.acts.append(act.copy()); self.lps.append(lp.copy())
        self.dones.append(bool(done)); self.rews.append(rew.copy()); self.vals.append(np.array(vals[0], dtype=np.float32))
        if adj is not None:
            self.adj.append(adj.copy())
        if h_a is not None:
            self.h_a.append(h_a.copy()); self.h_c.append(h_c.copy())

    def __len__(self):
        return len(self.obs)


# ------------------------------------------------------------------------------------------------- agent
class BaselineAgent:
    def __init__(self, kind, n_drones, obs_dim, act_dim=2, hidden=64, lr=3e-4, gamma=0.99, lam=0.95, clip_eps=0.2,
                 vf_coef=0.5, ent_coef=0.003, n_epochs=10, batch_size=64, chunk_len=16, gat_heads=4, **_unused):
        assert kind in KINDS, kind
        self.kind, self.n_drones, self.obs_dim, self.hidden = kind, n_drones, obs_dim, hidden
        self.gamma, self.lam, self.clip_eps = gamma, lam, clip_eps
        self.vf_coef, self.ent_coef, self.n_epochs, self.batch_size = vf_coef, ent_coef, n_epochs, batch_size
        self.chunk_len = chunk_len
        self.uses_graph = kind == 'igat'
        global_dim = n_drones * obs_dim
        if kind == 'ippo':
            self.actor = Actor(obs_dim, act_dim, hidden)
            self.critic = Critic(obs_dim, hidden)                    # local critic: V(o_i)
        elif kind == 'rmappo':
            self.actor = GRUActor(obs_dim, act_dim, hidden)
            self.critic = GRUCritic(global_dim, hidden)
        else:
            self.actor = IGATActor(obs_dim, act_dim, hidden, heads=gat_heads)
            self.critic = Critic(global_dim, hidden)
        self.actor.to(DEVICE); self.critic.to(DEVICE)
        self.params = list(self.actor.parameters()) + list(self.critic.parameters())
        self.opt = optim.Adam(self.params, lr=lr)
        self.reset_episode()

    # ---------------------------------------------------------------- recurrent state (RMAPPO only)
    def reset_episode(self):
        self.h_a = torch.zeros(self.n_drones, self.hidden)
        self.h_c = torch.zeros(1, self.hidden)

    def get_state(self):
        return self.h_a.clone(), self.h_c.clone()

    def set_state(self, s):
        self.h_a, self.h_c = s[0].clone(), s[1].clone()

    def hidden_np(self):
        return self.h_a.numpy().copy(), self.h_c[0].numpy().copy()

    # ---------------------------------------------------------------- acting
    @torch.no_grad()
    def get_actions(self, obs, deterministic=False, adj=None):
        o = torch.tensor(obs, dtype=torch.float32, device=DEVICE)
        if self.kind == 'ippo':
            dist = self.actor(o)
            vals = (self.critic(o).numpy(),)                         # one value per drone
        elif self.kind == 'rmappo':
            dist, self.h_a = self.actor.step(o, self.h_a)
            v, self.h_c = self.critic.step(o.flatten().unsqueeze(0), self.h_c)
            vals = (v.item(),)
        else:
            a = torch.tensor(np.asarray(adj, dtype=bool)).unsqueeze(0)
            dist = self.actor(o.unsqueeze(0), a)
            dist = Normal(dist.mean[0], dist.stddev[0])
            vals = (self.critic(o.flatten().unsqueeze(0)).item(),)
        act = dist.mean if deterministic else dist.sample()
        lp = dist.log_prob(act).sum(-1)
        return act.numpy(), lp.numpy(), vals

    def compute_alpha(self, tau_np, d_np, n_np):
        return np.full(len(tau_np), 0.5, dtype=np.float32)          # combined reward 0.5 / 0.5 (as Plain MAPPO)

    @torch.no_grad()
    def _last_value(self, last_obs):
        o = torch.tensor(last_obs, dtype=torch.float32)
        if self.kind == 'ippo':
            return self.critic(o).numpy()
        if self.kind == 'rmappo':                                    # does not advance the stored hidden state
            return self.critic.step(o.flatten().unsqueeze(0), self.h_c)[0].item()
        return self.critic(o.flatten().unsqueeze(0)).item()

    # ---------------------------------------------------------------- learning
    def update(self, buf, last_obs):
        dones = np.array(buf.dones, dtype=np.float32)
        rews = np.array(buf.rews, dtype=np.float32)                  # (T, n)
        v = np.array(buf.vals, dtype=np.float32)                     # (T,) or (T, n) for IPPO
        A = gae(rews, v, self._last_value(last_obs), dones, self.gamma, self.lam)
        ret = A + (v if v.ndim == 2 else v[:, None])                 # (T, n)
        obs = torch.tensor(np.array(buf.obs, dtype=np.float32)); T, N, D = obs.shape
        acts = torch.tensor(np.array(buf.acts, dtype=np.float32))
        lps = torch.tensor(np.array(buf.lps, dtype=np.float32))
        z = torch.tensor(A).reshape(-1)
        z = ((z - z.mean()) / (z.std() + 1e-8)).reshape(T, N)
        ret_t = torch.tensor(ret)
        st = {'actor_loss': [], 'critic_loss': [], 'entropy': []}

        def ppo_step(log_p, entropy, old_lp, adv, v_pred, v_target):
            ratio = (log_p - old_lp).exp()
            a_loss = -torch.min(ratio * adv, ratio.clamp(1 - self.clip_eps, 1 + self.clip_eps) * adv).mean()
            v_loss = 0.5 * (v_pred - v_target).pow(2).mean()
            e_loss = -entropy.mean()
            loss = a_loss + self.vf_coef * v_loss + self.ent_coef * e_loss
            self.opt.zero_grad(); loss.backward()
            nn.utils.clip_grad_norm_(self.params, 0.5); self.opt.step()
            st['actor_loss'].append(a_loss.item()); st['critic_loss'].append(v_loss.item())
            st['entropy'].append(-e_loss.item())

        if self.kind == 'ippo':                                      # minibatches of drone-steps (as Plain MAPPO)
            of, af, lf = obs.reshape(T * N, D), acts.reshape(T * N, -1), lps.reshape(-1)
            zf, rf = z.reshape(-1), ret_t.reshape(-1)
            idx_all = np.arange(T * N)
            for _ in range(self.n_epochs):
                np.random.shuffle(idx_all)
                for s in range(0, T * N, self.batch_size):
                    i = idx_all[s:s + self.batch_size]
                    log_p, ent = self.actor.evaluate_action(of[i], af[i])
                    ppo_step(log_p, ent, lf[i], zf[i], self.critic(of[i]), rf[i])

        elif self.kind == 'igat':                                    # minibatches of whole time steps (graph)
            adj = torch.tensor(np.array(buf.adj, dtype=bool))
            gs = obs.reshape(T, N * D)
            per = max(1, round(self.batch_size / N))                 # ~64 drone-steps per minibatch
            idx_all = np.arange(T)
            for _ in range(self.n_epochs):
                np.random.shuffle(idx_all)
                for s in range(0, T, per):
                    i = idx_all[s:s + per]
                    dist = self.actor(obs[i], adj[i])
                    log_p = dist.log_prob(acts[i]).sum(-1); ent = dist.entropy().sum(-1)
                    v_pred = self.critic(gs[i]).unsqueeze(1).expand(-1, N)
                    ppo_step(log_p, ent, lps[i], z[i], v_pred, ret_t[i])

        else:                                                        # RMAPPO: chunks of consecutive steps
            L = self.chunk_len
            h_a = torch.tensor(np.array(buf.h_a, dtype=np.float32))  # (T, n, H) hidden state before each step
            h_c = torch.tensor(np.array(buf.h_c, dtype=np.float32))  # (T, H)
            done_t = torch.tensor(dones)
            gs = obs.reshape(T, N * D)
            starts = np.arange(0, T, L)
            pairs = np.array([(c, d) for c in starts for d in range(N)])
            per = max(1, self.batch_size // L)                       # 4 chunks x 16 steps = 64 drone-steps
            for _ in range(self.n_epochs):
                np.random.shuffle(pairs)
                for s in range(0, len(pairs), per):
                    pb = pairs[s:s + per]
                    log_p, ent, v_pred, old, adv, tgt = self._chunk_eval(pb, obs, acts, lps, z, ret_t, gs, h_a, h_c,
                                                                         done_t, T)
                    ppo_step(log_p, ent, old, adv, v_pred, tgt)
        return {k: float(np.mean(x)) for k, x in st.items() if x}

    def _chunk_eval(self, pb, obs, acts, lps, z, ret_t, gs, h_a, h_c, done_t, T):
        """Re-run the GRUs over each (chunk start c, drone d) from the stored hidden state at c; the hidden
        state is zeroed after an episode end inside the chunk, exactly as during collection."""
        L = self.chunk_len
        c = torch.as_tensor(pb[:, 0], dtype=torch.long); d = torch.as_tensor(pb[:, 1], dtype=torch.long)
        t = c.unsqueeze(1) + torch.arange(L).unsqueeze(0)            # (B, L) time index of every chunk step
        if int(t.max()) >= T:
            raise ValueError('rollout length must be a multiple of chunk_len')
        ha, hc = h_a[c, d], h_c[c]                                   # (B, H) hidden state at the chunk start
        out = {k: [] for k in ('lp', 'ent', 'v')}
        for l in range(L):
            if l > 0:                                                # an episode ended at the previous step
                keep = (1.0 - done_t[t[:, l - 1]]).unsqueeze(1)
                ha, hc = ha * keep, hc * keep
            dist, ha = self.actor.step(obs[t[:, l], d], ha)
            v, hc = self.critic.step(gs[t[:, l]], hc)
            out['lp'].append(dist.log_prob(acts[t[:, l], d]).sum(-1)); out['ent'].append(dist.entropy().sum(-1))
            out['v'].append(v)
        tf, df = t.T.reshape(-1), d.repeat(L)                        # same (step-major) order as the lists
        return (torch.cat(out['lp']), torch.cat(out['ent']), torch.cat(out['v']),
                lps[tf, df], z[tf, df], ret_t[tf, df])

    # ---------------------------------------------------------------- save / load
    def save(self, path):
        torch.save({'actor': self.actor.state_dict(), 'critic': self.critic.state_dict(),
                    'config': dict(kind=self.kind)}, path)

    def load(self, path):
        ck = torch.load(path, map_location=DEVICE, weights_only=False)
        self.actor.load_state_dict(ck['actor']); self.critic.load_state_dict(ck['critic'])


# Phase 2 methods: (agent class key, environment switches)
METHODS = {
    'ippo':        dict(agent='ippo',   assignment='fixed-at-reset', teammates='all'),
    'mappo':       dict(agent='plain',  assignment='fixed-at-reset', teammates='all'),
    'rmappo':      dict(agent='rmappo', assignment='fixed-at-reset', teammates='all'),
    'da-mappo-2d': dict(agent='plain',  assignment='every-step',     teammates='all'),
    'igat-style':  dict(agent='igat',   assignment='fixed-at-reset', teammates='none'),
}
METHOD_NAMES = {'ippo': 'IPPO', 'mappo': 'MAPPO', 'rmappo': 'RMAPPO', 'da-mappo-2d': 'DA-MAPPO (2D)',
                'igat-style': 'IGAT-style MAPPO'}
