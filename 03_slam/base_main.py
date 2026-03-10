from matplotlib import pylab as plt
import math, random

#########################
# CONSTANTS
NUM_PARTICLES = 500
NUM_STEPS = 10
DEF_STEP = 1.0
MAP_X_MIN, MAP_X_MAX = -1.0, 11.0
MAP_Y_MIN, MAP_Y_MAX = -6.0, 6.0
LANDMARK_POSITIONS = [(2.0, 2.0), (2.0, -3.0), (3.0, 3.0), (5.0, -3), (5.0, 2.5), (8.0, -2.0), (9.0, 3.0)]

STD_ANGLE = 0.2
STD_DISTANCE = 0.2

ANIM_PAUSE = 0.3

#########################
# METHODS
def motion_model(pose, phi, d):
    x, y, theta = pose
    theta = theta + phi
    x = x + d * math.cos(theta)
    y = y + d * math.sin(theta)
    return x, y, theta

def move_robot(pose):
    angle = random.gauss(0.0, 0.05)
    distance = DEF_STEP + random.gauss(0.0, 0.1)
    return motion_model(pose, angle, distance)

def update_particle(pose):
    angle = random.gauss(0.0, STD_ANGLE)
    distance = DEF_STEP + random.gauss(0.0, STD_DISTANCE)
    return motion_model(pose, angle, distance)

def calculate_distance(point_a, point_b):
    xa, ya = point_a
    xb, yb = point_b
    return math.sqrt((xa - xb)**2 + (ya - yb)**2)

def measure_distance(pose, landmark):
    noise = random.gauss(0.0, 0.01)
    return calculate_distance(pose[:2], landmark[:2]) + noise

def update_weights(particles, landmarks, measurements):
    weights = []
    for particle in particles:
        total_error = 0.0
        for landmark, measurement in zip(landmarks, measurements):
            distance = calculate_distance(particle[:2], landmark[:2])
            error = abs(measurement - distance)**2
            total_error += error
        weight = 1.0 / (total_error + 0.0001) # safety check
        weights.append(weight)
    total_weights = sum(weights)
    return [w / total_weights for w in weights]
        
def resample(particles, weights):
    return random.choices(particles, weights, k=len(particles))

def get_estimate(particles):
    px, py, ptheta = zip(*particles)
    num = len(particles)
    avg_x = sum(px) / num
    avg_y = sum(py) / num
    avg_theta = sum(ptheta) / num
    return avg_x, avg_y, avg_theta

#########################
# MAIN
state = (0.0, 0.0, 0.0)
particles = [(0.0, 0.0, 0.0) for _ in range(NUM_PARTICLES)]

plt.figure()
plt.plot(state[0], state[1], 'ro')
lx, ly = zip(*LANDMARK_POSITIONS)
plt.plot(lx, ly, 'ko')
px, py, _ = zip(*particles)
plt.plot(px, py, 'go', alpha=0.2, markersize=3)

plt.xlim(MAP_X_MIN, MAP_X_MAX)
plt.ylim(MAP_Y_MIN, MAP_Y_MAX)
plt.pause(ANIM_PAUSE)

for step in range(NUM_STEPS):
    state = move_robot(state)
    particles = [update_particle(p) for p in particles]
    measurements = [measure_distance(state, lm) for lm in LANDMARK_POSITIONS]
    weights = update_weights(particles, LANDMARK_POSITIONS, measurements)
    particles = resample(particles, weights)
    estimated_state = get_estimate(particles)

    px, py, _ = zip(*particles)
    plt.plot(px, py, 'go', alpha=0.2, markersize=3)
    plt.plot(state[0], state[1], 'ro')
    plt.plot(estimated_state[0], estimated_state[1], 'bo', markersize=5)
    plt.pause(ANIM_PAUSE)

plt.show()