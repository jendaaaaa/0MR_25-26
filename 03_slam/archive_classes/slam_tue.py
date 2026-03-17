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
    def __init__(self, std_distance=0.01, std_angle=0.001, range=8.0):
        self.std_distance = std_distance
        self.std_angle = std_angle
        self.last_measurement = []
        self.max_range = range

    def read(self, pose, map):
        measurements = []
        for feature in map:
            angle_measured, distance_measured = measurement_model(pose, feature)
            if distance_measured <= self.max_range:
                noise_distance = random.gauss(0.0, self.std_distance)
                noise_angle = random.gauss(0.0, self.std_angle)
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
        self.map = []

    def init_map(self, measurements):
        for m in measurements:
            angle_measured, distance_measured = m
            x_projected = self.x + distance_measured * math.cos(self.theta + angle_measured)
            y_projected = self.y + distance_measured * math.sin(self.theta + angle_measured)
            self.map.append((x_projected, y_projected))

    def update_error(self, measurements, treshold=2.0):
        self.error = 0.0
        for m in measurements:
            angle_measured, distance_measured = m

            x_projected = self.x + distance_measured * math.cos(self.theta + angle_measured)
            y_projected = self.y + distance_measured * math.sin(self.theta + angle_measured)

            best_distance = float('inf')
            best_idx = -1
            for i, (x_map, y_map) in enumerate(self.map):
                distance = math.sqrt((x_map - x_projected)**2 + (y_map - y_projected)**2)
                if distance < best_distance:
                    best_distance = distance
                    best_idx = i

            if best_distance < treshold:
                # ASSUMPTION: projected and map landmark are identical
                angle_particle, distance_particle = measurement_model(self.get_pose(), self.map[best_idx])
                error_distance = abs(distance_measured - distance_particle)**2
                error_angle = abs(angle_measured - angle_particle)**2
                self.error += error_distance + error_angle

            else:
                # ASSUMPTION: new landmark! store to map
                self.map.append((x_projected, y_projected))
                self.error += 0.2 + 0.1 * best_distance

class Slam:
    def __init__(self, num_particles=300, std_distance=0.2, std_angle=0.2, treshold=2.0):
        self.num_particles = num_particles
        self.particles = [
            Particle(std_distance=std_distance, std_angle=std_angle) for _ in range(num_particles)
        ]
        self.x_avg = 0.0
        self.y_avg = 0.0
        self.theta_avg = 0.0
        self.assumption_treshold = treshold
    
    def update(self, angle, step, measurements):
        for p in self.particles:
            p.move(angle, step)
            p.update_error(measurements, self.assumption_treshold)
    
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

    def draw_map(self):
        best_particle = min(self.particles, key=lambda p: p.error)
        if best_particle.map:
            x_map_est, y_map_est = zip(*best_particle.map)
            plt.plot(x_map_est, y_map_est, 'gx')

#########################
# MAIN
if __name__ == "__main__":
    map = LANDMARK_POSITIONS
    robot = Robot(std_angle=0.2, std_distance=0.2)
    slam = Slam(num_particles=400)
    sensor = Sensor(std_distance=0.1, std_angle=0.05)

    sensor.read(robot.get_pose(), map)
    for p in slam.particles:
        p.init_map(sensor.last_measurement)

    plt.figure()
    slam.draw_particles()
    robot.draw()
    slam.draw_estimate()
    slam.draw_map()
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
        slam.update(angle, step, sensor.last_measurement)
        slam.resample()
        slam.estimate()

        slam.draw_particles()
        robot.draw()
        slam.draw_estimate()
        slam.draw_map()
        plt.pause(ANIM_PAUSE)

    plt.show()