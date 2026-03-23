import pybullet as p
import pybullet_data
import time
import os

p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.resetDebugVisualizerCamera(cameraDistance=5.0, cameraYaw=0, cameraPitch=-30, cameraTargetPosition=[0, 0, 0])

pwd = os.path.dirname(os.path.abspath(__file__))
urdf_path = os.path.join(pwd, "models", "pendulum.urdf")

# environment
p.setGravity(0, 0, -9.81)
pendulum = p.loadURDF(urdf_path)

p.resetJointState(pendulum, 1, targetValue=0.3)
p.setJointMotorControl2(pendulum, 0, p.VELOCITY_CONTROL, force=0)
p.setJointMotorControl2(pendulum, 1, p.VELOCITY_CONTROL, force=0)

# tune your PID parameters!
Kp_pole = 20.0
Ki_pole = 0.1
Kd_pole = 0.5

Kp_cart = 20
Ki_cart = 5
Kd_cart = 1

integral_pole = 0
last_error_pole = 0

integral_cart = 0
last_error_cart = 0

# main loop
while True:
    cart_pos, cart_vel = p.getJointState(pendulum, 0)[0:2]
    pole_ang, pole_vel = p.getJointState(pendulum, 1)[0:2]
    
    error_pole = pole_ang - 0
    error_cart = cart_pos - 0
    
    integral_pole += error_pole
    integral_cart += error_cart
    
    v_pole = (Kp_pole * error_pole) + (Ki_pole * integral_pole) + (Kd_pole * pole_vel)
    v_cart = (Kp_cart * error_cart) + (Ki_cart * integral_pole) + (Kd_cart * cart_vel)
    
    v_total = v_pole + v_cart
    p.setJointMotorControl2(pendulum, 0, p.VELOCITY_CONTROL, targetVelocity=v_total)
    
    p.stepSimulation()
    time.sleep(1./240.)