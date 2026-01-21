#!/usr/bin/env python3
#####################################################################
# Train PPO with stable-baselines3 on ViZDoom notifications and
# record/play back evaluation videos.
#####################################################################

from argparse import ArgumentParser
from pathlib import Path

import cv2
import gymnasium
from stable_baselines3.common.env_util import make_vec_env

import vizdoom.gymnasium_wrapper  # noqa
from learning_stable_baselines3_notifications import (
    FRAME_SKIP,
    ObservationWrapper,
    TRAINING_TIMESTEPS,
)


DEFAULT_ENV = "VizdoomBasicNotifications-v1"


def wrap_env(env):
    env = ObservationWrapper(env)
    env = gymnasium.wrappers.TransformReward(env, lambda r: r * 0.01)
    return env


def train_agent(args):
    envs = make_vec_env(
        args.env,
        n_envs=args.n_envs,
        wrapper_class=wrap_env,
        env_kwargs=dict(frame_skip=FRAME_SKIP),
    )

    from stable_baselines3 import PPO

    agent = PPO(
        "MultiInputPolicy",
        envs,
        n_steps=args.n_steps,
        verbose=2,
        tensorboard_log=args.log_dir,
    )
    total_timesteps = (
        args.timesteps if args.timesteps is not None else TRAINING_TIMESTEPS
    )
    try:
        agent.learn(
            total_timesteps=total_timesteps,
            tb_log_name=args.exp,
            progress_bar=True,
        )
    except ImportError:
        agent.learn(total_timesteps=total_timesteps)
    envs.close()
    return agent


def record_eval_videos(args, agent) -> list[Path]:
    env = gymnasium.make(
        args.env,
        render_mode="rgb_array",
        frame_skip=FRAME_SKIP,
    )
    env = wrap_env(env)
    video_dir = Path(args.video_dir)
    video_dir.mkdir(parents=True, exist_ok=True)
    env = gymnasium.wrappers.RecordVideo(
        env,
        video_folder=str(video_dir),
        name_prefix=args.exp,
        episode_trigger=lambda episode_id: True,
    )

    episode_rewards = []
    for _ in range(args.eval_episodes):
        obs, _ = env.reset()
        done = False
        truncated = False
        total_reward = 0.0
        while not (done or truncated):
            action, _ = agent.predict(obs, deterministic=False)
            obs, reward, done, truncated, _ = env.step(action)
            total_reward += float(reward)
        episode_rewards.append(total_reward)

    env.close()
    mean_reward = sum(episode_rewards) / max(len(episode_rewards), 1)
    print(f"Eval episodes: {len(episode_rewards)}, mean reward: {mean_reward:.3f}")
    return sorted(video_dir.glob(f"{args.exp}*.mp4"))


def playback_videos(video_paths: list[Path]) -> None:
    if not video_paths:
        print("No videos found to play back.")
        return
    for video_path in video_paths:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            print(f"Could not open video: {video_path}")
            continue
        window_name = f"Playback - {video_path.name}"
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow(window_name, frame)
            if cv2.waitKey(30) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyWindow(window_name)
    cv2.destroyAllWindows()


def main():
    parser = ArgumentParser("Train PPO and record/playback eval videos.")
    parser.add_argument(
        "--env",
        default=DEFAULT_ENV,
        choices=[env for env in gymnasium.envs.registry.keys() if "Vizdoom" in env],  # type: ignore
        help="Name of the environment to play",
    )
    parser.add_argument("--n-envs", type=int, default=1)
    parser.add_argument("--n-steps", type=int, default=512)
    parser.add_argument("--timesteps", type=int)
    parser.add_argument("--log-dir", default="./logs/")
    parser.add_argument("--exp", default="NotifVideo")
    parser.add_argument("--video-dir", default="./videos/")
    parser.add_argument("--eval-episodes", type=int, default=3)
    parser.add_argument("--no-playback", action="store_true")
    args = parser.parse_args()

    agent = train_agent(args)
    video_paths = record_eval_videos(args, agent)
    if not args.no_playback:
        playback_videos(video_paths)


if __name__ == "__main__":
    main()
