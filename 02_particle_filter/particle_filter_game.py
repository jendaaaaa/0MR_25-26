import pygame
import math
import numpy as np
import random
import os

##################################################################
# CONSTANTS ######################################################
##################################################################
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 30

COLOR_ROBOT = (0, 255, 0)
COLOR_NOSE = (20, 20, 20)
COLOR_PARTICLES = (0, 0, 255)
COLOR_SENSOR_MEASUREMENTS = (255, 0, 0)
COLOR_ESTIMATE = (255, 0, 0)

##################################################################
# CLASSES ########################################################
##################################################################
class Environment:
    def __init__(self, map_filepath):
        self.map_filepath = map_filepath
        self.map_surface = pygame.image.load(map_filepath).convert()
        self.width, self.height = self.map_surface.get_size()
        self.map_surface_invisible = pygame.Surface((self.width, self.height))
        self.map_surface_invisible.fill((0, 0, 0, 255))
        
        self.collision_grid = np.zeros((self.width, self.height), dtype=bool)
        for x in range(self.width):
            for y in range(self.height):
                r, g, b, _ = self.map_surface.get_at((x, y))
                if r < 128:
                    self.collision_grid[x, y] = True
    
    def is_collision(self, x: float, y: float) -> bool:
        ix, iy = int(x), int(y)
        if ix < 0 or ix >= self.width or iy < 0 or iy >= self.height:
            return True
        return self.collision_grid[ix, iy]
    
    def draw(self, screen: pygame.SurfaceType, is_map_visible:bool=True) -> None:
        if is_map_visible:
            screen.blit(self.map_surface, (0, 0))
            return None
        screen.blit(self.map_surface_invisible, (0, 0))

##################################################################
class Robot:
    def __init__(self, x: float, y: float, theta: float, sensor: Sensor):
        self.x = x
        self.y = y
        self.theta = theta
        self.radius = 10
        
        self.sensor = sensor
        self.last_scan = []
        
        self.max_v = 120.0
        self.max_w = 4.0
        
        
    def update(self, keys: pygame.constants, dt: float, env: Environment) -> tuple[float, float]:
        cmd_v = 0.0
        cmd_w = 0.0
        
        # forward/backward
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            cmd_v = self.max_v
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            cmd_v = -self.max_v / 2.0
        
        # left/right
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            cmd_w = -self.max_w
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            cmd_w = self.max_w
        
        real_v = 0.0
        real_w = cmd_w
            
        next_theta = self.theta + cmd_w * dt
        next_x = self.x + cmd_v * math.cos(next_theta) * dt
        next_y = self.y + cmd_v * math.sin(next_theta) * dt
        
        self.theta = next_theta
        if not env.is_collision(next_x, next_y):
            self.x = next_x
            self.y = next_y
            real_v = cmd_v
            
        return real_v, real_w
    
    def do_scan(self, env: Environment) -> None:
        self.last_scan = self.sensor.sense(self.x, self.y, self.theta, env)
    
    def draw(self, screen: pygame.Surface, sensor_visible: bool = False) -> None:        
        pygame.draw.circle(screen, COLOR_ROBOT, (int(self.x), int(self.y)), self.radius)
        nose_x = self.x + math.cos(self.theta) * (self.radius * 1.2)
        nose_y = self.y + math.sin(self.theta) * (self.radius * 1.2)
        pygame.draw.line(screen, COLOR_NOSE, (int(self.x), int(self.y)), (int(nose_x), int(nose_y)), 3)
        
        if not sensor_visible:
            return
        
        for d, phi in self.last_scan:
            x = self.x + d * math.cos(self.theta + phi)
            y = self.y + d * math.sin(self.theta + phi)
            pygame.draw.circle(screen, COLOR_SENSOR_MEASUREMENTS, (int(x), int(y)), 2)

