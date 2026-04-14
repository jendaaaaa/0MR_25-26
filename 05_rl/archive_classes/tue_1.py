import gymnasium as gym
import stable_baselines3 as sb
from stable_baselines3.common.env_util import make_vec_env
import os

class CartPoleCenterWrapper(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)
        
    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        
        cart_position = obs[0]
        pole_angle = obs[2]
        
        custom_reward = 1 - abs(pole_angle)/0.418 - abs(cart_position)/4.8
        return obs, custom_reward, terminated, truncated, info

learn = False

env_id = "CartPole-v1"
model_name = "cartpole_ppo_center_2"
log_dir = model_name + "_logs"
num_timesteps = 40_000
num_envs = 4
is_new = False

# env = make_vec_env(env_id, n_envs=num_envs)
env = make_vec_env(env_id, n_envs=num_envs, wrapper_class=CartPoleCenterWrapper)
if os.path.exists(model_name + ".zip"):
    model = sb.PPO.load(model_name, env, verbose=1, tensorboard_log=log_dir)
else:
    model = sb.PPO("MlpPolicy", env, verbose=1, tensorboard_log=log_dir)
    is_new = True

if learn:
    model.learn(num_timesteps, reset_num_timesteps=is_new)
    model.save(model_name)
else:
    env = gym.make(env_id, render_mode="human")
    obs, info = env.reset()

    num_episodes_elapsed = 0
    while num_episodes_elapsed < 5:
        # action = env.action_space.sample()
        action, _state = model.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        
        if terminated or truncated:
            env.reset()
            num_episodes_elapsed += 1