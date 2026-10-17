"""
test_baselines_v4.py -- Step 1 gate for v4 Phase 2 (PLAN: v4/03-base-paper-baselines/PLAN.md, Section 4).
Run:  python test_baselines_v4.py
(The Phase 1b tests -- test_env_v4.py, test_mappo_v4.py -- must still pass unchanged.)
"""
import os
import numpy as np
import torch

import env_v4 as E
import baselines_v4 as B


def _env(**kw):
    return E.MultiUAVEnvV4(n_drones=kw.pop('n', 5), n_obstacles=kw.pop('m', 10), seed=kw.pop('seed', 3),
                           safety_danger_radius=20.0, collision_penalty=10.0, **kw)


def test_fixed_at_reset_is_hungarian_at_step0_and_never_changes():
    rng = np.random.default_rng(0)
    changed_every_step = 0
    for seed in range(20):
        fixed = _env(seed=seed, assignment='fixed-at-reset'); live = _env(seed=seed)
        fixed.reset(); live.reset()
        assert np.array_equal(fixed.assignment, live.assignment)            # same Hungarian solution at reset
        a0 = fixed.assignment.copy()
        for _ in range(150):
            act = rng.uniform(-5, 5, (5, 2))
            _, _, te, tr, _ = fixed.step(act); live.step(act)
            assert np.array_equal(fixed.assignment, a0)
            changed_every_step += not np.array_equal(live.assignment, a0)
            if te or tr:
                break
    assert changed_every_step > 0                                            # the switch really differs


def test_fixed_arbitrary_is_the_phase1b_hungarian_off():
    a = _env(assignment='fixed-arbitrary'); b = _env(use_hungarian=False)
    oa, ob = a.reset(), b.reset()
    assert np.array_equal(a.assignment, np.arange(5)) and np.array_equal(oa, ob)


def test_all_teammates_block_matches_hand_calculation():
    env = _env(n=5, teammates='all')
    o = env.reset()
    assert o.shape == (5, E.BASE_DIM + E.N_RAYS + 8) and env.obs_dim == 38
    for i in range(5):
        expected = np.concatenate([(env.drone_pos[j] - env.drone_pos[i]) / env.W for j in range(5) if j != i])
        assert np.allclose(o[i, E.BASE_DIM + E.N_RAYS:], expected, atol=1e-6)
    ref = _env(n=5).reset()                                                  # own features identical to default env
    assert np.allclose(o[:, :E.BASE_DIM + E.N_RAYS], ref[:, :E.BASE_DIM + E.N_RAYS])
    assert _env(n=8, m=20, teammates='all').obs_dim == 30 + 14 and _env(teammates='none').obs_dim == 30


def _collect(agent, env, T=256):
    buf, obs = B.BaselineBuffer(), env.reset()
    agent.reset_episode()
    for _ in range(T):
        adj = env.cg.adj.copy()
        h = agent.hidden_np() if agent.kind == 'rmappo' else (None, None)
        a, lp, vals = agent.get_actions(obs, adj=adj if agent.uses_graph else None)
        nobs, _, te, tr, info = env.step(a)
        rew = 0.5 * info['r_mission'] + 0.5 * info['r_safety']
        buf.add(obs, a, lp, te or tr, rew, vals, adj=adj if agent.uses_graph else None, h_a=h[0], h_c=h[1])
        obs = nobs
        if te or tr:
            obs = env.reset(); agent.reset_episode()
    return buf, obs


def test_ippo_critic_sees_only_own_observation():
    torch.manual_seed(0)
    env = _env(teammates='all')
    ag = B.BaselineAgent('ippo', 5, env.obs_dim)
    assert ag.critic.net[0].in_features == env.obs_dim
    _, _, vals = ag.get_actions(env.reset())
    assert np.asarray(vals[0]).shape == (5,)


def test_rmappo_chunk_replay_reproduces_collection_log_probs():
    """Before any update, re-running the GRU over every stored chunk (from the stored hidden state, zeroing it
    after episode ends) must give exactly the log-probabilities recorded during collection (PPO ratio = 1)."""
    torch.manual_seed(0); np.random.seed(0)
    env = E.MultiUAVEnvV4(n_drones=5, n_obstacles=10, seed=5, max_steps=40, teammates='all')   # short episodes
    ag = B.BaselineAgent('rmappo', 5, env.obs_dim)
    buf, _ = _collect(ag, env, T=256)
    assert sum(buf.dones) >= 3                                               # episode ends inside chunks
    T, N = len(buf), 5
    obs = torch.tensor(np.array(buf.obs, dtype=np.float32)); acts = torch.tensor(np.array(buf.acts, dtype=np.float32))
    lps = torch.tensor(np.array(buf.lps, dtype=np.float32))
    h_a = torch.tensor(np.array(buf.h_a)); h_c = torch.tensor(np.array(buf.h_c))
    pairs = np.array([(c, d) for c in range(0, T, ag.chunk_len) for d in range(N)])
    z = torch.zeros(T, N)
    with torch.no_grad():
        lp, _, _, old, _, _ = ag._chunk_eval(pairs, obs, acts, lps, z, z, obs.reshape(T, -1), h_a, h_c,
                                             torch.tensor(np.array(buf.dones, dtype=np.float32)), T)
    assert torch.allclose(lp, old, atol=1e-5), (lp - old).abs().max()
    # hidden state is zero at the first step of every episode
    starts = [0] + [t + 1 for t, d in enumerate(buf.dones[:-1]) if d]
    for t in starts:
        assert np.abs(buf.h_a[t]).max() == 0.0 and np.abs(buf.h_c[t]).max() == 0.0


