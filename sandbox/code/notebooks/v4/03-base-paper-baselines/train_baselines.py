"""
train_baselines.py -- v4 Phase 2: train one base-paper method for one (stage, seed). Plan: PLAN.md.

Same loop, settings and logging as 02-redesign/train.py (8000 episodes, 512-step rollouts, PPO settings, combined
reward 0.5 / 0.5, deterministic training-time evaluation every 100 episodes on seed 999, checkpoints every 500
episodes). The only differences are the method's agent and its environment switches (baselines_v4.METHODS).

Usage:
  python train_baselines.py METHOD STAGE SEED [--episodes N] [--out DIR]
  METHOD: ippo | mappo | rmappo | da-mappo-2d | igat-style
  STAGE:  2 (5 drones, 10 discs) | 3 (8 drones, 20 discs)   -- the frozen Phase 1b settings (PLAN 02 Section 10)
"""
import os, sys, json, time
import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
import env_v4 as E
import mappo_v4 as M
import baselines_v4 as B

STAGES = {2: dict(n_drones=5, n_obstacles=10), 3: dict(n_drones=8, n_obstacles=20)}
CFG = dict(world_size=500.0, max_speed=5.0, max_steps=500, target_radius=25.0, collision_radius=3.0,
           success_bonus=20.0, target_speed=1.0, safety_danger_radius=20.0, collision_penalty=10.0,
           total_episodes=8000, rollout_steps=512, eval_every=100, eval_episodes=20, save_every=500, eval_seed=999,
           lr=3e-4, gamma=0.99, lam=0.95, clip_eps=0.2, vf_coef=0.5, ent_coef=0.003, n_epochs=10, batch_size=64,
           hidden=64, chunk_len=16, gat_heads=4)


def make_env(c, seed, bonus=None):
    return E.MultiUAVEnvV4(n_drones=c['n_drones'], n_obstacles=c['n_obstacles'], world_size=c['world_size'],
                           max_speed=c['max_speed'], max_steps=c['max_steps'], collision_radius=c['collision_radius'],
                           target_radius=c['target_radius'], success_bonus=c['success_bonus'] if bonus is None else bonus,
                           target_speed=c['target_speed'], seed=seed, safety_danger_radius=c['safety_danger_radius'],
                           collision_penalty=c['collision_penalty'], assignment=c['assignment'], teammates=c['teammates'])


def make_agent(c):
    keys = ('lr', 'gamma', 'lam', 'clip_eps', 'vf_coef', 'ent_coef', 'n_epochs', 'batch_size', 'hidden')
    kw = {k: c[k] for k in keys}
    if c['agent'] == 'plain':                       # MAPPO / DA-MAPPO (2D): the Plain MAPPO agent
        return M.Agent(n_drones=c['n_drones'], obs_dim=c['obs_dim'], **M.METHODS['plain-mappo'], **kw)
    return B.BaselineAgent(c['agent'], c['n_drones'], c['obs_dim'], chunk_len=c['chunk_len'], gat_heads=c['gat_heads'], **kw)


def act(agent, obs, env, deterministic=False):
    """One policy step, whatever the agent needs (graph for IGAT; RMAPPO keeps its own hidden state)."""
    kw = {'adj': env.cg.adj.copy()} if getattr(agent, 'uses_graph', False) else {}
    return agent.get_actions(obs, deterministic=deterministic, **kw)


def evaluate(agent, c, episodes, seed):
    saved = agent.get_state() if hasattr(agent, 'get_state') else None
    env = make_env(c, seed, bonus=0.0)
    out = dict(success=0, collision=0, timeout=0)
    for _ in range(episodes):
        o, done = env.reset(), False
        if hasattr(agent, 'reset_episode'):
            agent.reset_episode()
        while not done:
            a, _, _ = act(agent, o, env, deterministic=True)
            o, _, te, tr, info = env.step(a)
            done = te or tr
        k = 'collision' if info['episode_collision'] else 'success' if info['all_targets_reached'] else 'timeout'
        out[k] += 1
    if saved is not None:
        agent.set_state(saved)
    return {k: v / episodes for k, v in out.items()}


def main():
    method, stage, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    episodes = int(sys.argv[sys.argv.index('--episodes') + 1]) if '--episodes' in sys.argv else CFG['total_episodes']
    out_dir = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else \
        os.path.join(HERE, 'runs', 'stage{}'.format(stage), method, 'seed-{}'.format(seed))
    c = dict(CFG, **STAGES[stage], **B.METHODS[method], method=method, stage=stage, seed=seed,
             episodes=episodes)
    c['obs_dim'] = make_env(c, 0).obs_dim
    os.makedirs(out_dir, exist_ok=True)
    torch.set_num_threads(1)
    np.random.seed(seed); torch.manual_seed(seed)
    agent = make_agent(c)
    json.dump(c, open(os.path.join(out_dir, 'config.json'), 'w'), indent=1)

    plain = isinstance(agent, M.Agent)
    env = make_env(c, seed)
    buf = M.Buffer() if plain else B.BaselineBuffer()
    hist, obs = {}, env.reset()
    if not plain:
        agent.reset_episode()
    ep_count, last_eval, last_save, t0 = 0, 0, 0, time.time()
    print('{} | stage {} | seed {} | obs dim {}'.format(B.METHOD_NAMES[method], stage, seed, c['obs_dim']), flush=True)
    while ep_count < episodes:
        for _ in range(c['rollout_steps']):
            adj = env.cg.adj.copy()
            h = agent.hidden_np() if c['agent'] == 'rmappo' else (None, None)
            a, lp, vals = act(agent, obs, env)
            nobs, _, te, tr, info = env.step(a)
            done = te or tr
            rew = 0.5 * info['r_mission'] + 0.5 * info['r_safety']
            if plain:
                buf.add(obs, a, lp, done, info['r_mission'], info['r_safety'], rew, vals, info['pah_inputs'])
            else:
                buf.add(obs, a, lp, done, rew, vals, adj=adj if agent.uses_graph else None, h_a=h[0], h_c=h[1])
            obs = nobs
            if done:
                ep_count += 1
                obs = env.reset()
                if not plain:
                    agent.reset_episode()
        stats = agent.update(buf, obs)
        buf.clear()
        if ep_count >= last_eval + c['eval_every']:
            ev = evaluate(agent, c, c['eval_episodes'], c['eval_seed'])
            row = dict(episode=ep_count, minutes=(time.time() - t0) / 60, **{k: v for k, v in stats.items()
                                                                             if k in ('actor_loss', 'critic_loss', 'entropy')}, **ev)
            for k, v in row.items():
                hist.setdefault(k, []).append(v)
            print('{:>6} | succ {:5.1%} | coll {:5.1%} | timeout {:5.1%} | {:.1f}m'.format(
                ep_count, ev['success'], ev['collision'], ev['timeout'], row['minutes']), flush=True)
            last_eval = ep_count
        if ep_count >= last_save + c['save_every']:
            agent.save(os.path.join(out_dir, 'checkpoint_ep{}.pt'.format(ep_count)))
            last_save = ep_count
    agent.save(os.path.join(out_dir, 'final_model.pt'))
    json.dump(hist, open(os.path.join(out_dir, 'history.json'), 'w'), indent=1)
    json.dump(dict(wall_minutes=round((time.time() - t0) / 60, 2)), open(os.path.join(out_dir, 'wall_time.json'), 'w'))
    print('RUN_DONE {} stage {} seed {} in {:.1f} min'.format(method, stage, seed, (time.time() - t0) / 60))


if __name__ == '__main__':
    main()
