import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation


DRONE_COLOR    = ["#2196F3", "#E91E63", "#4CAF50", "#FF9800", "#9C27B0",
                   "#00BCD4", "#FF5722", "#607D8B"]
TARGET_COLOR   = ["#1565C0", "#880E4F", "#1B5E20", "#E65100", "#4A148C",
                   "#006064", "#BF360C", "#37474F"]
OBSTACLE_COLOR = "#757575"
BG_COLOR       = "#F5F5F5"
GRID_COLOR     = "#E0E0E0"


def run_episode(env, policy=None, max_steps=300, interval_ms=80, title="UAV Episode"):
    """
    Animate one episode.
    policy: callable(obs) -> actions. If None, uses random actions.
    """
    obs, _ = env.reset()
    world  = env.world_size
    n      = env.n_drones

    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, world)
    ax.set_ylim(0, world)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # Grid
    for x in range(0, int(world) + 1, 10):
        ax.axvline(x, color=GRID_COLOR, linewidth=0.5)
    for y in range(0, int(world) + 1, 10):
        ax.axhline(y, color=GRID_COLOR, linewidth=0.5)

    # Obstacles (drawn once — they don't move)
    for obs_pos in env.obstacle_pos:
        circle = plt.Circle(obs_pos, env.collision_radius,
                             color=OBSTACLE_COLOR, alpha=0.6, zorder=2)
        ax.add_patch(circle)
    ax.plot([], [], "s", color=OBSTACLE_COLOR, alpha=0.6, label="Obstacle")

    # Targets
    target_markers = []
    for j in range(n):
        m, = ax.plot(*env.target_pos[j], "*", markersize=16,
                     color=TARGET_COLOR[j % len(TARGET_COLOR)],
                     zorder=3, label=f"Target {j+1}")
        target_markers.append(m)

    # Drones
    drone_markers = []
    drone_trails  = [[] for _ in range(n)]
    trail_lines   = []
    for i in range(n):
        m, = ax.plot(*env.drone_pos[i], "o", markersize=12,
                     color=DRONE_COLOR[i % len(DRONE_COLOR)],
                     zorder=5, label=f"Drone {i+1}")
        drone_markers.append(m)
        line, = ax.plot([], [], "-", color=DRONE_COLOR[i % len(DRONE_COLOR)],
                        alpha=0.35, linewidth=1.5, zorder=4)
        trail_lines.append(line)

    # Assignment lines (drone → its target)
    assign_lines = []
    for i in range(n):
        line, = ax.plot([], [], "--", linewidth=1,
                        color=DRONE_COLOR[i % len(DRONE_COLOR)],
                        alpha=0.4, zorder=3)
        assign_lines.append(line)

    # Info text
    step_text  = ax.text(1, world - 3, "", fontsize=10, color="#333333")
    status_text = ax.text(world / 2, world + 2, "", fontsize=11,
                          color="#333333", ha="center", fontweight="bold",
                          transform=ax.transData, clip_on=False)

    ax.legend(loc="upper right", fontsize=8, framealpha=0.85)

    state = {"obs": obs, "done": False, "result": ""}

    def update(_frame):
        if state["done"]:
            return

        if policy is not None:
            actions = policy(state["obs"])
        else:
            actions = env.action_space.sample()

        state["obs"], _rewards, terminated, truncated, info = env.step(actions)

        # Update drone positions and trails
        for i in range(n):
            pos = env.drone_pos[i]
            drone_markers[i].set_data([pos[0]], [pos[1]])
            drone_trails[i].append(pos.copy())
            if len(drone_trails[i]) > 40:
                drone_trails[i].pop(0)
            trail = np.array(drone_trails[i])
            trail_lines[i].set_data(trail[:, 0], trail[:, 1])

            # Assignment line: drone → assigned target
            t_idx = env.assignment[i]
            tpos  = env.target_pos[t_idx]
            assign_lines[i].set_data(
                [pos[0], tpos[0]], [pos[1], tpos[1]]
            )

        step_text.set_text(f"Step: {info['step']}")

        if terminated or truncated:
            state["done"] = True
            if info["all_targets_reached"]:
                state["result"] = "SUCCESS — all targets reached!"
                status_text.set_color("#2E7D32")
            elif info["any_collision"]:
                state["result"] = "COLLISION!"
                status_text.set_color("#C62828")
            else:
                state["result"] = "Time out."
                status_text.set_color("#E65100")
            status_text.set_text(state["result"])

    anim = FuncAnimation(fig, update, frames=max_steps,
                         interval=interval_ms, repeat=False)
    plt.tight_layout()
    plt.show()
    return anim
