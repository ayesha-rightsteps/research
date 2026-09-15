"""
Unit tests for MultiUAVEnv.
Run with: python3 -m pytest code/tests/test_env.py -v
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pytest
from environment.multi_uav_env import MultiUAVEnv


# ──────────────────────────────────────────────
# 1. Basic shape and reset
# ──────────────────────────────────────────────

def test_obs_shape():
    """Observation shape: 10 dims without conflict graph, 30 with (10 + 4*5)."""
    env_base = MultiUAVEnv(n_drones=3, n_obstacles=3, seed=0, use_conflict_graph=False)
    obs, _ = env_base.reset()
    assert obs.shape == (3, 10), f"Expected (3,10), got {obs.shape}"

    env_cg = MultiUAVEnv(n_drones=3, n_obstacles=3, seed=0, use_conflict_graph=True)
    obs_cg, _ = env_cg.reset()
    assert obs_cg.shape == (3, 30), f"Expected (3,30), got {obs_cg.shape}"


def test_reset_gives_valid_positions():
    """After reset, all drones and targets must be inside the world."""
    env = MultiUAVEnv(n_drones=3, n_obstacles=3, seed=1)
    env.reset()
    assert np.all(env.drone_pos >= 0) and np.all(env.drone_pos <= env.world_size)
    assert np.all(env.target_pos >= 0) and np.all(env.target_pos <= env.world_size)


def test_step_returns_correct_shapes():
    """step() must return obs, rewards, terminated, truncated, info with right shapes."""
    env = MultiUAVEnv(n_drones=3, n_obstacles=3, seed=2, use_conflict_graph=False)
    env.reset()
    actions = env.action_space.sample()
    obs, rewards, terminated, truncated, info = env.step(actions)
    assert obs.shape == (3, 10), f"Expected (3,10), got {obs.shape}"
    assert rewards.shape == (3,)
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)
    # r_mission and r_safety always in info
    assert "r_mission" in info and "r_safety" in info


# ──────────────────────────────────────────────
# 2. Determinism — same seed = same episode
# ──────────────────────────────────────────────

def test_determinism():
    """Two envs with the same seed must produce identical trajectories."""
    actions_seq = [np.ones((3, 2)) * 2.0 for _ in range(10)]

    def run(seed):
        env = MultiUAVEnv(n_drones=3, n_obstacles=3, seed=seed)
        env.reset()
        positions = []
        for a in actions_seq:
            env.step(a)
            positions.append(env.drone_pos.copy())
        return positions

    traj1 = run(42)
    traj2 = run(42)
    for p1, p2 in zip(traj1, traj2):
        np.testing.assert_array_equal(p1, p2)


# ──────────────────────────────────────────────
# 3. Boundary clamping
# ──────────────────────────────────────────────

def test_drone_stays_inside_world():
    """Drones must never leave the world boundary, even with max speed."""
    env = MultiUAVEnv(n_drones=3, n_obstacles=0, seed=5)
    env.reset()
    for _ in range(50):
        # Push drones hard in one direction
        actions = np.full((3, 2), env.max_speed)
        env.step(actions)
    assert np.all(env.drone_pos >= 0)
    assert np.all(env.drone_pos <= env.world_size)


# ──────────────────────────────────────────────
# 4. Collision detection
# ──────────────────────────────────────────────

def test_drone_drone_collision_detected():
    """Two drones placed on top of each other must trigger a collision."""
    env = MultiUAVEnv(n_drones=2, n_obstacles=0, seed=0)
    env.reset()
    # Force both drones to the same position
    env.drone_pos[0] = np.array([50.0, 50.0])
    env.drone_pos[1] = np.array([50.0, 50.0])
    assert env._drone_collision(0), "Drone-drone collision not detected"


def test_no_false_collision():
    """Drones far apart must NOT trigger a collision."""
    env = MultiUAVEnv(n_drones=2, n_obstacles=0, seed=0)
    env.reset()
    env.drone_pos[0] = np.array([10.0, 10.0])
    env.drone_pos[1] = np.array([90.0, 90.0])
    assert not env._drone_collision(0), "False collision detected"


def test_obstacle_collision_detected():
    """Drone placed on top of an obstacle must trigger a collision."""
    env = MultiUAVEnv(n_drones=1, n_obstacles=1, seed=0)
    env.reset()
    # Place drone exactly on the obstacle
    env.drone_pos[0] = env.obstacle_pos[0].copy()
    assert env._obstacle_collision(0), "Drone-obstacle collision not detected"


# ──────────────────────────────────────────────
# 5. Reward signs
# ──────────────────────────────────────────────

def test_collision_gives_negative_reward():
    """A drone on top of another must receive a negative r_safety."""
    env = MultiUAVEnv(n_drones=2, n_obstacles=0, seed=0, use_conflict_graph=False)
    env.reset()
    env.drone_pos[0] = np.array([50.0, 50.0])
    env.drone_pos[1] = np.array([50.0, 50.0])
    env.drone_vel = np.zeros((2, 2))
    rewards, r_mission, r_safety = env._compute_rewards()
    assert rewards[0] < 0,   "Collision should give negative combined reward"
    assert r_safety[0] == -1.0, "Hard collision should give r_safety = -1.0"


def test_closer_to_target_less_negative_reward():
    """A drone closer to its target should have a less-negative reward than one far away."""
    env = MultiUAVEnv(n_drones=1, n_obstacles=0, seed=0)
    env.reset()
    env.assignment = np.array([0])

    env.target_pos[0] = np.array([50.0, 50.0])

    env.drone_pos[0] = np.array([49.0, 50.0])   # very close
    close_reward = env._compute_rewards()[0]

    env.drone_pos[0] = np.array([10.0, 10.0])    # far away
    far_reward = env._compute_rewards()[0]

    assert close_reward > far_reward, "Closer drone should get better reward"


# ──────────────────────────────────────────────
# 6. Target reached
# ──────────────────────────────────────────────

def test_target_reached_when_close():
    """A drone within target_radius of its target must count as reached."""
    env = MultiUAVEnv(n_drones=1, n_obstacles=0, seed=0)
    env.reset()
    env.assignment = np.array([0])
    env.target_pos[0] = np.array([50.0, 50.0])
    env.drone_pos[0] = np.array([50.0, 50.0])   # exactly on target
    assert env._all_targets_reached(), "Target should be reached"


def test_target_not_reached_when_far():
    """A drone far from its target must NOT count as reached."""
    env = MultiUAVEnv(n_drones=1, n_obstacles=0, seed=0)
    env.reset()
    env.assignment = np.array([0])
    env.target_pos[0] = np.array([50.0, 50.0])
    env.drone_pos[0] = np.array([10.0, 10.0])
    assert not env._all_targets_reached(), "Target should not be reached"


# ──────────────────────────────────────────────
# 7. Hungarian assignment
# ──────────────────────────────────────────────

def test_hungarian_assigns_all_drones():
    """Every drone must get exactly one unique target."""
    env = MultiUAVEnv(n_drones=4, n_obstacles=0, seed=0)
    env.reset()
    assignment = env._hungarian_assignment()
    assert len(assignment) == 4
    assert len(set(assignment)) == 4, "Each drone must have a unique target"


def test_hungarian_obvious_case():
    """
    3 drones and 3 targets lined up — assignment should be identity (0→0, 1→1, 2→2).
    Drone i is closest to target i.
    """
    env = MultiUAVEnv(n_drones=3, n_obstacles=0, seed=0)
    env.reset()
    env.drone_pos  = np.array([[10., 10.], [50., 50.], [90., 90.]], dtype=np.float32)
    env.target_pos = np.array([[10., 10.], [50., 50.], [90., 90.]], dtype=np.float32)
    assignment = env._hungarian_assignment()
    np.testing.assert_array_equal(assignment, [0, 1, 2])


# ──────────────────────────────────────────────
# 8. Timeout
# ──────────────────────────────────────────────

def test_timeout_truncates_episode():
    """Episode must truncate after max_steps even if no target is reached."""
    env = MultiUAVEnv(n_drones=3, n_obstacles=0, max_steps=5, seed=0)
    env.reset()
    terminated = truncated = False
    for _ in range(10):
        if terminated or truncated:
            break
        _, _, terminated, truncated, _ = env.step(np.zeros((3, 2)))
    assert truncated, "Episode should have truncated after max_steps"


# ──────────────────────────────────────────────
# 9. Success bonus (added 2026-09-15 — without it, Stage 1 got 0% success)
# ──────────────────────────────────────────────

def test_success_bonus_awarded_on_arrival():
    """Reaching the target must add success_bonus to both rewards and r_mission."""
    env_bonus = MultiUAVEnv(n_drones=1, n_obstacles=0, use_conflict_graph=False,
                             success_bonus=10.0, seed=0)
    env_plain = MultiUAVEnv(n_drones=1, n_obstacles=0, use_conflict_graph=False,
                             success_bonus=0.0, seed=0)
    for env in (env_bonus, env_plain):
        env.reset()
        env.drone_pos[0]  = env.target_pos[env.assignment[0]].copy()
        env.drone_vel[:]  = 0.0

    _, r_bonus, _, _, info_b = env_bonus.step(np.zeros((1, 2)))
    _, r_plain, _, _, info_p = env_plain.step(np.zeros((1, 2)))

    assert info_b["all_targets_reached"] and info_p["all_targets_reached"]
    assert r_bonus[0] - r_plain[0] == pytest.approx(10.0, abs=1e-4), (
        "success_bonus should add exactly to the reward when all targets are reached"
    )


def test_no_success_bonus_when_not_reached():
    """success_bonus must not leak into the reward when targets are not reached."""
    env = MultiUAVEnv(n_drones=1, n_obstacles=0, use_conflict_graph=False,
                       success_bonus=10.0, seed=0)
    env.reset()
    env.drone_pos[0] = env.target_pos[env.assignment[0]] + np.array([50.0, 0.0])
    _, rewards, _, _, info = env.step(np.zeros((1, 2)))
    assert not info["all_targets_reached"]
    assert rewards[0] < 5.0, "No bonus should be applied when the target isn't reached"


# ──────────────────────────────────────────────
# 10. use_hungarian ablation flag (added 2026-09-15, see notebooks/v3/ablation/)
# ──────────────────────────────────────────────

def test_use_hungarian_true_can_reassign():
    """With Hungarian ON, the assignment is free to change step to step."""
    env = MultiUAVEnv(n_drones=3, n_obstacles=0, use_hungarian=True, seed=3)
    env.reset()
    first = env.assignment.copy()
    for _ in range(20):
        env.step(env.action_space.sample())
    # Not asserting it DID change (may coincidentally stay the same) — only that
    # the mechanism is live: it must equal a fresh Hungarian solve on current state.
    np.testing.assert_array_equal(env.assignment, env._hungarian_assignment())


def test_use_hungarian_false_keeps_fixed_assignment():
    """With Hungarian OFF, the assignment must be the fixed identity pairing,
    set once at reset() and never re-solved in step()."""
    env = MultiUAVEnv(n_drones=4, n_obstacles=0, use_hungarian=False, seed=4)
    env.reset()
    np.testing.assert_array_equal(env.assignment, np.arange(4))
    for _ in range(20):
        env.step(env.action_space.sample())
        np.testing.assert_array_equal(env.assignment, np.arange(4))


# ──────────────────────────────────────────────
# 11. Poisson-disk obstacle placement (added 2026-09-15)
# ──────────────────────────────────────────────

def test_obstacles_respect_minimum_separation():
    """Every pair of obstacles must be >= 2*collision_radius apart, and every
    obstacle >= collision_radius from every drone/target position at reset."""
    for seed in range(10):
        env = MultiUAVEnv(n_drones=3, n_obstacles=5, collision_radius=3.0, seed=seed)
        env.reset()
        obstacles = env.obstacle_pos
        r_obs_min = 2.0 * env.collision_radius

        for i in range(len(obstacles)):
            for j in range(i + 1, len(obstacles)):
                d = np.linalg.norm(obstacles[i] - obstacles[j])
                assert d >= r_obs_min - 1e-6, (
                    f"seed={seed}: obstacles {i},{j} are {d:.2f} apart, "
                    f"need >= {r_obs_min}"
                )

        existing = np.concatenate([env.drone_pos, env.target_pos])
        for obs_pos in obstacles:
            d = np.min(np.linalg.norm(existing - obs_pos, axis=-1))
            assert d >= env.collision_radius - 1e-6, (
                f"seed={seed}: obstacle too close to a drone/target ({d:.2f})"
            )


def test_obstacle_placement_never_raises_when_crowded():
    """A tiny world with many obstacles must degrade gracefully (fewer obstacles),
    never raise — matches the documented 'reduce K silently' behaviour."""
    env = MultiUAVEnv(n_drones=2, n_obstacles=50, world_size=30.0,
                       collision_radius=3.0, seed=0)
    env.reset()   # must not raise
    assert len(env.obstacle_pos) <= 50
