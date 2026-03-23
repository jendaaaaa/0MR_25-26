import pybullet as p
import pybullet_data
import time

p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.resetDebugVisualizerCamera(cameraDistance=15.0, cameraYaw=0, cameraPitch=-30, cameraTargetPosition=[0, 0, 2])

# environment
p.setGravity(0, 0, -9.81)
floor = p.loadURDF("plane.urdf")

# ball parameters
radius = 0.5
collision_shape = p.createCollisionShape(shapeType=p.GEOM_SPHERE, radius=radius)
visual_red = p.createVisualShape(shapeType=p.GEOM_SPHERE, radius=radius, rgbaColor=[1, 0, 0, 1])
visual_blue = p.createVisualShape(shapeType=p.GEOM_SPHERE, radius=radius, rgbaColor=[0, 0, 1, 1])

def create_ball(position, color_rgba=[1, 0, 0, 1], radius=0.4):
    collision_id = p.createCollisionShape(shapeType=p.GEOM_SPHERE, radius=radius)
    visual_id = p.createVisualShape(shapeType=p.GEOM_SPHERE, radius=radius, rgbaColor=color_rgba)
    return p.createMultiBody(baseMass=1.0, baseCollisionShapeIndex=collision_id, baseVisualShapeIndex=visual_id, basePosition=position)

def create_pair(x_offset=0, y_offset=0, restitution=1):
    colors = [[1, 0, 0, 1], [0, 0, 1, 1]]
    offests = [1.5, -1.5]
    velocities = [-3, 3]
    for i in range(2):
        b = create_ball([x_offset + offests[i], y_offset, 3], colors[i])
        p.changeDynamics(b, -1, restitution=restitution)
        p.resetBaseVelocity(b, linearVelocity=[velocities[i], 0, 0])

p.changeDynamics(floor, -1, restitution=1)
restitutions = [0, 0.8, 1]
x_offsets = [0, 0, 0]
y_offsets = [-2, 0, 2]
for i in range(len(restitutions)):
    create_pair(x_offsets[i], y_offsets[i], restitutions[i])

# main loop
while True:
    p.stepSimulation()
    time.sleep(1./240.)