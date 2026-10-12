"""
train.py -- v4 Phase 1b: train one (method, stage, seed). Plan: PLAN.md.

The training loop is the v3 run_training() (v3/stage2/stage2-pah-v3-pah-change/var-alpha, cell 6) with
these changes, all from the plan:
  * environment v4 (../common/env_v4.py) and agent v4 (../common/mappo_v4.py);
  * no warm start (the observation grew from 30 to 50), every run trains from scratch;
  * training-time evaluation is deterministic (v3 sampled actions there) and uses a fixed evaluation seed
    (999) disjoint from the training seeds, so its curve uses the same protocol as the final evaluation;
  * diagnostics are logged during training (Manish's review, session 2026-10-12 Section 16).

Usage:
  python train.py METHOD STAGE SEED [--episodes N] [--out DIR] [--curriculum]
  METHOD: plain-mappo | fixed-weight-mappo | tau-rule-mappo | mappo-pah | mappo-pah-no-hungarian
  STAGE:  2 (5 drones, 20 discs) | 3 (8 drones, 40 discs)
  --curriculum: base-paper obstacle curriculum (only if Step 3 needs it; off by default)
  --danger R, --collision-penalty P: safety-reward shape (Step 3 tuning; defaults = v3: 9, 1)
  --obstacles N, --ent-coef C, --hidden H: Step 3 tuning (defaults: stage's disc count, 0.003, 64)
"""
import os, sys, json, time
import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
import env_v4 as E
import mappo_v4 as M

STAGES = {2: dict(n_drones=5, n_obstacles=20), 3: dict(n_drones=8, n_obstacles=40)}
CFG = dict(world_size=500.0, max_speed=5.0, max_steps=500, target_radius=25.0, collision_radius=3.0,
           success_bonus=20.0, target_speed=1.0,
           total_episodes=8000, rollout_steps=512, eval_every=100, eval_episodes=20, save_every=500,
           lr=3e-4, gamma=0.99, lam=0.95, clip_eps=0.2, vf_coef=0.5, ent_coef=0.003, n_epochs=10, batch_size=64,
           alpha_min=0.1, alpha_max=0.9, pah_delta_scale=0.2, pah_prior_coef=0.15, pah_hidden=32,
           pah_horizon=3.0, pah_d_max=500.0 * 1.4142136, eval_seed=999,
           safety_danger_radius=9.0, collision_penalty=1.0)     # v3 values; Step 3 tuning may change them


def method_config(method):
    if method == 'mappo-pah-no-hungarian':
        return dict(M.METHODS['mappo-pah']), False
    return dict(M.METHODS[method]), True


def make_env(stage, seed, use_hungarian, bonus=None, n_obstacles=None):
    s = STAGES[stage]
    return E.MultiUAVEnvV4(n_drones=s['n_drones'], n_obstacles=s['n_obstacles'] if n_obstacles is None else n_obstacles,
                           world_size=CFG['world_size'], max_speed=CFG['max_speed'], max_steps=CFG['max_steps'],
                           collision_radius=CFG['collision_radius'], target_radius=CFG['target_radius'],
                           success_bonus=CFG['success_bonus'] if bonus is None else bonus,
                           target_speed=CFG['target_speed'], use_hungarian=use_hungarian, seed=seed,
                           safety_danger_radius=CFG['safety_danger_radius'], collision_penalty=CFG['collision_penalty'])


def curriculum_obstacles(ep, total, final):
    """Base-paper style: start with 5 discs, reach the stage's count by 60% of training."""
    frac = min(1.0, ep / (0.6 * total))
    return int(round(5 + frac * (final - 5)))


