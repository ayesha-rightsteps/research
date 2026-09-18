"""
Main training script — Stage 1 MAPPO on the 2D multi-UAV environment.

Run locally  : python3 code/training/train.py
Run on Kaggle: paste this file into a cell and run (see notebook instructions below)

What this script does, step by step:
  1. Load config from a yaml file
  2. Create environment + MAPPO agent
  3. Loop:
       a. Collect 512 steps of experience (rollout)
       b. Update MAPPO using collected experience
       c. Every 100 episodes: evaluate and print results
       d. Every 200 episodes: save checkpoint
  4. Save final model + training curves
"""

import sys, os, yaml, time, json
import numpy as np

# ── path setup so imports work from any working directory ──────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from environment.multi_uav_env import MultiUAVEnv
from algorithms.mappo import MAPPO, RolloutBuffer
from algorithms.pah import PriorityArbitrationHead, PAHNormalizer, PAHWrapper


# ══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════

def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def make_env(cfg: dict, seed: int) -> MultiUAVEnv:
    e = cfg["env"]
    use_cg = e.get("use_conflict_graph", False)
    return MultiUAVEnv(
        n_drones=e["n_drones"],
        n_obstacles=e["n_obstacles"],
        world_size=e["world_size"],
        max_speed=e["max_speed"],
        max_steps=e["max_steps"],
        target_radius=e["target_radius"],
        collision_radius=e["collision_radius"],
        use_conflict_graph=use_cg,
        success_bonus=e.get("success_bonus", 0.0),
        use_hungarian=e.get("use_hungarian", True),
        seed=seed,
    )


def make_pah_wrapper(cfg: dict, env: MultiUAVEnv, device) -> PAHWrapper | None:
    """Create a PAHWrapper if the config requests PAH, else return None."""
    pah_cfg = cfg.get("pah")
    if pah_cfg is None or not pah_cfg.get("enabled", False):
        return None

    e   = cfg["env"]
    pah = PriorityArbitrationHead(
        hidden_dim  = pah_cfg.get("hidden_dim",  32),
        alpha_min   = pah_cfg.get("alpha_min",   0.1),
        alpha_max   = pah_cfg.get("alpha_max",   0.9),
        prior_coef  = pah_cfg.get("prior_coef",  0.01),
    ).to(device)

    norm = PAHNormalizer(
        horizon  = e.get("horizon", 3.0),
        d_max    = e["world_size"] * (2 ** 0.5),
        n_drones = e["n_drones"],
    )

    return PAHWrapper(pah, norm, device)


def make_agent(cfg: dict, env: MultiUAVEnv, pah_wrapper=None) -> MAPPO:
    m = cfg["mappo"]
    return MAPPO(
        n_drones=env.n_drones,
        obs_dim=env.observation_space.shape[1],
        action_dim=env.action_space.shape[1],
        max_speed=env.max_speed,
        lr=m["lr"],
        gamma=m["gamma"],
        lam=m["lam"],
        clip_eps=m["clip_eps"],
        vf_coef=m["vf_coef"],
        ent_coef=m["ent_coef"],
        n_epochs=m["n_epochs"],
        batch_size=m["batch_size"],
        pah_wrapper=pah_wrapper,
    )


def collect_rollout(env, agent, buffer, rollout_steps, pah_wrapper=None):
    """
    Play rollout_steps steps in the environment and store experience in buffer.
    Returns the last observation (needed for GAE bootstrapping).

    TWO-HEAD CRITIC (2026-09-17): when pah_wrapper is active, get_actions()
    returns two value estimates (one per critic head) instead of one, and the
    buffer stores r_mission/r_safety directly — there is no combined reward
    to build anymore (see mappo.py module docstring). pah_wrapper.compute_alpha
    is still called here for its side effect of logging into the running
    diagnostics (pah_wrapper.get_diagnostics(), used for history['alpha_mean']),
    even though its return value is no longer used to blend a reward.
    """
    obs, _ = env.reset()
    for _ in range(rollout_steps):
        if pah_wrapper is not None:
            actions, log_probs, value_m, value_s = agent.get_actions(obs)
        else:
            actions, log_probs, value = agent.get_actions(obs)

        next_obs, rewards, terminated, truncated, info = env.step(actions)
        done = terminated or truncated

        r_mission   = info.get("r_mission")
        r_safety    = info.get("r_safety")
        pah_inputs  = info.get("pah_inputs")

        if pah_wrapper is not None and pah_inputs is not None:
            pah_wrapper.compute_alpha(
                pah_inputs["tau"], pah_inputs["d_target"], pah_inputs["n_conflict"]
            )
            buffer.add(obs, actions, log_probs, done,
                       r_mission=r_mission, r_safety=r_safety, pah_inputs=pah_inputs,
                       value_m=value_m, value_s=value_s)
        else:
            buffer.add(obs, actions, log_probs, done, rewards=rewards, value=value)

        obs = next_obs
        if done:
            obs, _ = env.reset()
    return obs   # last obs for bootstrap


