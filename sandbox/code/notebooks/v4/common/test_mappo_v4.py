"""
test_mappo_v4.py -- Step 2 gate for v4 Phase 1b (PLAN: v4/02-redesign/PLAN.md, Section 6).
Run:  python test_mappo_v4.py
"""
import json, os, copy
import numpy as np
import torch

import mappo_v4 as M
import v3_env as V3
import env_v4 as E

HERE = os.path.dirname(os.path.abspath(__file__))
V3NB = os.path.join(HERE, '..', '..', 'v3', 'stage2', 'stage2-pah-v3-pah-change', 'var-alpha',
                    'kaggle_stage2_pah_allseeds.ipynb')


def v3_namespace():
    """Executes the v3 notebook's cells 2-4 (conflict graph, env, MAPPOAgent + RolloutBuffer) as they are."""
    cells = [''.join(c['source']) for c in json.load(open(V3NB))['cells']]
    ns = {}
    for i in (1, 2, 3, 4):
        exec(cells[i], ns)
    return ns


def test_gae_matches_hand_calculation():
    g, l = 0.9, 0.5
    r = np.array([[1.0], [0.0], [2.0], [0.0], [1.0]], dtype=np.float32)
    v = np.array([0.5, 0.4, 0.3, 0.2, 0.1], dtype=np.float32)
    dones = np.array([0, 0, 1, 0, 0], dtype=np.float32)      # episode ends at t=2
    last_val = 0.7
    # by hand, backwards
    d4 = 1.0 + g * 0.7 - 0.1;            a4 = d4
    d3 = 0.0 + g * 0.1 - 0.2;            a3 = d3 + g * l * a4
    d2 = 2.0 + 0.0 - 0.3;                a2 = d2                        # mask 0: no bootstrap, no carry
    d1 = 0.0 + g * 0.3 - 0.4;            a1 = d1 + g * l * a2
    d0 = 1.0 + g * 0.4 - 0.5;            a0 = d0 + g * l * a1
    out = M.gae(r, v, last_val, dones, g, l)[:, 0]
    assert np.allclose(out, [a0, a1, a2, a3, a4], atol=1e-6), (out, [a0, a1, a2, a3, a4])


def _collect(env, act_fn, T, n):
    """A fixed batch: list of (obs, act, lp, done, r_m, r_s, info) from env with act_fn."""
    rows, obs = [], env.reset()
    for _ in range(T):
        act, lp = act_fn(obs)
        nobs, _, te, tr, info = env.step(act)
        rows.append((obs, act, lp, te or tr, info))
        obs = env.reset() if (te or tr) else nobs
    return rows, obs


def test_v3_compat_update_is_identical_to_v3():
    """heads=1, actor_adv='mixed', fixed alpha 0.5 must reproduce the v3 MAPPOAgent.update exactly."""
    ns = v3_namespace()
    torch.manual_seed(0); np.random.seed(0)
    n = 5
    v3a = ns['MAPPOAgent'](n_drones=n, obs_dim=ns['OBS_DIM'], act_dim=2, use_pah=False, fixed_alpha=0.5)
    v4a = M.Agent(n_drones=n, obs_dim=ns['OBS_DIM'], heads=1, actor_adv='mixed', alpha_source='fixed', fixed_alpha=0.5)
    v4a.actor.load_state_dict(v3a.actor.state_dict()); v4a.critic.load_state_dict(v3a.critic.state_dict())
    env = ns['MultiUAVEnv'](n_drones=n, n_obstacles=5, seed=3)
    torch.manual_seed(1)
    rows, last_obs = _collect(env, lambda o: tuple(x for x in v3a.get_actions(o)[:2]), 512, n)
    b3, b4 = ns['RolloutBuffer'](n_drones=n), M.Buffer()
    for obs, act, lp, done, info in rows:
        with torch.no_grad():
            val = v3a.critic(torch.tensor(obs, dtype=torch.float32).flatten().unsqueeze(0)).item()
        rew = 0.5 * info['r_mission'] + 0.5 * info['r_safety']
        b3.add(obs, act, rew, val, lp, done, info['r_mission'], info['r_safety'], info['pah_inputs'])
        b4.add(obs, act, lp, done, info['r_mission'], info['r_safety'], rew, (val,), info['pah_inputs'])
    np.random.seed(42); s3 = v3a.update(b3, last_obs)
    np.random.seed(42); s4 = v4a.update(b4, last_obs)
    for (k, p3), (_, p4) in zip(v3a.actor.state_dict().items(), v4a.actor.state_dict().items()):
        assert torch.allclose(p3, p4, atol=1e-6), 'actor ' + k
    for (k, p3), (_, p4) in zip(v3a.critic.state_dict().items(), v4a.critic.state_dict().items()):
        assert torch.allclose(p3, p4, atol=1e-6), 'critic ' + k
    assert abs(s3['actor_loss'] - s4['actor_loss']) < 1e-6 and abs(s3['critic_loss'] - s4['critic_loss']) < 1e-6


