#!/usr/bin/env python3
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional

import numpy as np
from tensorboard.backend.event_processing import event_accumulator


def find_latest_tb_run(
    log_dir: Path, exp_name: str, suffix: Optional[str] = None
) -> Optional[Path]:
    if not log_dir.exists():
        return None
    candidates = [
        path
        for path in log_dir.iterdir()
        if path.is_dir()
        and path.name.startswith(exp_name)
        and (suffix is None or path.name.endswith(suffix))
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def moving_average(values: np.ndarray, window: int) -> np.ndarray:
    if window <= 1:
        return values
    if window > len(values):
        window = len(values)
    kernel = np.ones(window, dtype=np.float32) / window
    return np.convolve(values, kernel, mode="same")


def exponential_moving_average(values: np.ndarray, alpha: float) -> np.ndarray:
    if alpha <= 0.0 or alpha >= 1.0:
        return values
    ema = np.empty_like(values, dtype=np.float32)
    ema[0] = values[0]
    for idx in range(1, len(values)):
        ema[idx] = alpha * ema[idx - 1] + (1.0 - alpha) * values[idx]
    return ema


def parse_int_list(raw: str) -> list[int]:
    if not raw:
        return []
    values = []
    for item in raw.split(","):
        item = item.strip()
        if item:
            values.append(int(item))
    return values


def load_scalar_runs(
    log_dir: Path, run_prefixes: list[str], tag: str, suffix: Optional[str] = None
) -> list[tuple[list[int], list[float]]]:
    runs = []
    for prefix in run_prefixes:
        run_dir = find_latest_tb_run(log_dir, prefix, suffix=suffix)
        if run_dir is None:
            continue
        accumulator = event_accumulator.EventAccumulator(
            str(run_dir),
            size_guidance={"scalars": 0},
        )
        accumulator.Reload()
        events = accumulator.Scalars(tag)
        if not events:
            continue
        steps = [event.step for event in events]
        values = [event.value for event in events]
        runs.append((steps, values))
    return runs


def aggregate_runs(
    runs: list[tuple[list[int], list[float]]]
) -> Optional[tuple[list[int], np.ndarray, np.ndarray]]:
    if not runs:
        return None
    step_sets = [set(steps) for steps, _ in runs]
    common_steps = sorted(set.intersection(*step_sets))
    if not common_steps:
        return None
    values_matrix = []
    for steps, values in runs:
        step_to_value = dict(zip(steps, values))
        values_matrix.append([step_to_value[step] for step in common_steps])
    values_array = np.array(values_matrix, dtype=np.float32)
    mean = values_array.mean(axis=0)
    std = values_array.std(axis=0)
    return common_steps, mean, std


def export_tensorboard_images(
    log_dir: Path, exp_name: str, output_dir: Path, image_format: str
) -> None:
    run_dir = find_latest_tb_run(log_dir, exp_name)
    if run_dir is None:
        return

    accumulator = event_accumulator.EventAccumulator(
        str(run_dir),
        size_guidance={"scalars": 0},
    )
    accumulator.Reload()
    scalar_tags = set(accumulator.Tags().get("scalars", []))

    tag_map = {
        "mean_reward": "rollout/ep_rew_mean",
        "eps_len": "rollout/ep_len_mean",
        "time_fps": "time/fps",
    }

    output_dir.mkdir(parents=True, exist_ok=True)

    def apply_pub_style() -> None:
        import matplotlib.pyplot as plt

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
            }
        )

    for filename, tag in tag_map.items():
        if tag not in scalar_tags:
            continue
        events = accumulator.Scalars(tag)
        steps = [event.step for event in events]
        values = [event.value for event in events]

        import matplotlib.pyplot as plt

        apply_pub_style()
        plt.figure()
        plt.plot(steps, values)
        plt.title(tag)
        plt.xlabel("step")
        plt.ylabel(tag)
        plt.tight_layout()
        plt.savefig(output_dir / f"{filename}.{image_format}")
        plt.close()


def export_tensorboard_band_plots(
    log_dir: Path,
    exp_prefixes: dict[str, list[str]],
    output_dir: Path,
    image_format: str,
    smooth_window: int = 1,
    smooth_alpha: Optional[float] = None,
    run_suffix: Optional[str] = None,
) -> None:
    import matplotlib.pyplot as plt

    def apply_pub_style() -> None:
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
            }
        )

    tag_map = {
        "mean_reward": "rollout/ep_rew_mean",
        "eps_len": "rollout/ep_len_mean",
        "time_fps": "time/fps",
    }

    palette = {
        "Notifications on": "#1f77b4",
        "Notifications off": "#d62728",
    }

    output_dir.mkdir(parents=True, exist_ok=True)

    for filename, tag in tag_map.items():
        plt.figure()
        apply_pub_style()
        has_any = False
        for label, prefixes in exp_prefixes.items():
            runs = load_scalar_runs(log_dir, prefixes, tag, suffix=run_suffix)
            aggregate = aggregate_runs(runs)
            if aggregate is None:
                continue
            steps, mean, std = aggregate
            mean = moving_average(mean, smooth_window)
            std = moving_average(std, smooth_window)
            if smooth_alpha is not None:
                mean = exponential_moving_average(mean, smooth_alpha)
                std = exponential_moving_average(std, smooth_alpha)
            color = palette.get(label)
            plt.plot(steps, mean, label=label, color=color)
            plt.fill_between(
                steps,
                mean - std,
                mean + std,
                color=color,
                alpha=0.2,
            )
            has_any = True
        if not has_any:
            plt.close()
            continue
        plt.title(tag)
        plt.xlabel("step")
        plt.ylabel(tag)
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_dir / f"{filename}.{image_format}")
        plt.close()


def main() -> None:
    parser = ArgumentParser("Export smoothed TensorBoard band plots.")
    parser.add_argument("--log-dir", default="./logs/")
    parser.add_argument("--output-dir")
    parser.add_argument("--image-format", default="pdf")
    parser.add_argument("--exp", default="Notif")
    parser.add_argument("--trials", type=int, default=4)
    parser.add_argument("--trial-ids", default="")
    parser.add_argument("--run-suffix", default="")
    parser.add_argument("--smooth-window", type=int, default=1)
    parser.add_argument("--smooth-alpha", type=float)
    parser.add_argument("--label-on", default="Notifications on")
    parser.add_argument("--label-off", default="Notifications off")
    args = parser.parse_args()

    log_dir = Path(args.log_dir)
    output_dir = Path(args.output_dir) if args.output_dir else log_dir / "images"
    trial_ids = parse_int_list(args.trial_ids)
    if not trial_ids:
        trial_ids = list(range(args.trials))
    notif_on_prefixes = [f"{args.exp}_notif_on_trial{trial}" for trial in trial_ids]
    notif_off_prefixes = [f"{args.exp}_notif_off_trial{trial}" for trial in trial_ids]

    export_tensorboard_band_plots(
        log_dir,
        {
            args.label_on: notif_on_prefixes,
            args.label_off: notif_off_prefixes,
        },
        output_dir,
        args.image_format,
        smooth_window=args.smooth_window,
        smooth_alpha=args.smooth_alpha,
        run_suffix=args.run_suffix if args.run_suffix else None,
    )


if __name__ == "__main__":
    main()