def evaluate(env, agent, n_episodes: int) -> dict:
    """
    Run n_episodes with the current policy (no training).
    Returns mission success rate and collision rate.
    """
    successes  = 0
    collisions = 0

    for _ in range(n_episodes):
        obs, _ = env.reset()
        while True:
            if agent.pah_wrapper is not None:
                actions, _, _, _ = agent.get_actions(obs)
            else:
                actions, _, _ = agent.get_actions(obs)
            obs, _, terminated, truncated, info = env.step(actions)
            if terminated or truncated:
                if info["all_targets_reached"]:
                    successes += 1
                if info["any_collision"]:
                    collisions += 1
                break

    return {
        "success_rate":   successes  / n_episodes,
        "collision_rate": collisions / n_episodes,
    }


def save_results(results_dir, run_name, history, agent):
    """Save training log (JSON) and final model."""
    os.makedirs(results_dir, exist_ok=True)
    run_dir = os.path.join(results_dir, run_name)
    os.makedirs(run_dir, exist_ok=True)

    # Training log
    log_path = os.path.join(run_dir, "training_log.json")
    with open(log_path, "w") as f:
        json.dump(history, f, indent=2)

    # Final model
    model_path = os.path.join(run_dir, "final_model.pt")
    agent.save(model_path)

    print(f"\nResults saved to: {run_dir}/")
    return run_dir


def print_header(cfg):
    e = cfg["env"]
    t = cfg["training"]
    print("=" * 55)
    print("  MAPPO Training — Stage 1")
    print("=" * 55)
    print(f"  Drones     : {e['n_drones']}")
    print(f"  Obstacles  : {e['n_obstacles']}")
    print(f"  Episodes   : {t['total_episodes']}")
    print(f"  Seed       : {t['seed']}")
    print("=" * 55)


# ══════════════════════════════════════════════════════════════════════
# MAIN TRAINING LOOP
# ══════════════════════════════════════════════════════════════════════