def _v4_batch(agent, n=5, m=20, T=512, seed=4):
    env = E.MultiUAVEnvV4(n_drones=n, n_obstacles=m, seed=seed)
    buf, obs = M.Buffer(), env.reset()
    for _ in range(T):
        act, lp, vals = agent.get_actions(obs)
        nobs, _, te, tr, info = env.step(act)
        p = info['pah_inputs']
        alpha = agent.compute_alpha(p['tau'], p['d_target'], p['n_conflict'])
        buf.add(obs, act, lp, te or tr, info['r_mission'], info['r_safety'],
                alpha * info['r_mission'] + (1 - alpha) * info['r_safety'], vals, p)
        obs = env.reset() if (te or tr) else nobs
    return buf, obs


def test_two_head_value_losses_decrease_on_a_fixed_batch():
    torch.manual_seed(0); np.random.seed(0)
    a = M.Agent(n_drones=5, obs_dim=E.OBS_DIM, **{k: v for k, v in M.METHODS['fixed-weight-mappo'].items()})
    buf, last = _v4_batch(a)
    first = a.update(buf, last)
    for _ in range(4):
        out = a.update(buf, last)          # same batch again: the critic should fit it better
    assert out['v_loss_m'] < first['v_loss_m'] and out['v_loss_s'] < first['v_loss_s'], (first, out)


def test_every_method_updates_saves_and_loads(tmp='/tmp'):
    for name, cfg in M.METHODS.items():
        torch.manual_seed(0); np.random.seed(0)
        a = M.Agent(n_drones=5, obs_dim=E.OBS_DIM, **cfg)
        buf, last = _v4_batch(a, T=256)
        s = a.update(buf, last)
        assert all(np.isfinite(v) for v in s.values()), (name, s)
        p = os.path.join(tmp, 'v4_test_{}.pt'.format(name))
        a.save(p)
        b = M.Agent(n_drones=5, obs_dim=E.OBS_DIM, **cfg); b.load(p)
        o = np.random.default_rng(0).uniform(-1, 1, (5, E.OBS_DIM)).astype(np.float32)
        assert np.allclose(a.get_actions(o, deterministic=True)[0], b.get_actions(o, deterministic=True)[0]), name
        os.remove(p)


def test_alpha_sources_behave():
    a_fixed = M.Agent(5, E.OBS_DIM, **M.METHODS['fixed-weight-mappo'])
    a_rule = M.Agent(5, E.OBS_DIM, **M.METHODS['tau-rule-mappo'])
    tau = np.array([0.0, 1.5, 3.0, 3.0, 0.75], dtype=np.float32); d = np.full(5, 100.0, np.float32); nc = np.zeros(5, np.float32)
    assert np.allclose(a_fixed.compute_alpha(tau, d, nc), 0.5)
    assert np.allclose(a_rule.compute_alpha(tau, d, nc), 0.1 + 0.8 * tau / 3.0, atol=1e-6)


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
