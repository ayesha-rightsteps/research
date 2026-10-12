"""
test_env_v4.py -- Step 1 gate for v4 Phase 1b (PLAN: v4/02-redesign/PLAN.md, Section 6).
Run:  python test_env_v4.py   (or pytest test_env_v4.py)
Every test compares against a value computed by hand, or against the frozen v3 environment.
"""
import numpy as np

import env_v4 as E
import v3_env as V3

R = E.OBS_RADIUS


def test_ray_hits_disc_surface_exactly():
    d = E.ray_distances(np.array([100.0, 100.0]), np.array([[150.0, 100.0]]), R, 500.0)
    assert abs(d[0] - (50.0 - R)) < 1e-9, d[0]            # ray 0 (east): 50 - 12 = 38
    assert abs(d[12] - E.RAY_RANGE) < 1e-9                  # ray 12 (west): nothing within range


def test_ray_misses_disc_and_returns_range():
    d = E.ray_distances(np.array([100.0, 100.0]), np.array([[150.0, 140.0]]), R, 500.0)   # disc spans y 128..152
    assert abs(d[0] - E.RAY_RANGE) < 1e-9, d[0]


def test_ray_stops_at_wall():
    d = E.ray_distances(np.array([480.0, 100.0]), np.zeros((0, 2)), R, 500.0)
    assert abs(d[0] - 20.0) < 1e-9 and abs(d[6] - E.RAY_RANGE) < 1e-9   # east wall 20 away; north 400 -> capped


def test_diagonal_ray_against_hand_calculation():
    pos, c = np.array([100.0, 100.0]), np.array([[130.0, 130.0]])
    k = 3                                                  # 45 degrees
    expected = np.hypot(30.0, 30.0) - R                    # straight at the centre
    d = E.ray_distances(pos, c, R, 500.0)
    assert abs(d[k] - expected) < 1e-9, (d[k], expected)


def test_collision_boundary_is_obstacle_radius_plus_collision_radius():
    env = E.MultiUAVEnvV4(n_drones=2, n_obstacles=0, seed=0)
    env.reset()
    env.obstacle_pos = np.array([[250.0, 250.0]], dtype=np.float32)
    env.drone_pos = np.array([[250.0 + R + env.col_r, 250.0], [50.0, 50.0]], dtype=np.float32)
    assert env._collision_kind() == ''                     # exactly on the boundary: no collision
    env.drone_pos[0, 0] = 250.0 + R + env.col_r - 0.01
    assert env._collision_kind() == 'drone-obstacle'
    env.drone_pos = np.array([[100.0, 100.0], [100.0 + env.col_r - 0.01, 100.0]], dtype=np.float32)
    assert env._collision_kind() == 'drone-drone'


def test_time_to_disc_matches_hand_calculation():
    boundary = R + 3.0
    c = np.array([[125.0, 100.0]])
    t = E.time_to_disc(np.array([100.0, 100.0]), np.array([5.0, 0.0]), c, boundary)
    assert abs(t - (25.0 - boundary) / 5.0) < 1e-9, t      # (25 - 15) / 5 = 2 steps
    t_far = E.time_to_disc(np.array([100.0, 100.0]), np.array([5.0, 0.0]), np.array([[200.0, 100.0]]), boundary)
    assert t_far == E.TAU_HORIZON                          # 17 steps away -> capped at 3
    t_away = E.time_to_disc(np.array([100.0, 100.0]), np.array([-5.0, 0.0]), c, boundary)
    assert t_away == E.TAU_HORIZON
    t_still = E.time_to_disc(np.array([100.0, 100.0]), np.array([0.0, 0.0]), c, boundary)
    assert t_still == E.TAU_HORIZON
    t_inside = E.time_to_disc(np.array([112.0, 100.0]), np.array([1.0, 0.0]), c, boundary)
    assert t_inside == 0.0


def test_hazard_tau_is_min_of_drone_and_obstacle():
    env = E.MultiUAVEnvV4(n_drones=3, n_obstacles=20, seed=1)
    env.reset()
    rng = np.random.default_rng(0)
    for _ in range(200):
        _, _, term, trunc, info = env.step(rng.uniform(-5, 5, (3, 2)))
        assert np.allclose(info['pah_inputs']['tau'], np.minimum(info['tau_drone'], info['tau_obstacle']))
        assert (info['pah_inputs']['tau'] <= E.TAU_HORIZON + 1e-6).all() and (info['pah_inputs']['tau'] >= 0).all()
        if term or trunc:
            env.reset()


