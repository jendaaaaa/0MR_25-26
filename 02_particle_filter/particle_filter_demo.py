import numpy as np
import pylab as plt
import random

##################################################################
# CONSTANTS ######################################################
##################################################################

# --- particle filter
NUM_PARTICLES = 500
NUM_STEPS = 20

# --- environment
# try to change number or position of landmarks
LANDMARK_POSITIONS = [(1.0, 3.0), (6.0, 4.0), (9.0, 5.0), (14.0, 3.0),(17.0, 5.0), (20.0, 4.0)]
# LANDMARK_POSITIONS = [(5.0, 3.0)]

MAP_MIN_X, MAP_MAX_X = -2.0, 22.0
MAP_MIN_Y, MAP_MAX_Y = -2.0, 8.0

# --- motion model
STEP_DISTANCE = 1

# --- distribution constants (std)
SIGMA_DISTANCE = 0.5            # uncertainty in driving forward
SIGMA_ANGLE = 0.3               # uncertainty in steering

# --- animation
ANIM_PAUSE_S = 0.3

##################################################################
# MOTION #########################################################
##################################################################

def motion_model(state, d_phi=0.0, distance=STEP_DISTANCE):
    x, y, phi = state
    phi += d_phi

    x = x + distance * np.cos(phi)
    y = y + distance * np.sin(phi)
    return x, y, phi

# robot's movement is not perfect, it moves with ceratin amount of noise
# (steers a bit more/less, goes a bit faster/slower)
def move_robot(robot_state):
    d_phi = random.gauss(0.0, 0.01)                     # noise in steering
    distance = random.gauss(STEP_DISTANCE, 0.01)        # noise in driving forward
    return motion_model(robot_state, d_phi, distance)   # returning precise motion model with added noise

# the same as robot, but we set the STDs ourselves - we choose how much we trust the robot's motion
def move_particle(particle_state):
    d_phi = random.gauss(0, SIGMA_ANGLE)
    distance = random.gauss(STEP_DISTANCE, SIGMA_DISTANCE)
    return motion_model(particle_state, d_phi)

##################################################################
# SENSORS ########################################################
##################################################################

# exact distance between 2 points (state - landmark)
def calculate_distance(point_a, point_b):
    xa, ya = point_a
    xb, yb = point_b
    return np.sqrt((xa - xb)**2 + (ya - yb)**2)

# simulation of real sensor with noise
def measure_distance(state, target):
    true_distance = calculate_distance((state[0], state[1]), target)
    noise = random.gauss(0, 0.01)       # simulating noisy sensor readings
    return true_distance + noise

##################################################################
# PARTICLE FILTER ################################################
##################################################################

# calculate error of each particle and calculate weights
def update_weights(particles, measured_distances, landmarks):
    weights = []
    for particle in particles:
        # iterate through all particles
        total_error = 0.0
        for distance, landmark in zip(measured_distances, landmarks):
            # exact distance, particles are hypotheses (virtual), no noisy sensor
            expected_distance = calculate_distance((particle[0], particle[1]), landmark)
            # difference between sensor reading and particle's calculated distance
            error = abs(distance - expected_distance)
            total_error += error

        # safe division (non zero)
        weight = 1.0 / (total_error + 0.001)
        weights.append(weight)
        
    total_weight = sum(weights)
    return [weight / total_weight for weight in weights]

def resample(particles, weights):
    # simplest method of resampling - ROULETTE WHEEL
    return random.choices(particles, weights=weights, k=len(particles))

def get_estimate(particles):
    # simplest method of getting estimated position - AVERAGE position of all particles
    avg_x = sum(p[0] for p in particles) / len(particles)
    avg_y = sum(p[1] for p in particles) / len(particles)
    return avg_x, avg_y

##################################################################
# MAIN ###########################################################
##################################################################

if __name__ == "__main__":
    # init state of robot
    state = (0.0, 0.0, 0.0) # x, y, phi
    
    # >>> robot initially knows where it is
    particles = [(0.0, 0.0, 0.0) for _ in range(NUM_PARTICLES)]
    state_estimated = state

    # # >>> robot doesnt know where it is
    # particles = []
    # for _ in range(NUM_PARTICLES):
    #     rand_x = random.uniform(MAP_MIN_X, MAP_MAX_X)
    #     rand_y = random.uniform(MAP_MIN_Y, MAP_MAX_Y)
    #     rand_phi = random.uniform(0, 2 * np.pi)
    #     particles.append((rand_x, rand_y, rand_phi))
    # state_estimated = get_estimate(particles)
    
    # plot config
    plt.figure(figsize=(16, 8))
    plt.title("Particle Filter")
    plt.xlim(MAP_MIN_X, MAP_MAX_X)
    plt.ylim(MAP_MIN_Y, MAP_MAX_Y)
    
    # initialize legend
    plt.plot([], [], 'ko', markersize=8, label="landmarks")
    plt.plot([], [], 'ro', markersize=8, label="Real Position")
    plt.plot([], [], 'bo', markersize=6, label="Estimated Position")
    plt.scatter([], [], color='green', alpha=1, label="Particles")

    # draw landmarks
    for landmark in LANDMARK_POSITIONS:
        plt.plot(landmark[0], landmark[1], 'ko', markersize=8)

    # draw initial state
    plt.plot(state[0], state[1], 'ro', markersize=8)
    plt.plot(state_estimated[0], state_estimated[1], 'bo', markersize=6)
    px = [p[0] for p in particles]
    py = [p[1] for p in particles]
    plt.scatter(px, py, color='green', alpha=0.3)

    # update plot and wait
    plt.legend(loc="upper left")
    plt.pause(ANIM_PAUSE_S)

    # iterate through all steps
    for step in range(NUM_STEPS):
        # move robot
        state = move_robot(state)

        # move particle
        particles = [move_particle(particle) for particle in particles]

        # measure distances
        distances = [measure_distance(state, target) for target in LANDMARK_POSITIONS]

        # calculate weights
        weights = update_weights(particles, distances, LANDMARK_POSITIONS)
        
        # resample particles
        particles = resample(particles, weights)

        # calculate estimated position
        state_estimated = get_estimate(particles)
        
        # draw robot
        plt.plot(state[0], state[1], 'ro', markersize=8)

        # draw particles
        px = [p[0] for p in particles]
        py = [p[1] for p in particles]
        plt.scatter(px, py, color='green', alpha=0.3, s=10)

        # draw estimated position
        plt.plot(state_estimated[0], state_estimated[1], 'bo', markersize=6)

        # animate plot
        plt.pause(ANIM_PAUSE_S)

    plt.show()