def evaluate(agent, stage, use_hungarian, episodes, seed):
    env = make_env(stage, seed, use_hungarian, bonus=0.0)
    out = dict(success=0, collision=0, timeout=0, kinds={'drone-drone': 0, 'drone-obstacle': 0, 'both': 0},
               drone_steps=0, safety_on=0, safety_drone=0, safety_obs=0, tau_obstacle=0, tau_drone=0,
               los=0, edges=0, steps=0)
    a_danger, a_safe = [], []
    for _ in range(episodes):
        o, done = env.reset(), False
        while not done:
            a, _, _ = agent.get_actions(o, deterministic=True)
            o, _, te, tr, info = env.step(a)
            done = te or tr
            n = len(info['r_safety'])
            out['drone_steps'] += n; out['steps'] += 1
            out['safety_on'] += int((info['r_safety'] != 0).sum())
            out['safety_drone'] += int(info['safety_cause_drone'].sum())
            out['safety_obs'] += int(info['safety_cause_obstacle'].sum())
            tau, td, to = info['pah_inputs']['tau'], info['tau_drone'], info['tau_obstacle']
            flagged = tau < CFG['pah_horizon'] - 1e-6
            out['tau_obstacle'] += int((flagged & (to <= td)).sum())
            out['tau_drone'] += int((flagged & (td < to)).sum())
            out['los'] += info['los_pairs']; out['edges'] += info['active_edges']
            p = info['pah_inputs']
            al = agent.compute_alpha(p['tau'], p['d_target'], p['n_conflict'])
            a_danger += list(al[tau <= 1.0]); a_safe += list(al[tau >= CFG['pah_horizon'] - 1e-6])
        if info['episode_collision']:
            out['collision'] += 1; out['kinds'][info['collision_kind']] += 1
        elif info['all_targets_reached']:
            out['success'] += 1
        else:
            out['timeout'] += 1
    ds = max(out['drone_steps'], 1)
    return dict(success=out['success'] / episodes, collision=out['collision'] / episodes, timeout=out['timeout'] / episodes,
                coll_drone_drone=out['kinds']['drone-drone'], coll_drone_obstacle=out['kinds']['drone-obstacle'],
                coll_both=out['kinds']['both'],
                safety_on_frac=out['safety_on'] / ds, safety_drone_frac=out['safety_drone'] / ds,
                safety_obs_frac=out['safety_obs'] / ds,
                tau_set_by_obstacle_frac=out['tau_obstacle'] / ds, tau_set_by_drone_frac=out['tau_drone'] / ds,
                los_per_episode=out['los'] / episodes, edges_per_step=out['edges'] / max(out['steps'], 1),
                alpha_danger=float(np.mean(a_danger)) if a_danger else float('nan'),
                alpha_safe=float(np.mean(a_safe)) if a_safe else float('nan'))


