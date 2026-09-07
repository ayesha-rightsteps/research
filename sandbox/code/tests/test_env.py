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
    """Observation must be (n_drones, 10) after reset."""
    env = MultiUAVEnv(n_drones=3, n_obstacles=3, seed=0)
    obs, _ = env.reset()
    assert obs.shape == (3, 10), f"Expected (3,10), got {obs.shape}"


def test_reset_gives_valid_positions():
    """After reset, all drones and targets must be inside the world."""
    env = MultiUAVEnv(n_drones=3, n_obstacles=3, seed=1)
    env.reset()
    assert np.all(env.drone_pos >= 0) and np.all(env.drone_pos <= env.world_size)
    assert np.all(env.target_pos >= 0) and np.all(env.target_pos <= env.world_size)


def test_step_returns_correct_shapes():
    """step() must return obs, rewards, terminated, truncated, info with right shapes."""
    env = MultiUAVEnv(n_drones=3, n_obstacles=3, seed=2)
    env.reset()
    actions = env.action_space.sample()
    obs, rewards, terminated, truncated, info = env.step(actions)
    assert obs.shape == (3, 10)
    assert rewards.shape == (3,)
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)


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
    """A drone on top of another must receive a negative reward."""
    env = MultiUAVEnv(n_drones=2, n_obstacles=0, seed=0)
    env.reset()
    env.drone_pos[0] = np.array([50.0, 50.0])
    env.drone_pos[1] = np.array([50.0, 50.0])
    env.drone_vel = np.zeros((2, 2))
    rewards = env._compute_rewards()
    assert rewards[0] < 0, "Collision should give negative reward"


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
