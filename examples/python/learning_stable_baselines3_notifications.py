#!/usr/bin/env python3
#####################################################################
# Example script of training agents with stable-baselines3
# on ViZDoom using the Gymnasium API
#
# Note: For this example to work, you need to install stable-baselines3 and opencv:
#       pip install stable-baselines3 opencv-python
#
# See more stable-baselines3 documentation here:
#   https://stable-baselines3.readthedocs.io/en/master/index.html
#####################################################################

from argparse import ArgumentParser
from pathlib import Path

import cv2
import gymnasium
import numpy as np
from stable_baselines3.common.env_util import make_vec_env

import vizdoom.gymnasium_wrapper  # noqa
from export_notification_plots import (
    export_tensorboard_band_plots,
    export_tensorboard_images,
)
from sklearn.feature_extraction.text import HashingVectorizer


DEFAULT_ENV = "VizdoomBasicNotifications-v1"
DEFAULT_ENV_OFF = "VizdoomBasicNotificationsOff-v1"
AVAILABLE_ENVS = [env for env in gymnasium.envs.registry.keys() if "Vizdoom" in env]  # type: ignore

# Height and width of the resized image
IMAGE_SHAPE = (60, 80)

# Training parameters
TRAINING_TIMESTEPS = int(1e6)
N_STEPS = 512
N_ENVS = 1
FRAME_SKIP = 4


class ObservationWrapper(gymnasium.ObservationWrapper):
    """
    ViZDoom environments return dictionaries as observations, containing
    the main image as well other info.
    The image is also too large for normal training.

    This wrapper replaces the dictionary observation space with a simple
    Box space (i.e., only the RGB image), and also resizes the image to a
    smaller size.

    NOTE: Ideally, you should set the image size to smaller in the scenario files
          for faster running of ViZDoom. This can really impact performance,
          and this code is pretty slow because of this!
    """

    def __init__(self, env, shape=IMAGE_SHAPE):
        super().__init__(env)
        self.image_shape = shape
        self.image_shape_reverse = shape[::-1]
        self.n_features = 256
        self.vectorizer = HashingVectorizer(n_features=self.n_features)

        # Create new observation space with the new shape
        num_channels = env.observation_space["screen"].shape[-1]
        new_shape = (shape[0], shape[1], num_channels)

        # Get audio observation space if available
        if "audio" in env.observation_space.spaces:
            self.observation_space = gymnasium.spaces.Dict(
                {
                    "screen": gymnasium.spaces.Box(
                        0, 255, shape=new_shape, dtype=np.uint8
                    ),
                    "audio": env.observation_space["audio"],
                }
            )
        elif "notifications" in env.observation_space.spaces:
            self.observation_space = gymnasium.spaces.Dict(
                {
                    "screen": gymnasium.spaces.Box(
                        0, 255, shape=new_shape, dtype=np.uint8
                    ),
                    "notifications": gymnasium.spaces.Box(
                        low=-np.inf,
                        high=np.inf,
                        shape=(self.n_features,),
                        dtype=np.float32,
                    )
                    # "notifications": env.observation_space["notifications"]
                }
            )
        else:
            self.observation_space = gymnasium.spaces.Dict(
                {
                    "screen": gymnasium.spaces.Box(
                        0, 255, shape=new_shape, dtype=np.uint8
                    )
                }
            )

    def observation(self, observation):
        if "audio" in self.observation_space.spaces:
            observation = {
                "screen": cv2.resize(observation["screen"], self.image_shape_reverse),
                "audio": observation["audio"],
            }
        elif "notifications" in self.observation_space.spaces:
            notif = observation["notifications"]
            if isinstance(notif, str):
                notif_vector = (
                    self.vectorizer.fit_transform([notif])
                    .toarray()
                    .astype(np.float32)[0]
                )
            else:
                notif_vector = notif
            observation = {
                "screen": cv2.resize(observation["screen"], self.image_shape_reverse),
                "notifications": notif_vector,
            }
        else:
            observation = {
                "screen": cv2.resize(observation["screen"], self.image_shape_reverse)
            }
        return observation


