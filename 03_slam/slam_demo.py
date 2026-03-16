import matplotlib.pylab as plt
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

COLOR_TRUE_LANDMARK         = '#0d0d0d'
COLOR_ROBOT                 = '#d83034'
COLOR_ROBOT_MEASUREMENT     = '#a1a1a1'
COLOR_MAPPED_LANDMARK       = '#262626'
COLOR_PARTICLE              = '#4ecb8d'
COLOR_ROBOT_ESTIMATED       = '#008dff'
COLOR_OBSERVATIONS          = '#4ecb8d'

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
    def __init__(self, range=8.0, std_distance=0.01, std_angle=0.001):
        self.std_distance = std_distance
        self.std_angle = std_angle
        self.last_measurement = []
        self.range_distance = range

    def read_inf(self, pose, map):
        measurements = []
        for feature in map:
            noise_distance = random.gauss(0.0, self.std_distance)
            noise_angle = random.gauss(0.0, self.std_angle)
            angle_measured, distance_measured = measurement_model(pose, feature)
            measurement = normalize_angle(angle_measured + noise_angle), distance_measured + noise_distance
            measurements.append(measurement)
        self.last_measurement = measurements
        
    def read(self, pose, map):
        measurements = []
        for feature in map:
            angle_measured, distance_measured = measurement_model(pose, feature)
            if distance_measured < self.range_distance:
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

class Particle(Robot):
    def __init__(self, pose=(0, 0, 0), std_distance=0.2, std_angle=0.2):
        super().__init__(pose, std_distance, std_angle)
        self.error = 0.0
        self.map = []

    def update_error(self, measurements, treshold = 2.0):
        self.error = 0.0

        for angle_measured, distance_measured in measurements:
            x_projected = self.x + distance_measured * math.cos(self.theta + angle_measured)
            y_projected = self.y + distance_measured * math.sin(self.theta + angle_measured)
            
            if not self.map:
                self.map.append((x_projected, y_projected))
                continue
            
            best_distance = float('inf')
            best_index = -1
            for i, (x_map, y_map) in enumerate(self.map):
                distance = math.sqrt((x_map - x_projected)**2 + (y_map - y_projected)**2)
                if distance < best_distance:
                    best_index = i
                    best_distance = distance
                    
            if best_distance < treshold:
                # assumption: projected landmark and its closest neighbour are identical
                angle_expected, distnace_expected = measurement_model(self.get_pose(), self.map[best_index])
                error_angle = abs(angle_measured - angle_expected)
                error_distance = abs(distance_measured - distnace_expected)
                self.error += error_angle + error_distance
            
            else:
                # assumption: projected landmark is a new landmark
                self.map.append((x_projected, y_projected))
                self.error += 0.2 + 0.1 * best_distance

class Slam:
    def __init__(self, num_particles=300, treshold=2.0, std_distance=0.2, std_angle=0.2):
        self.num_particles = num_particles
        self.particles = [
            Particle(std_distance=std_distance, std_angle=std_angle) for _ in range(num_particles)
        ]
        self.x_avg = 0.0
        self.y_avg = 0.0
        self.theta_avg = 0.0
        self.treshold_association = treshold
    
    def update(self, angle, step, measurements):
        for p in self.particles:
            p.move(angle, step)
            p.update_error(measurements, self.treshold_association)
    
    def resample(self):
        weights = [math.exp(-p.error * 10.0) for p in self.particles]
        total_weights = sum(weights)
        weights_norm = [w / total_weights for w in weights]
        
        new_particles = []
        N = len(self.particles)
        r = random.uniform(0, 1.0 / N)
        c = weights_norm[0]
        i = 0
        for m in range(N):
            U = r + m * (1.0 / N)
            while U > c:
                i += 1
                c += weights_norm[i]
            new_particles.append(copy.deepcopy(self.particles[i]))
        self.particles = new_particles

    def estimate(self):
        x_y_theta = zip(*[(p.x, p.y, p.theta) for p in self.particles])
        self.x_avg, self.y_avg, self.theta_avg = [sum(x)/len(self.particles) for x in x_y_theta]
        
    def get_pose_estimated(self):
        return self.x_avg, self.y_avg, self.theta_avg

#########################
# HELPER METHODS
def get_visible_landmarks_global(robot_pose, measurements):
    rx, ry, rtheta = robot_pose
    visible_points = []
    for angle_measured, distance_measured in measurements:
        lx = rx + distance_measured * math.cos(rtheta + angle_measured)
        ly = ry + distance_measured * math.sin(rtheta + angle_measured)
        visible_points.append((lx, ly))
    return visible_points

