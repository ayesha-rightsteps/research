"""
Run this file to watch a random-action episode in the 2D UAV environment.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from environment.multi_uav_env import MultiUAVEnv
from environment.rendering import run_episode

env = MultiUAVEnv(n_drones=3, n_obstacles=4, seed=7)
run_episode(env, policy=None, max_steps=200, title="Multi-UAV Environment — Random Actions")