def train(config_path: str = None):

    # ── load config ────────────────────────────────────────────────
    if config_path is None:
        config_path = os.path.join(ROOT, "configs", "stage1.yaml")
    cfg = load_config(config_path)

    seed          = cfg["training"]["seed"]
    total_eps     = cfg["training"]["total_episodes"]
    rollout_steps = cfg["training"]["rollout_steps"]
    eval_every    = cfg["training"]["eval_every"]
    eval_eps      = cfg["training"]["eval_episodes"]
    save_every    = cfg["training"]["save_every"]
    results_dir   = os.path.join(ROOT, "..", cfg["paths"]["results_dir"])
    run_name      = cfg["paths"]["run_name"]

    np.random.seed(seed)

    # ── setup ──────────────────────────────────────────────────────
    env         = make_env(cfg, seed=seed)
    eval_env    = make_env(cfg, seed=seed + 1000)

    # Determine device early so PAH and agent share the same one
    import torch
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    pah_wrapper = make_pah_wrapper(cfg, env, device)
    agent       = make_agent(cfg, env, pah_wrapper=pah_wrapper)
    buffer      = RolloutBuffer(
        n_drones=env.n_drones,
        obs_dim=env.observation_space.shape[1],
        action_dim=env.action_space.shape[1],
        use_pah=(pah_wrapper is not None),
    )

    print_header(cfg)
    print(f"  Device: {agent.device}\n")

    # ── tracking ───────────────────────────────────────────────────
    history = {
        "episode":       [],
        "success_rate":  [],
        "collision_rate":[],
        "actor_loss":    [],
        "critic_loss":   [],
        "entropy":       [],
        "pah_loss":      [],   # stays empty when PAH is inactive
        "alpha_mean":    [],   # mean α across rollout when PAH is active
    }

    episode    = 0
    update_num = 0
    start_time = time.time()
    obs, _     = env.reset()

    # ── training loop ──────────────────────────────────────────────
    while episode < total_eps:

        # 1. Collect experience
        last_obs = collect_rollout(env, agent, buffer, rollout_steps,
                                   pah_wrapper=pah_wrapper)
        episode += max(1, rollout_steps // cfg["env"]["max_steps"])
        update_num += 1

        # 2. Update MAPPO (+ PAH when active)
        stats = agent.update(buffer, last_obs)

        # 3. Evaluate and log
        if update_num % max(1, eval_every // max(1, rollout_steps // cfg["env"]["max_steps"])) == 0:
            eval_stats = evaluate(eval_env, agent, eval_eps)
            elapsed    = time.time() - start_time

            print(
                f"Ep {episode:4d}/{total_eps} | "
                f"Success: {eval_stats['success_rate']*100:5.1f}% | "
                f"Collision: {eval_stats['collision_rate']*100:5.1f}% | "
                f"ALoss: {stats['actor_loss']:+.3f} | "
                f"CLoss: {stats['critic_loss']:.3f} | "
                f"Ent: {stats['entropy']:.2f} | "
                f"Time: {elapsed/60:.1f}m"
            )

            history["episode"].append(episode)
            history["success_rate"].append(eval_stats["success_rate"])
            history["collision_rate"].append(eval_stats["collision_rate"])
            history["actor_loss"].append(stats["actor_loss"])
            history["critic_loss"].append(stats["critic_loss"])
            history["entropy"].append(stats["entropy"])
            history["pah_loss"].append(stats.get("pah_loss", None))

            if pah_wrapper is not None:
                diag = pah_wrapper.get_diagnostics()
                if len(diag["alpha"]) > 0:
                    history["alpha_mean"].append(float(diag["alpha"].mean()))
                pah_wrapper.reset_diagnostics()

        # 4. Save checkpoint
        if update_num % max(1, save_every // max(1, rollout_steps // cfg["env"]["max_steps"])) == 0:
            run_dir = os.path.join(ROOT, "..", cfg["paths"]["results_dir"], run_name)
            os.makedirs(run_dir, exist_ok=True)
            ckpt_path = os.path.join(run_dir, f"checkpoint_ep{episode}.pt")
            agent.save(ckpt_path)
            print(f"  [checkpoint saved → {ckpt_path}]")

    # ── done ───────────────────────────────────────────────────────
    print("\nTraining complete!")
    final_eval = evaluate(eval_env, agent, n_episodes=50)
    print(f"Final success rate  : {final_eval['success_rate']*100:.1f}%")
    print(f"Final collision rate: {final_eval['collision_rate']*100:.1f}%")

    save_results(
        os.path.join(ROOT, "..", cfg["paths"]["results_dir"]),
        run_name,
        history,
        agent,
    )

    return history


# ══════════════════════════════════════════════════════════════════════
# KAGGLE NOTEBOOK INSTRUCTIONS
# ══════════════════════════════════════════════════════════════════════
"""
Kaggle pe chalane ke liye:

1. New Notebook banao
2. Settings → Accelerator → GPU T4
3. Pehle cell mein:
   !git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   %cd YOUR_REPO/sandbox

4. Doosre cell mein:
   !pip install gymnasium scipy pyyaml --quiet

5. Teesre cell mein:
   import sys; sys.path.insert(0, 'code')
   from training.train import train
   history = train('code/configs/stage1.yaml')

6. Model download karne ke liye:
   from IPython.display import FileLink
   FileLink('code/results/stage1_seed42/final_model.pt')
"""

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=None, help="Path to config yaml")
    args = parser.parse_args()
    train(args.config)
