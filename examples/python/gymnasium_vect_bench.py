#####################################################################
# Test and benchmark the vectorization of VizDoom in gymnasium
#####################################################################

import argparse
import time
import warnings

import gymnasium


warnings.filterwarnings("ignore")
parser = argparse.ArgumentParser()
parser.add_argument("--n_envs", type=int, default=1, help="Number of envs")
args = parser.parse_args()
seed = 42
n_episodes = 1000

# Pick an environment VizdoomCorridor-v0
envs = gymnasium.make_vec(
    "VizdoomCorridor-v0", num_envs=args.n_envs, vectorization_mode="async"
)

# Time it
start = time.time()

observation, info = envs.reset()
for _ in range(n_episodes):
    # No learning here, for purposes of benchmarks
    actions = envs.action_space.sample()
    observations, rewards, terminations, truncations, infos = envs.step(actions)
    # env reset here slows it down
    # if terminated or truncated:
    #    observation, info = env.reset()
print(f"{args.n_envs}  {n_episodes *args.n_envs /round(time.time() - start,1)}")
envs.close()