#########################
# DRAW METHODS
def draw_robot(ax:plt.Axes, pose:tuple[float, float, float], color:str='r', length:float=0.3):
    x, y, theta = pose
    ax.plot(x, y,
            color=color,
            marker='o',
            linestyle='none')
    dx = length * math.cos(theta)
    dy = length * math.sin(theta)
    ax.arrow(x, y, dx, dy, head_width=0.2, head_length=0.2, fc=color, ec=color)

def setup_axis(ax:plt.Axes, title:str):
    ax.set_xlim(MAP_X_MIN, MAP_X_MAX)
    ax.set_ylim(MAP_Y_MIN, MAP_Y_MAX)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title(title)

#########################
# MAIN
if __name__ == "__main__":
    map = LANDMARK_POSITIONS
    robot = Robot()
    slam = Slam(num_particles=300, treshold=1.0, std_angle=0.2, std_distance=0.2)
    sensor = Sensor()
    
    turn = 0.0
    step = DEF_STEP
    
    sensor.read(robot.get_pose(), map)
    for p in slam.particles:
        p.update_error(sensor.last_measurement, slam.treshold_association)
    slam.estimate()

    path_real = [(robot.x, robot.y)]
    path_estimated = [(slam.x_avg, slam.y_avg)]
    
    plt.ion()
    fig, (ax_real, ax_belief) = plt.subplots(1, 2, figsize=(14, 6))

    for step_idx in range(NUM_STEPS):
        robot.move(turn, step)
        sensor.read(robot.get_pose(), map)
        
        slam.update(turn, step, sensor.last_measurement)
        slam.resample()
        slam.estimate()
        
        best_particle = min(slam.particles, key=lambda p: p.error)

        path_real.append((robot.x, robot.y))
        path_estimated.append((slam.x_avg, slam.y_avg))
        
        visible_points = get_visible_landmarks_global(robot.get_pose(), sensor.last_measurement)
        
        #########################
        # PLOTTING
        ax_real.clear()
        ax_belief.clear()
        
        setup_axis(ax_real, "Groud Truth")
        setup_axis(ax_belief, "Belief + Map")
        
        # LEFT
        lx, ly = zip(*LANDMARK_POSITIONS)
        ax_real.plot(lx, ly,
                     color=COLOR_TRUE_LANDMARK,
                     marker='s',
                     linestyle='none',
                     label='True landmarks')
        
        ax_real.plot([], [],
                     color=COLOR_ROBOT_MEASUREMENT,
                     linestyle='dashed',
                     linewidth=1,
                     alpha=1,
                     label='Measurements')
        for vx, vy in visible_points:
            ax_real.plot([robot.x, vx],
                         [robot.y, vy],
                         color=COLOR_ROBOT_MEASUREMENT,
                         linestyle='dashed',
                         linewidth=1,
                         alpha=1)
            ax_real.plot(vx, vy,
                         color=COLOR_ROBOT_MEASUREMENT,
                         markersize=8,
                         marker='.',
                         alpha=0.7)
        
        x_real, y_real = zip(*path_real)
        ax_real.plot(x_real,
                     y_real,
                     color=COLOR_ROBOT,
                     linestyle='solid',
                     alpha=0.7,
                     label='True path')
        draw_robot(ax_real, robot.get_pose(), COLOR_ROBOT)
            
        # RIGHT
        px, py = zip(*[(p.x, p.y) for p in slam.particles])
        ax_belief.plot([], [],
                       color=COLOR_PARTICLE,
                       markersize=10,
                       marker='.',
                       linestyle='none',
                       alpha=1,
                       label='Particles')
        ax_belief.plot(px, py,
                       color=COLOR_PARTICLE,
                       markersize=10,
                       marker='.',
                       linestyle='none',
                       alpha=0.3)
        
        if best_particle.map:
            mx, my = zip(*best_particle.map)
            ax_belief.plot(mx, my,
                           color=COLOR_MAPPED_LANDMARK,
                           marker='s',
                           linestyle='none',
                           alpha=1,
                           label='Mapped landmarks')
        
        est_x, est_y = zip(*path_estimated)
        ax_belief.plot(est_x, est_y,
                       color=COLOR_ROBOT_ESTIMATED,
                       alpha=0.7,
                       label='Estimated path')
        draw_robot(ax_belief, slam.get_pose_estimated(), COLOR_ROBOT_ESTIMATED)
        
        if visible_points:
            vx, vy = zip(*visible_points)
            ax_belief.plot(vx, vy,
                           color=COLOR_OBSERVATIONS,
                           markersize=8,
                           marker='x',
                           linestyle='none',
                           alpha=1,
                           label='Current observations')

        ax_real.legend(loc='upper left')
        ax_belief.legend(loc='upper left')
        
        plt.pause(ANIM_PAUSE)
        
    plt.ioff()
    plt.show()