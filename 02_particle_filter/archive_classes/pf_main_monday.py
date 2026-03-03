import numpy as np
from matplotlib import pyplot as plt
import math
import random

NUM_STEPS = 10
DEF_STEP = 1.0
NUM_PARTICLES = 500

STD_ANGLE = 0.2
STD_DISTANCE = 0.05

MAP_X_MIN, MAP_X_MAX = -1.0, 11.0
MAP_Y_MIN, MAP_Y_MAX = -6.0, 6.0

# landmarks
LANDMARKS_POSITIONS = [(1.0, 2.0), (3.0, 1.0), (5.0, 3.0), (9.0, 4.0), (10.0, 2.0)]
# LANDMARKS_POSITIONS = [(1.0, 2.0)]

def motion_model(state, d_phi=0.0, distance=DEF_STEP):
    x, y, phi = state
    phi += d_phi
    x = x + distance * math.cos(phi)
    y = y + distance * math.sin(phi)
    return x, y, phi

def move_robot(state_robot):
    d_phi = random.gauss(0.0, 0.01)
    distance = random.gauss(DEF_STEP, 0.05)
    return motion_model(state_robot, d_phi, distance)

def move_particles(state_particle):
    d_phi = random.gauss(0.0, STD_ANGLE)
    distance = random.gauss(DEF_STEP, STD_DISTANCE)
    return motion_model(state_particle, d_phi, distance)

def calculate_distance(pa, pb):
    xa, ya = pa
    xb, yb = pb
    return math.sqrt((xa-xb)**2 + (ya-yb)**2)

def measure_distance(state, target):
    true_distance = calculate_distance(state[0:2], target[0:2])
    noise = random.gauss(0.0, 0.01)
    return true_distance + noise

def update_weights(particles, distances, landmarks):
    weights = []
    for particle in particles:
        total_error = 0.0
        for landmark, measured_distance in zip(landmarks, distances):
            distance = calculate_distance(particle[0:2], landmark[0:2])
            error = abs(distance - measured_distance)
            total_error += error
        weight = 1.0 / (total_error + 0.0001)
        weights.append(weight)
    total_weight = sum(weights)
    return [(w / total_weight) for w in weights]

def resample(particles, weights):
    return random.choices(particles, weights=weights, k=len(particles))

def get_estimate(particles):
    px = [p[0] for p in particles]
    py = [p[1] for p in particles]
    avg_x = sum(px) / len(particles)
    avg_y = sum(py) / len(particles)
    return avg_x, avg_y

# robot (x, y, phi)
state = (0.0, 0.0, 0.0)
# particles = [state for _ in range(NUM_PARTICLES)]

particles = []
for _ in range(NUM_PARTICLES):
    rand_x = random.uniform(MAP_X_MIN, MAP_X_MAX)
    rand_y = random.uniform(MAP_Y_MIN, MAP_Y_MAX)
    rand_phi = random.uniform(0.0, 2.0 * math.pi)
    particles.append((rand_x, rand_y, rand_phi))

est_state = get_estimate(particles)

# plot
plt.figure(figsize=(8,4))
plt.title("Particle filter")
plt.xlim(MAP_X_MIN, MAP_X_MAX)
plt.ylim(MAP_Y_MIN, MAP_Y_MAX)
plt.plot(state[0], state[1], "ro", markersize=8, label="Real position")
plt.plot([], [], "bo", markersize=8, label="Estimated position")
plt.plot([], [], "ko", markersize=8, label="Landmark")
plt.plot([], [], "go", markersize=6, alpha=1, label="Particles")

for landmark in LANDMARKS_POSITIONS:
    plt.plot(landmark[0], landmark[1], "ko")
plt.legend()

for step in range(NUM_STEPS):
    plt.pause(0.5)
    
    state = move_robot(state)
    particles = [move_particles(p) for p in particles]
    distances = [measure_distance(state, target) for target in LANDMARKS_POSITIONS]
    weights = update_weights(particles, distances, LANDMARKS_POSITIONS)
    particles = resample(particles, weights)
    est_state = get_estimate(particles)

    px = [p[0] for p in particles]
    py = [p[1] for p in particles]
    plt.plot(px, py, "go", alpha=0.3, markersize=6)
    plt.plot(state[0], state[1], "ro", markersize=8)
    plt.plot(est_state[0], est_state[1], "bo", markersize=8)

plt.show()