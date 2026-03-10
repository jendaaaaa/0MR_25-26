from matplotlib import pylab as plt
import math, random, copy

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
def normalize_angle(angle):
    return (angle + math.pi) % ( 2 * math.pi) - math.pi

def motion_model(pose, phi, d):
    x, y, theta = pose
    theta = theta + phi
    x = x + d * math.cos(theta)
    y = y + d * math.sin(theta)
    return x, y, theta

def measurement_model(pose: tuple[float, float, float], target: tuple[float, float]) -> tuple[float, float]:
    xp, yp, thetap = pose
    xt, yt = target
    dx = xt - xp
    dy = yt - yp
    distance = math.sqrt(dx**2 + dy**2)
    angle = normalize_angle(math.atan2(dy,dx) - thetap)
    return angle, distance

#########################
# CLASSES
class Sensor:
    def __init__(self, std_distance=0.01, std_angle=0.001):
        self.std_distance = std_distance
        self.std_angle = std_angle
        self.last_measurement = []

    def read(self, pose, map):
        measurements = []
        for feature in map:
            noise_distance = random.gauss(0.0, self.std_distance)
            noise_angle = random.gauss(0.0, self.std_angle)
            angle_measured, distance_measured = measurement_model(pose, feature)
            measurement = normalize_angle(angle_measured + noise_angle), distance_measured + noise_distance
            measurements.append(measurement)
        self.last_measurement = measurements

class Robot:
    def __init__(self, pose=(0.0, 0.0, 0.0), std_distance=0.1, std_angle=0.1):
        self.x, self.y, self.theta = pose
        self.std_distance = std_distance
        self.std_angle = std_angle

    def get_pose(self):
        return self.x, self.y, self.theta
    
    def set_pose(self, pose):
        self.x, self.y, self.theta = pose

    def move(self, angle_cmd, distance_cmd):
        angle = angle_cmd + random.gauss(0.0, self.std_angle)
        distance = distance_cmd + random.gauss(0.0, self.std_distance)
        self.set_pose(motion_model(self.get_pose(), angle, distance))

    def draw(self):
        plt.plot(self.x, self.y, 'ro')

class Particle(Robot):
    def __init__(self, pose=(0, 0, 0), std_distance=0.2, std_angle=0.2):
        super().__init__(pose, std_distance, std_angle)
        self.error = 0.0

    def update_error(self, measurements, map):
        self.error = 0.0
        for measurement, feature in zip(measurements, map):
            angle_measured, distance_measured = measurement
            angle_particle, distance_particle = measurement_model(self.get_pose(), feature)
            error_distance = abs(distance_measured - distance_particle)**2
            error_angle = abs(angle_measured - angle_particle)**2
            self.error += error_distance + error_angle

class ParticleFilter:
    def __init__(self, num_particles=300, std_distance=0.2, std_angle=0.2):
        self.num_particles = num_particles
        self.particles = [
            Particle(std_distance=std_distance, std_angle=std_angle) for _ in range(num_particles)
        ]
        self.x_avg = 0.0
        self.y_avg = 0.0
        self.theta_avg = 0.0
    
    def update(self, angle, step, measurements, map):
        for p in self.particles:
            p.move(angle, step)
            p.update_error(measurements, map)
    
    def resample(self):
        weights = [(1.0 / p.error) for p in self.particles]
        total_weights = sum(weights)
        weights_norm = [w / total_weights for w in weights]

        new_particles = random.choices(self.particles, weights_norm, k=len(self.particles))
        self.particles = [copy.deepcopy(p) for p in new_particles]

    def estimate(self):
        sum_x, sum_y, sum_theta = 0.0, 0.0, 0.0
        num = len(self.particles)
        for p in self.particles:
            sum_x += p.x
            sum_y += p.y
            sum_theta += p.theta
        self.x_avg = sum_x/num
        self.y_avg = sum_y/num
        self.theta_avg = sum_theta/num

    def draw_particles(self):
        px, py = zip(*[(p.x, p.y) for p in self.particles])
        plt.plot(px, py, 'go', alpha=0.2, markersize=3)

    def draw_estimate(self):
        plt.plot(self.x_avg, self.y_avg, 'bo', markersize=5)

#########################
# MAIN
if __name__ == "__main__":
    map = LANDMARK_POSITIONS
    robot = Robot()
    pf = ParticleFilter(num_particles=400)
    sensor = Sensor()

    plt.figure()
    pf.draw_particles()
    robot.draw()
    pf.draw_estimate()
    lx, ly = zip(*LANDMARK_POSITIONS)
    plt.plot(lx, ly, 'ko')

    plt.xlim(MAP_X_MIN, MAP_X_MAX)
    plt.ylim(MAP_Y_MIN, MAP_Y_MAX)
    plt.pause(ANIM_PAUSE)

    angle = 0.0
    step = DEF_STEP

    for _ in range(NUM_STEPS):
        robot.move(angle, step)
        sensor.read(robot.get_pose(), map)
        pf.update(angle, step, sensor.last_measurement, map)
        pf.resample()
        pf.estimate()

        pf.draw_particles()
        robot.draw()
        pf.draw_estimate()
        plt.pause(ANIM_PAUSE)

    plt.show()