##################################################################
class Sensor:
    def __init__(self, fov_degrees: int, num_rays: int, noise_std: float, max_range: float):
        self.fov = math.radians(float(fov_degrees))
        self.num_rays = num_rays
        self.noise_std = noise_std
        self.max_range = max_range
        self.last_scan = []
        
        self.__scan_step = 2.0
        
        if self.num_rays > 1:
            self.angle_increment = self.fov / (self.num_rays - 1)
        else:
            self.angle_increment = 0.0
            self.fov = 0.0
            
    def sense(self, x: float, y: float, theta: float, env: Environment) -> None:
        measurements = []
        start_angle = -(self.fov / 2.0)
        for i in range(self.num_rays):
            relative_angle = start_angle + (i * self.angle_increment)
            global_angle = theta + relative_angle
            distance = 0
            while distance <= self.max_range:
                check_x = x + distance * math.cos(global_angle)
                check_y = y + distance * math.sin(global_angle)
                
                if env.is_collision(check_x, check_y):
                    noisy_distance = distance + random.gauss(0, self.noise_std)
                    measurements.append((noisy_distance, relative_angle))
                    break
                
                distance += self.__scan_step
        
        return measurements

##################################################################
class ParticleFilter:
    def __init__(self, num_particles: int, env: Environment, start_position = None):
        self.num_particles = num_particles
        self.particles = []
        
        self.x_estimated = 0.0
        self.y_estimated = 0.0
        self.theta_estimated = 0.0
        
        self.__scan_step = 4.0
        self.__variance = 200.0
        
        self.__ratio_kept = 0.2
        self.__ratio_generated = 0.1
        self.__ratio_estimated = 0.1
        
        self.__estimate_line_thickness = 2
        self.__particle_size = 1
        
        self.num_kept = int(self.num_particles * self.__ratio_kept)
        self.num_generated = int(self.num_particles * self.__ratio_generated)
        self.num_choosed = int(self.num_particles - self.num_kept - self.num_generated)
        self.num_estimated = int(self.num_particles * self.__ratio_estimated)
        
        if sum([self.num_kept, self.num_generated, self.num_choosed]) - self.num_particles != 0:
            raise ValueError("Not 100")
        
        self.weights = [1.0 / num_particles] * num_particles
        if start_position is not None:
            init_x, init_y, init_theta = start_position
            while len(self.particles) != num_particles:
                x = random.gauss(init_x, 1)
                y = random.uniform(init_y, 1)
                if not env.is_collision(x, y):
                    theta = random.gauss(init_theta, 0.1)
                    self.particles.append((x, y, theta))
        else:
            self.particles = self._generate_random_particles(num_particles, env)
                    
    def predict(self, input_v: float, input_w: float, dt: float, env: Environment):
        new_particles = []
        for x, y, theta in self.particles:
            noisy_v = input_v + random.gauss(0, 0.1)
            noisy_w = input_w + random.gauss(0, 0.05)
            
            new_theta = theta + noisy_w * dt
            new_x = x + noisy_v * dt * math.cos(new_theta)
            new_y = y + noisy_v * dt * math.sin(new_theta)
            
            if not env.is_collision(new_x, new_y):
                new_particles.append((new_x, new_y, new_theta))
            else:
                new_particles.append((x, y, new_theta))
        
        self.particles = new_particles
    
    def update_weights(self, real_scan, sensor: Sensor, env: Environment) -> None:
        if not real_scan:
            return
        
        new_weights = []
        
        downsampled_scan = real_scan[::5]
        
        for x, y, theta in self.particles:
            score = 1.0
            particle_scan = []
            
            for real_distance, phi in downsampled_scan:
                current_distance = 0.0
                while current_distance <= sensor.max_range:
                    check_x = x + current_distance * math.cos(theta + phi)
                    check_y = y + current_distance * math.sin(theta + phi)
                    if env.is_collision(check_x, check_y):
                        particle_scan.append((current_distance, phi))
                        break
                    
                    current_distance += self.__scan_step
            
                error = abs(real_distance - current_distance)
                score *= math.exp(-(error ** 2) / self.__variance)
                
            new_weights.append(score)
            
        total = sum(new_weights)
        if total > 0:
            self.weights = [w / total for w in new_weights]
        else:
            self.weights = [1.0 / self.num_particles] * self.num_particles
    
    def resample(self, env: Environment) -> None:
        chosen_particles = random.choices(self.particles, self.weights, k=self.num_choosed)
        mutated_chosen_particles = []
        
        for x, y, theta in chosen_particles:
            new_x = x + random.gauss(0, 2)
            new_y = y + random.gauss(0, 2)
            new_theta = theta + random.gauss(0, 0.2)
            mutated_chosen_particles.append((new_x, new_y, new_theta))
        
        generated_particles = self._generate_random_particles(self.num_generated, env)
        
        paired = zip(self.particles, self.weights)
        sorted_particles = sorted(paired, key=lambda x: x[1], reverse=True)
        kept_particles = [p for p, w in sorted_particles[0:self.num_kept-1]]
        
        self.particles = mutated_chosen_particles + generated_particles + kept_particles
        
    def draw(self, screen: pygame.Surface, show_particles: bool = True, show_estimate: bool = False, radius: int = 10) -> None:
        if show_particles:
            for x, y, _ in self.particles:
                pygame.draw.circle(screen, COLOR_PARTICLES, (int(x), int(y)), self.__particle_size)
            
        if not show_estimate:
            return
        
        paired = zip(self.particles, self.weights)
        sorted_particles = sorted(paired, key=lambda x: x[1], reverse=True)
        kept_particles = [p for p, w in sorted_particles[:self.num_estimated]]
        
        sum_x = 0.0
        sum_y = 0.0
        sum_sin = 0.0
        sum_cos = 0.0
        for x, y, theta in kept_particles:
            sum_x += x
            sum_y += y
            sum_sin += math.sin(theta)
            sum_cos += math.cos(theta)
        
        avg_x = sum_x/self.num_estimated
        avg_y = sum_y/self.num_estimated
        avg_theta = math.atan2(sum_sin / self.num_estimated, sum_cos / self.num_estimated)
        
        pygame.draw.circle(screen, COLOR_ESTIMATE, (int(avg_x), int(avg_y)), radius, self.__estimate_line_thickness)
        nose_x = avg_x + math.cos(avg_theta) * (radius * 1.2)
        nose_y = avg_y + math.sin(avg_theta) * (radius * 1.2)
        pygame.draw.line(screen, COLOR_ESTIMATE, (int(avg_x), int(avg_y)), (int(nose_x), int(nose_y)), self.__estimate_line_thickness)
    
    def _generate_random_particles(self, num_particles: int, env: Environment):
        new_particles = []
        while len(new_particles) != num_particles:
                x = random.uniform(0, env.width)
                y = random.uniform(0, env.height)
                if not env.is_collision(x, y):
                    theta = random.uniform(0, 2 * math.pi)
                    new_particles.append((x, y, theta))
        return new_particles
    
    def reset_particles(self, env: Environment):
        self.particles = self._generate_random_particles(self.num_particles, env)
                
