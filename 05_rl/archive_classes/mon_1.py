import gymnasium as gym
import math
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.env_util import make_vec_env

class CartPoleCenterWrapper(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)
        
    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        
        cart_position = obs[0]
        pole_angle = obs[2]
        
        custom_reward = 1 - abs(pole_angle)/math.pi - abs(cart_position)/4.8
        return obs, custom_reward, terminated, truncated, info

env_id = "CartPole-v1"
num_env = 2
num_timesteps = 100_000

# create single environment
env = gym.make(env_id)

##############################################
# this is already provided by the library
# def make_env(env_id, rank, seed):
#     def init():
#         env = gym.make(env_id)
#         env = CartPoleCenterWrapper(env)
#         env = Monitor(env)
#         env.reset(seed=rank + seed)
#         return env
#     return init

# env_fns = [make_env(env_id, i) for i in range(num_env)]
# env_vec = DummyVecEnv(env_fns)
##############################################

# create vectorized environment
env_vec = make_vec_env(env_id=env_id, n_envs=num_env, vec_env_cls=DummyVecEnv)

model = PPO("MlpPolicy", env_vec, verbose=1, tensorboard_log="mon_log")
model.learn(total_timesteps=num_timesteps)
env_vec.close()


env = gym.make(env_id, render_mode="human")
obs, info = env.reset()

for _ in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    
    if (terminated or truncated):
        env.reset()

env.close()

# terminal with conda env activated:
# tensorboard --logdir "path"