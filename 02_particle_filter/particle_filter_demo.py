import numpy as np
import pylab as plt
import random

NUM_PARTICLES = 500
# NUM_STEPS = 10
NUM_STEPS = 20

FEATURE_POSITIONS = [(1.0, 3.0), (6.0, 4.0), (9.0, 5.0), (14.0, 3.0),(17.0, 5.0), (20.0, 4.0)]
# FEATURE_POSITIONS = [(5.0, 3.0)]
STEP_DISTANCE = 1

MAP_MIN_X, MAP_MAX_X = -2.0, 22.0
MAP_MIN_Y, MAP_MAX_Y = -2.0, 8.0

SIGMA_DISTANCE = 0.05
SIGMA_MEASUREMENT = 0.01
SIGMA_ANGLE = 0.5

def move(state, d_phi=0.0, distance=STEP_DISTANCE):
    x, y, phi = state
    phi += d_phi
    ds = random.gauss(distance, SIGMA_DISTANCE)
    x = x + ds * np.cos(phi)
    y = y + ds * np.sin(phi)
    return x, y, phi

def calculate_distance(point_a, point_b):
    xa, ya = point_a
    xb, yb = point_b
    return np.sqrt((xa - xb)**2 + (ya - yb)**2)

def measure_distance(state, target):
    true_distance = calculate_distance((state[0], state[1]), target)
    noise = random.gauss(0, SIGMA_MEASUREMENT)
    return true_distance + noise

def move_particle(particle_state):
    d_phi = random.gauss(0, SIGMA_ANGLE)
    return move(particle_state, d_phi)

def update_weights(particles, measured_distances, features):
    weights = []
    for particle in particles:
        total_error = 0.0
        for distance, feature in zip(measured_distances, features):
            expected_distance = calculate_distance((particle[0], particle[1]), feature)
            error = abs(distance - expected_distance)
            total_error += error
        weight = 1.0 / (total_error + 0.001)
        weights.append(weight)
        
    total_weight = sum(weights)
    return [weight / total_weight for weight in weights]

def resample_particles(particles, weights):
    return random.choices(particles, weights=weights, k=len(particles))

def get_estimate(particles):
    avg_x = sum(p[0] for p in particles) / len(particles)
    avg_y = sum(p[1] for p in particles) / len(particles)
    return avg_x, avg_y

if __name__ == "__main__":    
    state = (0.0, 0.0, 0.0) # x, y, phi

    # robot initially knows where it is
    particles = [(0.0, 0.0, 0.0) for _ in range(NUM_PARTICLES)]
    state_estimated = state

    # robot doesnt know where it is    
    # particles = []
    # for _ in range(NUM_PARTICLES):
    #     rand_x = random.uniform(MAP_MIN_X, MAP_MAX_X)
    #     rand_y = random.uniform(MAP_MIN_Y, MAP_MAX_Y)
    #     rand_phi = random.uniform(0, 2 * np.pi)
    #     particles.append((rand_x, rand_y, rand_phi))
    # state_estimated = get_estimate(particles)
    
    plt.figure(figsize=(16, 8))
    plt.title("Particle Filter")
    plt.xlim(MAP_MIN_X, MAP_MAX_X)
    plt.ylim(MAP_MIN_Y, MAP_MAX_Y)
    
    plt.plot([], [], 'ko', markersize=8, label="Features")
    plt.plot([], [], 'ro', markersize=8, label="Real Position")
    plt.plot([], [], 'bo', markersize=6, label="Estimated Position")
    plt.scatter([], [], color='green', alpha=1, label="Particles")
    plt.legend(loc="upper left")

    for feature in FEATURE_POSITIONS:
        plt.plot(feature[0], feature[1], 'ko', markersize=8)

    for step in range(NUM_STEPS + 1):
        plt.plot(state[0], state[1], 'ro', markersize=8)
        px = [p[0] for p in particles]
        py = [p[1] for p in particles]
        plt.scatter(px, py, color='green', alpha=0.3, s=10)
        plt.plot(state_estimated[0], state_estimated[1], 'bo', markersize=6)
        state = move(state)
        particles = [move_particle(particle) for particle in particles]
        distances = [measure_distance(state, target) for target in FEATURE_POSITIONS]
        weights = update_weights(particles, distances, FEATURE_POSITIONS)
        particles = resample_particles(particles, weights)
        state_estimated = get_estimate(particles)
        plt.pause(0.3)
        
    plt.show()