##################################################################
# MAIN ###########################################################
##################################################################
def main():
    pygame.init()
    
    print("\n ---- GAME OF PARTICLE FILTER ---- \n")
    print("Controls:")
    print("[i] reset particles")
    print("[h] show/hide estimated position")
    print("[j] show/hide sensor data")
    print("[k] show/hide particles")
    print("[l] show/hide map\n")
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Particle Filter Simulator")
    clock = pygame.time.Clock()
    
    path = os.path.join(".", "img", "map1.bmp")
    env = Environment(path)
    lidar = Sensor(360.0, 60, 0.5, 200)
    robot = Robot(x=100, y=200, theta=3, sensor=lidar)
    
    # -------- PARTICLE FILTER INIT --------
    pf = ParticleFilter(800, env, None)
    # --------------------------------------
    
    map_visible = False
    particles_visible = False
    sensor_visible = True
    estimate_visible = False
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_l]:
            map_visible = not map_visible
        elif keys[pygame.K_k]:
            particles_visible = not particles_visible
        elif keys[pygame.K_j]:
            sensor_visible = not sensor_visible
        elif keys[pygame.K_i]:
            pf.reset_particles(env)
        elif keys[pygame.K_h]:
            estimate_visible = not estimate_visible
        
        env.draw(screen, map_visible)
        
        v, w = robot.update(keys, dt, env)
        robot.do_scan(env)
        robot.draw(screen, sensor_visible)
        
        # ------ PARTICLE FILTER ALGORHITM -----
        pf.predict(v, w, dt, env)
        pf.update_weights(robot.last_scan, lidar, env)
        pf.resample(env)
        pf.draw(screen, particles_visible, estimate_visible)
        # --------------------------------------
        
        pygame.display.flip()
    
    pygame.quit()

##################################################################
if __name__ == "__main__":
    main()