def test_discs_keep_clear_of_starts_and_targets():
    for seed in range(50):
        env = E.MultiUAVEnvV4(n_drones=8, n_obstacles=40, seed=seed)
        env.reset()
        pts = np.concatenate([env.drone_pos, env.target_pos])
        d = np.linalg.norm(pts[:, None, :] - env.obstacle_pos[None, :, :], axis=-1)
        assert d.min() >= R + env.col_r + 5.0 - 1e-4
        dd = np.linalg.norm(env.obstacle_pos[:, None] - env.obstacle_pos[None], axis=-1) + np.eye(40) * 1e9
        assert dd.min() >= 2 * R + 2.0 - 1e-4


def test_targets_never_inside_a_disc():
    env = E.MultiUAVEnvV4(n_drones=8, n_obstacles=40, target_speed=1.0, seed=3)
    env.reset()
    zero = np.zeros((8, 2))
    for _ in range(2000):                                  # drones stand still; only targets move
        env.t = 0                                          # keep the episode from timing out
        env.step(zero)
        d = np.linalg.norm(env.target_pos[:, None, :] - env.obstacle_pos[None, :, :], axis=-1)
        assert d.min() >= R - 1e-3, d.min()


def test_same_seed_same_episode():
    def roll(seed):
        env = E.MultiUAVEnvV4(n_drones=5, n_obstacles=20, seed=seed)
        o = env.reset(); rng = np.random.default_rng(7); out = [o.copy()]
        for _ in range(100):
            o, r, te, tr, _ = env.step(rng.uniform(-5, 5, (5, 2))); out.append(o.copy())
            if te or tr:
                o = env.reset(); out.append(o.copy())
        return np.array(out)
    assert np.array_equal(roll(11), roll(11))
    assert not np.array_equal(roll(11), roll(12))


def test_observation_shape_and_ranges():
    env = E.MultiUAVEnvV4(n_drones=8, n_obstacles=40, seed=5)
    o = env.reset()
    assert o.shape == (8, 50) and E.OBS_DIM == 50
    rays = o[:, E.BASE_DIM:E.BASE_DIM + E.N_RAYS]
    assert (rays >= 0).all() and (rays <= 1).all()


def test_no_obstacles_matches_v3_exactly():
    """With zero obstacles nothing of the v3 behaviour may change: same starts, assignment, rewards,
    termination and neighbour features for the same actions (the LiDAR / clearance part of the observation
    differs by design and is excluded)."""
    rng = np.random.default_rng(0)
    for seed in (1, 2, 3):
        a = V3.MultiUAVEnv(n_drones=5, n_obstacles=0, seed=seed)
        b = E.MultiUAVEnvV4(n_drones=5, n_obstacles=0, seed=seed)
        oa, ob = a.reset(), b.reset()
        assert np.array_equal(a.drone_pos, b.drone_pos) and np.array_equal(a.target_pos, b.target_pos)
        for _ in range(300):
            act = rng.uniform(-5, 5, (5, 2)).astype(np.float32)
            oa, ra, ta, tra, ia = a.step(act)
            ob, rb, tb, trb, ib = b.step(act)
            assert np.allclose(ra, rb) and ta == tb and tra == trb
            assert np.allclose(ia['r_mission'], ib['r_mission']) and np.allclose(ia['r_safety'], ib['r_safety'])
            assert np.array_equal(a.assignment, b.assignment)
            assert np.allclose(oa[:, :6], ob[:, :6])                       # pos, vel, target offset
            assert np.allclose(oa[:, 10:], ob[:, E.BASE_DIM + E.N_RAYS:])  # conflict-neighbour features
            assert np.allclose(ia['pah_inputs']['tau'], ib['pah_inputs']['tau'])   # no discs -> tau = tau_drone
            if ta or tra:
                oa, ob = a.reset(), b.reset()


def test_random_policy_many_episodes_no_errors():
    rng = np.random.default_rng(1)
    for n, m in ((5, 20), (8, 40)):
        env = E.MultiUAVEnvV4(n_drones=n, n_obstacles=m, seed=9)
        for ep in range(500):
            o = env.reset(); done = False
            while not done:
                o, r, te, tr, info = env.step(rng.uniform(-5, 5, (n, 2)))
                assert np.isfinite(o).all() and np.isfinite(r).all()
                done = te or tr
            if info['episode_collision']:
                assert info['collision_kind'] in ('drone-drone', 'drone-obstacle', 'both')


if __name__ == '__main__':
    import sys, time
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    failed = 0
    for t in tests:
        t0 = time.time()
        try:
            t(); print('PASS  {:55s} {:.1f}s'.format(t.__name__, time.time() - t0))
        except AssertionError as e:
            failed += 1; print('FAIL  {:55s} {}'.format(t.__name__, e))
    print('\n{} / {} passed'.format(len(tests) - failed, len(tests)))
    sys.exit(1 if failed else 0)
