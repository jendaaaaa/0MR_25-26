# Setup Guide: Reinforcement Learning Class

This guide covers the installation of Miniconda and the specific libraries required for Stable Baselines3 and Gymnasium (Box2D environments) on Windows.

[![Watch the video](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://youtu.be/VIDEO_ID)

## 1. Install Miniconda
1. Download the installer from the [Miniconda Download Page](https://docs.conda.io/en/latest/miniconda.html).
2. Run the installer.
3. **Advanced Installation Options:**
   * **Option A (Recommended for Class):** Leave "Add Miniconda3 to my PATH" **unchecked**. This keeps your AI tools in a "Sandbox." You will use the **Anaconda Prompt** for class to keep your computer's system settings clean.
   * **Option B (For Long-term Use):** If you plan to use Conda daily after this class and want to access it from the standard Windows Command Prompt/PowerShell, you may **CHECK** this box.

## 2. Create the Environment
Open the Anaconda Prompt and run these commands one by one:

```Bash
# Create a virtual environment named 'rl_env'
conda create -n rl_env python=3.10 -y

# Activate the environment
conda activate rl_env
```

## 3. Install Dependencies
Copy and paste these commands into the Anaconda Prompt. These will install the physics engines and the RL frameworks.

```Bash
# Install SWIG (Required for Box2D on Windows)
conda install swig

# Install Gymnasium (Box2D) and Stable Baselines3
pip install "gymnasium[box2d]" "stable-baselines3[extra]"
```

## 4. Configure Visual Studio Code (VS Code)
To write and run our AI scripts, we need to tell VS Code to use the new sandbox we just created.

### Step A: Fix the Terminal (Windows Only)
By default, VS Code uses PowerShell, which often blocks Conda environments from activating properly. We need to switch it to Command Prompt.

1. Open VS Code.
2. Open the Command Palette: Press Ctrl + Shift + P.
3. Type Terminal: Select Default Profile and press Enter.
4. Select Command Prompt from the list.

### Step B: Select the Python Interpreter (The "Brain")

1. Open the Command Palette again: Press Ctrl + Shift + P (Windows) or Cmd + Shift + P (Mac).
2. Type Python: Select Interpreter and press Enter.
3. Look through the list and select the one that says Python 3.10.x ('rl_env': conda).

## 5. Verification
1. In VS Code, create a new file named `test_setup.py`.
2. Copy and paste the following code into the file:

```python
import time
import gymnasium as gym
from stable_baselines3 import PPO

try:
    env = gym.make("LunarLander-v2", render_mode="human")
    observation, info = env.reset()
    print("   Success: Environment loaded! Watch the pop-up window.")
    for step in range(200):
        env.render()
        action = env.action_space.sample() 
        observation, reward, terminated, truncated, info = env.step(action)
        time.sleep(0.01)
        
        if terminated or truncated:
            observation, info = env.reset()

    env.close()

except Exception as e:
    print("ERROR: Something went wrong!")
    print(f"Details: {e}")
```

## Common Fixes
* **Command Not Found:** Make sure you are using the Anaconda Prompt, not the standard Windows Command Prompt, unless you chose Option B during install.
* **SWIG Errors:** If gymnasium[box2d] fails, ensure you ran pip install swig first.
* **Permissions:** If you get a "Permission Denied" error, close the prompt, right-click "Anaconda Prompt" in the Start Menu, and select **"Run as Administrator"**.