import pybullet as p
import pybullet_data
import time

p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.81)

visual = p.createVisualShape(shapeType=p.GEOM_SPHERE, radius=0.4, rgbaColor=[1, 0, 0, 1])
collision = p.createCollisionShape(shapeType=p.GEOM_SPHERE, radius=0.4)
# inertia

ball = p.createMultiBody(baseCollisionShapeIndex=collision,
                         baseVisualShapeIndex=visual,
                         basePosition=[0, 0, 3],
                         baseMass=1)

floor = p.loadURDF("plane.urdf")

p.changeVisualShape(ball, -1, rgbaColor=[0, 1, 0, 1])

p.changeDynamics(ball, -1, restitution=0.8)
p.changeDynamics(floor, -1, restitution=0.8)

while True:
    p.stepSimulation()
    time.sleep(1./240.)