def run_random_actions(envs, steps: int, n_envs: int) -> None:
    envs.reset()
    for _ in range(steps):
        actions = np.array([envs.action_space.sample() for _ in range(n_envs)])
        envs.step(actions)


def build_envs(args, env_name: str):
    # Create multiple environments: this speeds up training with PPO
    # We apply two wrappers on the environment:
    #  1) The above wrapper that modifies the observations (takes only the image and resizes it)
    #  2) A reward scaling wrapper. Normally the scenarios use large magnitudes for rewards (e.g., 100, -100).
    #     This may lead to unstable learning, and we scale the rewards by 1/100
    def wrap_env(env):
        env = ObservationWrapper(env)
        env = gymnasium.wrappers.TransformReward(env, lambda r: r * 0.01)
        return env

    envs = make_vec_env(
        env_name,
        n_envs=args.n_envs,
        wrapper_class=wrap_env,
        env_kwargs=dict(frame_skip=FRAME_SKIP),
    )
    return envs


def train_agent(args, env_name: str, exp_name: str) -> None:
    envs = build_envs(args, env_name)
    if args.random_actions:
        run_random_actions(envs, args.random_steps, args.n_envs)
        return

    from stable_baselines3 import PPO

    agent = PPO(
        "MultiInputPolicy",
        envs,
        n_steps=N_STEPS,
        verbose=2,
        tensorboard_log=f"{args.dir}",
    )

    # Do the actual learning
    # This will print out the results in the console.
    # If agent gets better, "ep_rew_mean" should increase steadily
    total_timesteps = args.timesteps if args.timesteps is not None else TRAINING_TIMESTEPS
    try:
        agent.learn(
            total_timesteps=total_timesteps,
            tb_log_name=exp_name,
            progress_bar=True,
        )
    except ImportError:
        agent.learn(total_timesteps=total_timesteps)


def main(args):
    if args.compare_notifications:
        notif_on_prefixes = []
        notif_off_prefixes = []
        for trial in range(args.trials):
            exp_on = f"{args.exp}_notif_on_trial{trial}"
            exp_off = f"{args.exp}_notif_off_trial{trial}"
            train_agent(args, args.env_on, exp_on)
            train_agent(args, args.env_off, exp_off)
            notif_on_prefixes.append(exp_on)
            notif_off_prefixes.append(exp_off)

        images_dir = (
            Path(args.images_dir) if args.images_dir else Path(args.dir) / "images"
        )
        export_tensorboard_band_plots(
            Path(args.dir),
            {
                "Notifications on": notif_on_prefixes,
                "Notifications off": notif_off_prefixes,
            },
            images_dir,
            args.image_format,
        )
        return

    train_agent(args, args.env, args.exp)
    images_dir = (
        Path(args.images_dir) if args.images_dir else Path(args.dir) / "images"
    )
    export_tensorboard_images(
        Path(args.dir),
        args.exp,
        images_dir,
        args.image_format,
    )


if __name__ == "__main__":
    parser = ArgumentParser("Train stable-baselines3 PPO agents on ViZDoom.")
    parser.add_argument(
        "--env",
        default=DEFAULT_ENV,
        choices=AVAILABLE_ENVS,
        help="Name of the environment to play",
    )
    parser.add_argument(
        "--env-on",
        default=DEFAULT_ENV,
        choices=AVAILABLE_ENVS,
        help="Name of the notifications-on environment",
    )
    parser.add_argument(
        "--env-off",
        default=DEFAULT_ENV_OFF,
        choices=AVAILABLE_ENVS,
        help="Name of the notifications-off environment",
    )
    parser.add_argument("--dir", default="./logs/")
    parser.add_argument("--exp", default="Notif")
    parser.add_argument("--n-envs", type=int, default=N_ENVS)
    parser.add_argument("--images-dir")
    parser.add_argument("--image-format", default="pdf")
    parser.add_argument("--trials", type=int, default=4)
    parser.add_argument("--timesteps", type=int)
    parser.add_argument("--random-actions", action="store_true")
    parser.add_argument("--random-steps", type=int, default=1000)
    parser.add_argument("--compare-notifications", action="store_true")
    args = parser.parse_args()
    main(args)
