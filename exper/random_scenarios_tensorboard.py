#!/usr/bin/env python3

from __future__ import annotations

from argparse import ArgumentParser
from collections import deque
from pathlib import Path
from time import perf_counter

import gymnasium
from tensorboard.backend.event_processing import event_accumulator
from torch.utils.tensorboard import SummaryWriter

import vizdoom.gymnasium_wrapper  # noqa: F401


def export_tensorboard_pngs(log_dir: Path, output_dir: Path) -> None:
    accumulator = event_accumulator.EventAccumulator(
        str(log_dir),
        size_guidance={"scalars": 0},
    )
    accumulator.Reload()
    scalar_tags = set(accumulator.Tags().get("scalars", []))

    tag_map = {
        "mean_reward": {
            "tag": "rollout/ep_rew_mean",
            "title": "Mean Episode Reward",
            "ylabel": "Reward",
        },
        "eps_len": {
            "tag": "rollout/ep_len_mean",
            "title": "Mean Episode Length",
            "ylabel": "Steps",
        },
        "time_fps": {
            "tag": "time/fps",
            "title": "Throughput",
            "ylabel": "FPS",
        },
    }

    output_dir.mkdir(parents=True, exist_ok=True)

    def apply_pub_style() -> None:
        import matplotlib.pyplot as plt

        background = "#f6f6f2"
        try:
            plt.style.use("seaborn-v0_8-whitegrid")
        except OSError:
            plt.style.use("seaborn-whitegrid")
        plt.rcParams.update(
            {
                "figure.figsize": (6.0, 4.0),
                "figure.dpi": 200,
                "savefig.dpi": 300,
                "font.size": 11,
                "axes.titlesize": 12,
                "axes.labelsize": 11,
                "lines.linewidth": 2.0,
                "axes.spines.top": False,
                "axes.spines.right": False,
                "grid.alpha": 0.3,
                "figure.facecolor": background,
                "axes.facecolor": background,
            }
        )

    for filename, meta in tag_map.items():
        tag = meta["tag"]
        if tag not in scalar_tags:
            continue
        events = accumulator.Scalars(tag)
        steps = [event.step for event in events]
        values = [event.value for event in events]

        import matplotlib.pyplot as plt

        apply_pub_style()
        plt.figure()
        plt.plot(steps, values)
        plt.title(meta["title"])
        plt.xlabel("Environment steps")
        plt.ylabel(meta["ylabel"])
        plt.tight_layout()
        plt.savefig(output_dir / f"{filename}.png", facecolor=plt.rcParams["figure.facecolor"])
        plt.close()


def main() -> None:
    parser = ArgumentParser("Run random actions and log TensorBoard metrics.")
    parser.add_argument("--env", required=True)
    parser.add_argument("--log-dir", required=True)
    parser.add_argument("--images-dir", required=True)
    parser.add_argument("--combined-log-dir")
    parser.add_argument("--tag-prefix")
    parser.add_argument("--episodes", type=int, default=10)
    parser.add_argument("--window", type=int, default=10)
    args = parser.parse_args()

    log_dir = Path(args.log_dir)
    images_dir = Path(args.images_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    env = gymnasium.make(args.env)
    writer = SummaryWriter(log_dir=str(log_dir))
    combined_writer = None
    if args.combined_log_dir:
        combined_writer = SummaryWriter(log_dir=str(Path(args.combined_log_dir)))

    reward_window = deque(maxlen=args.window)
    length_window = deque(maxlen=args.window)

    total_steps = 0
    start_time = perf_counter()

    obs, _ = env.reset()
    for _ in range(args.episodes):
        episode_reward = 0.0
        episode_length = 0

        terminated = False
        truncated = False
        while not (terminated or truncated):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, _ = env.step(action)
            episode_reward += float(reward)
            episode_length += 1
            total_steps += 1

        reward_window.append(episode_reward)
        length_window.append(episode_length)

        mean_reward = sum(reward_window) / len(reward_window)
        mean_length = sum(length_window) / len(length_window)
        elapsed = max(perf_counter() - start_time, 1e-6)
        fps = total_steps / elapsed

        writer.add_scalar("rollout/ep_rew_mean", mean_reward, total_steps)
        writer.add_scalar("rollout/ep_len_mean", mean_length, total_steps)
        writer.add_scalar("time/fps", fps, total_steps)
        if combined_writer:
            tag_prefix = args.tag_prefix or args.env
            combined_writer.add_scalar(
                f"{tag_prefix}/rollout/ep_rew_mean", mean_reward, total_steps
            )
            combined_writer.add_scalar(
                f"{tag_prefix}/rollout/ep_len_mean", mean_length, total_steps
            )
            combined_writer.add_scalar(f"{tag_prefix}/time/fps", fps, total_steps)

        obs, _ = env.reset()

    writer.flush()
    writer.close()
    if combined_writer:
        combined_writer.flush()
        combined_writer.close()
    env.close()

    export_tensorboard_pngs(log_dir, images_dir)


if __name__ == "__main__":
    main()