def main():
    method, stage, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    episodes = int(sys.argv[sys.argv.index('--episodes') + 1]) if '--episodes' in sys.argv else CFG['total_episodes']
    out_dir = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else \
        os.path.join(HERE, 'runs', 'stage{}'.format(stage), method, 'seed-{}'.format(seed))
    curriculum = '--curriculum' in sys.argv
    n_obstacles_override = int(sys.argv[sys.argv.index('--obstacles') + 1]) if '--obstacles' in sys.argv else None
    if n_obstacles_override is not None:
        STAGES[stage] = dict(STAGES[stage], n_obstacles=n_obstacles_override)
    if '--ent-coef' in sys.argv:
        CFG['ent_coef'] = float(sys.argv[sys.argv.index('--ent-coef') + 1])
    CFG['hidden'] = int(sys.argv[sys.argv.index('--hidden') + 1]) if '--hidden' in sys.argv else 64
    if '--danger' in sys.argv:
        CFG['safety_danger_radius'] = float(sys.argv[sys.argv.index('--danger') + 1])
    if '--collision-penalty' in sys.argv:
        CFG['collision_penalty'] = float(sys.argv[sys.argv.index('--collision-penalty') + 1])
    cfg, use_hungarian = method_config(method)
    os.makedirs(out_dir, exist_ok=True)
    torch.set_num_threads(1)
    np.random.seed(seed); torch.manual_seed(seed)

    n = STAGES[stage]['n_drones']
    agent = M.Agent(n_drones=n, obs_dim=E.OBS_DIM, **cfg, pah_hidden=CFG['pah_hidden'], alpha_min=CFG['alpha_min'],
                    alpha_max=CFG['alpha_max'], pah_delta_scale=CFG['pah_delta_scale'],
                    pah_prior_coef=CFG['pah_prior_coef'], pah_horizon=CFG['pah_horizon'], pah_d_max=CFG['pah_d_max'],
                    lr=CFG['lr'], gamma=CFG['gamma'], lam=CFG['lam'], clip_eps=CFG['clip_eps'], vf_coef=CFG['vf_coef'],
                    ent_coef=CFG['ent_coef'], n_epochs=CFG['n_epochs'], batch_size=CFG['batch_size'],
                    hidden=CFG['hidden'])
    json.dump(dict(method=method, stage=stage, seed=seed, episodes=episodes, curriculum=curriculum,
                   use_hungarian=use_hungarian, agent=cfg, **STAGES[stage], **CFG),
              open(os.path.join(out_dir, 'config.json'), 'w'), indent=1)

    n_obs_now = curriculum_obstacles(0, episodes, STAGES[stage]['n_obstacles']) if curriculum else None
    env = make_env(stage, seed, use_hungarian, n_obstacles=n_obs_now)
    buf, hist = M.Buffer(), {}
    obs, ep_count, last_eval, last_save, t0 = env.reset(), 0, 0, 0, time.time()
    print('{} | stage {} | seed {} | curriculum {}'.format(M.METHOD_NAMES.get(method.replace('-no-hungarian', ''), method)
                                                         + (' (Hungarian off)' if not use_hungarian else ''), stage, seed, curriculum))
    while ep_count < episodes:
        for _ in range(CFG['rollout_steps']):
            act, lp, vals = agent.get_actions(obs)
            nobs, _, te, tr, info = env.step(act)
            done = te or tr
            p = info['pah_inputs']
            alpha = agent.compute_alpha(p['tau'], p['d_target'], p['n_conflict'])
            rew = alpha * info['r_mission'] + (1.0 - alpha) * info['r_safety']
            buf.add(obs, act, lp, done, info['r_mission'], info['r_safety'], rew, vals, p)
            obs = nobs
            if done:
                ep_count += 1
                if curriculum:
                    k = curriculum_obstacles(ep_count, episodes, STAGES[stage]['n_obstacles'])
                    if k != env.n_obs:
                        env.n_obs = k
                obs = env.reset()
        stats = agent.update(buf, obs)
        buf.clear()
        if ep_count >= last_eval + CFG['eval_every']:
            ev = evaluate(agent, stage, use_hungarian, CFG['eval_episodes'], CFG['eval_seed'])
            row = dict(episode=ep_count, minutes=(time.time() - t0) / 60, n_obstacles_train=env.n_obs,
                       log_std=agent.actor.log_std.data.cpu().numpy().tolist(), **stats, **ev)
            for k, v in row.items():
                hist.setdefault(k, []).append(v)
            print('{:>6} | succ {:5.1%} | coll {:5.1%} (obst {}/{}) | timeout {:5.1%} | alpha {:.3f} | {:.1f}m'.format(
                ep_count, ev['success'], ev['collision'], ev['coll_drone_obstacle'] + ev['coll_both'],
                ev['coll_drone_drone'] + ev['coll_drone_obstacle'] + ev['coll_both'], ev['timeout'],
                stats.get('alpha', float('nan')), row['minutes']), flush=True)
            last_eval = ep_count
        if ep_count >= last_save + CFG['save_every']:
            agent.save(os.path.join(out_dir, 'checkpoint_ep{}.pt'.format(ep_count)))
            last_save = ep_count
    agent.save(os.path.join(out_dir, 'final_model.pt'))
    json.dump(hist, open(os.path.join(out_dir, 'history.json'), 'w'), indent=1)
    json.dump(dict(wall_minutes=round((time.time() - t0) / 60, 2)), open(os.path.join(out_dir, 'wall_time.json'), 'w'))
    print('RUN_DONE {} stage {} seed {} in {:.1f} min'.format(method, stage, seed, (time.time() - t0) / 60))


if __name__ == '__main__':
    main()