def test_igat_attends_only_through_the_conflict_graph():
    torch.manual_seed(0)
    ag = B.BaselineAgent('igat', 5, 30)
    obs = np.random.default_rng(1).uniform(-1, 1, (5, 30)).astype(np.float32)
    adj = np.zeros((5, 5), bool); adj[0, 1] = adj[1, 0] = True; adj[3, 4] = adj[4, 3] = True   # {0,1} {2} {3,4}
    base = ag.get_actions(obs, deterministic=True, adj=adj)[0]
    far = obs.copy(); far[3] += 0.5                                           # drone 3: not connected to drone 0
    assert np.allclose(ag.get_actions(far, deterministic=True, adj=adj)[0][0], base[0], atol=1e-6)
    near = obs.copy(); near[1] += 0.5                                         # drone 1: neighbour of drone 0
    assert not np.allclose(ag.get_actions(near, deterministic=True, adj=adj)[0][0], base[0], atol=1e-4)
    perm = np.array([2, 0, 4, 1, 3])                                          # relabelling drones relabels actions
    padj = adj[perm][:, perm]
    assert np.allclose(ag.get_actions(obs[perm], deterministic=True, adj=padj)[0], base[perm], atol=1e-5)


def test_every_baseline_updates_saves_and_loads(tmp='/tmp'):
    for kind in B.KINDS:
        torch.manual_seed(0); np.random.seed(0)
        env = _env(teammates='none' if kind == 'igat' else 'all', assignment='fixed-at-reset')
        ag = B.BaselineAgent(kind, 5, env.obs_dim)
        buf, last = _collect(ag, env, T=256)
        before = [p.detach().clone() for p in ag.actor.parameters()]
        s = ag.update(buf, last)
        assert all(np.isfinite(v) for v in s.values()), (kind, s)
        assert any(not torch.equal(a, b) for a, b in zip(before, ag.actor.parameters())), kind
        p = os.path.join(tmp, 'v4_baseline_{}.pt'.format(kind)); ag.save(p)
        ag2 = B.BaselineAgent(kind, 5, env.obs_dim); ag2.load(p); os.remove(p)
        o, adj = env.reset(), env.cg.adj.copy()
        ag.reset_episode(); ag2.reset_episode()
        x1 = ag.get_actions(o, deterministic=True, adj=adj)[0]; x2 = ag2.get_actions(o, deterministic=True, adj=adj)[0]
        assert np.allclose(x1, x2), kind


def test_values_false_gives_the_same_actions_and_runs_on_other_swarm_sizes():
    """Phase 3: get_actions(values=False) skips the critic only -- same actions -- so a model trained on 5 drones can act
    for 8 (IGAT-style here; the Phase 1b agent is checked in test_mappo_v4)."""
    import mappo_v4 as M
    for kind in B.KINDS:
        torch.manual_seed(0)
        env = _env(teammates='none' if kind == 'igat' else 'all', assignment='fixed-at-reset')
        ag = B.BaselineAgent(kind, 5, env.obs_dim)
        o, adj = env.reset(), env.cg.adj.copy()
        ag.reset_episode(); a1 = ag.get_actions(o, deterministic=True, adj=adj)[0]
        ag.reset_episode(); a2, _, v = ag.get_actions(o, deterministic=True, adj=adj, values=False)
        assert np.array_equal(a1, a2) and v == (), kind
    env8 = E.MultiUAVEnvV4(n_drones=8, n_obstacles=5, seed=2, teammates='none', assignment='fixed-at-reset')
    ag = B.BaselineAgent('igat', 5, env8.obs_dim)
    o = env8.reset()
    a = ag.get_actions(o, deterministic=True, adj=env8.cg.adj.copy(), values=False)[0]
    assert a.shape == (8, 2) and np.isfinite(a).all()
    pm = M.Agent(n_drones=5, obs_dim=E.OBS_DIM, **M.METHODS['mappo-pah'])
    env8c = E.MultiUAVEnvV4(n_drones=8, n_obstacles=5, seed=2)
    a = pm.get_actions(env8c.reset(), deterministic=True, values=False)[0]
    assert a.shape == (8, 2) and np.isfinite(a).all()
    env5c = E.MultiUAVEnvV4(n_drones=5, n_obstacles=5, seed=2); o5 = env5c.reset()
    assert np.array_equal(pm.get_actions(o5, deterministic=True)[0], pm.get_actions(o5, deterministic=True, values=False)[0])


if __name__ == '__main__':
    import sys, time
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    failed = 0
    for t in tests:
        t0 = time.time()
        try:
            t(); print('PASS  {:55s} {:.1f}s'.format(t.__name__, time.time() - t0))
        except AssertionError as e:
            failed += 1; print('FAIL  {:55s} {}'.format(t.__name__, str(e)[:300]))
    print('\n{} / {} passed'.format(len(tests) - failed, len(tests)))
    sys.exit(1 if failed else 0)
