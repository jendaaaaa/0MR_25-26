# Introduction

**PyBullet** is the Python interface for the [Bullet Physics SDK](https://pybullet.org/). It is a high-performance physics engine used widely for **Reinforcement Learning (RL)**, **Motion Planning**, and **Sim-to-Real** transfer in robotics.

[Bullet Docs](https://github.com/bulletphysics/bullet3/tree/master/docs)

---

## 1. Core Architecture
PyBullet operates on a **Client-Server** model. Your Python script is the *Client*, sending instructions to the *Physics Server* which handles the heavy math.

### Connection Modes
* **`p.GUI`**: Opens a 3D visualizer window. Best for debugging and watching your robot move.
* **`p.DIRECT`**: No window (headless). Used for high-speed training on servers or in the cloud.

---

## 2. The URDF
The **Unified Robot Description Format (URDF)** is an XML file that defines the robot's structure using a tree-like hierarchy.

### Links vs. Joints
* **Links (The Bones):** Rigid bodies. Each link contains:
    * `<visual>`: The 3D model (what it looks like).
    * `<collision>`: The simplified "hit-box" (for physics calculations).
    * `<inertial>`: Mass and inertia properties.
* **Joints (The Hinges):** Connects a "Parent Link" to a "Child Link."
    * **Revolute:** Rotational movement with limits (e.g., an elbow).
    * **Continuous:** Rotational movement without limits (e.g., a wheel).
    * **Prismatic:** Linear sliding movement (e.g., a piston).
    * **Fixed:** No movement allowed (e.g., a camera mount).

---

## 3. Essential Commands

### Simulation Setup
```python
import pybullet as p
import pybullet_data

# Connect and set search path for default models
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# World settings
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf") # Load a floor
```

### Robot Control & State
| Feature | Command |
| :--- | :--- |
| **Load Robot** | `robotId = p.loadURDF("robot.urdf", [x, y, z])` |
| **Step Physics** | `p.stepSimulation()` (Call this in a loop!) |
| **Get State** | `pos, orn = p.getBasePositionAndOrientation(robotId)` |
| **Move Joint** | `p.setJointMotorControl2(robotId, jointIdx, p.POSITION_CONTROL, targetPosition=val)` |
| **Inverse Kinematics** | `jointPoses = p.calculateInverseKinematics(robotId, eeIdx, [x, y, z])` |

---

## 4. "Hello World" Script
Copy and paste this into a `.py` file to see a simple robotic arm in action.

```python
import pybullet as p
import pybullet_data
import time

# Initialize
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# Load Plane and Robot
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("franka_panda/panda.urdf", useFixedBase=True)

# Simulation Loop
for i in range(1000):
    # Move joint index 0 to a sine-wave position
    targetPos = 1.0 * (i / 100.0)
    p.setJointMotorControl2(robotId, 0, p.POSITION_CONTROL, targetPosition=targetPos)
    
    p.stepSimulation()
    time.sleep(1./240.) # 240Hz is the default step frequency

p.disconnect()
```

![PyBullet Hello World](/pybullet_hello_world.png)

---

## Tips
1.  **Quaternions:** PyBullet uses Quaternions $(x, y, z, w)$ for rotation. Use `p.getQuaternionFromEuler([r, p, y])` if you prefer working with degrees/radians.
2.  **Indexing:** Joint indices start at $0$. Always check `p.getNumJoints(robotId)` and `p.getJointInfo()` to identify which index corresponds to which motor.
3.  **Real-Time:** If you don't want to manually step the simulation, use `p.setRealTimeSimulation(1)`, but note this is less deterministic for AI training.
