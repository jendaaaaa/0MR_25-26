import pybullet as p
import pybullet_data
import time
import os

p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.resetDebugVisualizerCamera(cameraDistance=10, cameraYaw=0, cameraPitch=-30,
                             cameraTargetPosition=[0, 0, 0])
p.setGravity(0, 0, -9.81)

pwd = os.path.dirname(os.path.abspath(__file__))
urdf_path = os.path.join(pwd, "models", "new_pendulum.urdf")
pendulum = p.loadURDF(urdf_path)

p.resetJointState(pendulum, 1, targetValue=0.3)
p.setJointMotorControl2(pendulum, 0, p.VELOCITY_CONTROL, force=0)
p.setJointMotorControl2(pendulum, 1, p.VELOCITY_CONTROL, force=0)

integral = 0
while True:
    p.stepSimulation()
    angle, velocity = p.getJointState(pendulum, 1)[0:2]
    error_angle = angle - 0
    integral += error_angle
    action = error_angle * 20 + integral * 5
    p.setJointMotorControl2(pendulum, 0, p.VELOCITY_CONTROL, targetVelocity=action)

    time.sleep(1./240.)