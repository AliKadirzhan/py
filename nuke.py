import pygame
import random
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nuclear Fission Simulation")
clock = pygame.time.Clock()

# Define colors
GREY = (128, 128, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)

class Neutron:
    def __init__(self, pos, velocity=(0, 0), source="player"):
        self.pos = [float(pos[0]), float(pos[1])]
        self.vel = [float(velocity[0]), float(velocity[1])]
        self.mass = 1
        self.radius = 10
        self.color = GREY
        self.alive = True
        self.source = source  # "player" or "emitted"

    def update(self, dt):
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        # Keep within screen bounds
        if self.pos[0] < self.radius: self.pos[0] = self.radius
        if self.pos[0] > WIDTH - self.radius: self.pos[0] = WIDTH - self.radius
        if self.pos[1] < self.radius: self.pos[1] = self.radius
        if self.pos[1] > HEIGHT - self.radius: self.pos[1] = HEIGHT - self.radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)

class Core:
    def __init__(self, pos, velocity=(0, 0), composition=None):
        self.pos = [float(pos[0]), float(pos[1])]
        self.vel = [float(velocity[0]), float(velocity[1])]
        # If no composition is provided, generate a nucleus with 40-100 nuclons.
        if composition is None:
            num_nuclons = random.randint(40, 100)
            # Create a larger nucleus by scaling up the cluster radius
            base_cluster = 10 + math.sqrt(num_nuclons) * 5
            cluster_radius = base_cluster * 1.5  # scaling factor for bigger uranium atom
            self.composition = []
            # Use the sunflower algorithm for an even, round distribution.
            golden_angle = math.pi * (3 - math.sqrt(5))
            for i in range(num_nuclons):
                r = math.sqrt(i / num_nuclons) * cluster_radius
                theta = i * golden_angle
                offset_x = int(r * math.cos(theta))
                offset_y = int(r * math.sin(theta))
                color = RED if i % 2 == 0 else GREY
                self.composition.append((offset_x, offset_y, color))
        else:
            # For fission products, use the provided composition directly.
            self.composition = composition
        self.base_radius = 10  # Each nucleon is drawn with this radius
        self.dragging = False
        self.alive = True
        self.decay_time = None  # In milliseconds

    def get_mass(self):
        # Mass is the number of nuclons
        return len(self.composition)

    def update(self, dt):
        if not self.dragging:
            self.pos[0] += self.vel[0] * dt
            self.pos[1] += self.vel[1] * dt
        r = self.bounding_radius()
        if self.pos[0] < r:
            self.pos[0] = r
            self.vel[0] *= -1
        if self.pos[0] > WIDTH - r:
            self.pos[0] = WIDTH - r
            self.vel[0] *= -1
        if self.pos[1] < r:
            self.pos[1] = r
            self.vel[1] *= -1
        if self.pos[1] > HEIGHT - r:
            self.pos[1] = HEIGHT - r
            self.vel[1] *= -1

        # Decay: after the set timer, split the nucleus into two smaller fragments.
        if self.decay_time is not None and pygame.time.get_ticks() >= self.decay_time:
            explosions.append(Explosion(self.pos))
            total_nuclons = len(self.composition)
            # Using approximate ratios for Kr-89 and Ba-144 (89:144 ~ 89/233 and 144/233)
            ratio_kr = 89 / 233.0
            count_kr = round(total_nuclons * ratio_kr)
            count_ba = total_nuclons - count_kr
            random.shuffle(self.composition)
            composition_kr = self.composition[:count_kr]
            composition_ba = self.composition[count_kr:]
            # Scale down the nucleon offsets to make the fragments appear tighter.
            scale_factor = 0.5  # Adjust this value as needed
            composition_kr = [(int(off_x * scale_factor), int(off_y * scale_factor), color)
                              for (off_x, off_y, color) in composition_kr]
            composition_ba = [(int(off_x * scale_factor), int(off_y * scale_factor), color)
                              for (off_x, off_y, color) in composition_ba]
            angle = random.uniform(0, 2 * math.pi)
            speed = 80 * 1.5  # 50% faster movement for the fragments
            vel1 = [speed * math.cos(angle), speed * math.sin(angle)]
            vel2 = [-speed * math.cos(angle), -speed * math.sin(angle)]
            core1 = Core(self.pos, velocity=vel1, composition=composition_kr)
            core2 = Core(self.pos, velocity=vel2, composition=composition_ba)
            cores.append(core1)
            cores.append(core2)
            # Emit three new neutrons with random velocities.
            for _ in range(3):
                angle_n = random.uniform(0, 2 * math.pi)
                speed_n = 100 * 1.5
                vel_n = [speed_n * math.cos(angle_n), speed_n * math.sin(angle_n)]
                neutrons.append(Neutron(self.pos, velocity=vel_n, source="emitted"))
            self.alive = False

    def draw(self, surface):
        for off_x, off_y, color in self.composition:
            pos = (int(self.pos[0] + off_x), int(self.pos[1] + off_y))
            pygame.draw.circle(surface, color, pos, self.base_radius)
        # Uncomment to see the bounding circle:
        # pygame.draw.circle(surface, (0,255,0), (int(self.pos[0]), int(self.pos[1])), int(self.bounding_radius()), 1)

    def bounding_radius(self):
        max_dist = 0
        for off_x, off_y, _ in self.composition:
            d = math.hypot(off_x, off_y)
            if d > max_dist:
                max_dist = d
        return max_dist + self.base_radius

class Explosion:
    def __init__(self, pos):
        self.pos = [float(pos[0]), float(pos[1])]
        self.radius = 200
        self.duration = 500  # milliseconds
        self.start_time = pygame.time.get_ticks()
        self.alive = True

    def update(self):
        if pygame.time.get_ticks() - self.start_time > self.duration:
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (int(self.pos[0]), int(self.pos[1])), self.radius)

# Initialize objects: one controllable neutron and one draggable core.
neutron = Neutron((100, HEIGHT // 2))
cores = [Core((WIDTH // 2, HEIGHT // 2))]
neutrons = [neutron]
explosions = []

# Movement parameters
acceleration = 75
neutron_speed_limit = 100

# For mouse dragging
drag_offset = (0, 0)
dragging_core = None

running = True
while running:
    dt = clock.tick(60) / 1000.0  # Seconds per frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse dragging for cores
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for core in cores:
                dx = mouse_pos[0] - core.pos[0]
                dy = mouse_pos[1] - core.pos[1]
                if math.hypot(dx, dy) <= core.bounding_radius():
                    core.dragging = True
                    dragging_core = core
                    drag_offset = (core.pos[0] - mouse_pos[0], core.pos[1] - mouse_pos[1])
                    break
        if event.type == pygame.MOUSEBUTTONUP:
            if dragging_core:
                dragging_core.dragging = False
                dragging_core = None

        # Keyboard control for the player neutron (WASD)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                neutron.vel[1] -= acceleration
            if event.key == pygame.K_s:
                neutron.vel[1] += acceleration
            if event.key == pygame.K_a:
                neutron.vel[0] -= acceleration
            if event.key == pygame.K_d:
                neutron.vel[0] += acceleration

    if dragging_core:
        mpos = pygame.mouse.get_pos()
        dragging_core.pos[0] = mpos[0] + drag_offset[0]
        dragging_core.pos[1] = mpos[1] + drag_offset[1]

    # Update neutrons
    for n in neutrons:
        if n.alive:
            n.update(dt)

    # Update cores and check for decay/split
    for core in cores:
        if core.alive:
            core.update(dt)

    # Check collisions: only player neutron is absorbed by cores.
    for core in cores:
        if core.alive:
            for n in neutrons:
                if n.alive and n.source != "emitted":
                    dx = n.pos[0] - core.pos[0]
                    dy = n.pos[1] - core.pos[1]
                    distance = math.hypot(dx, dy)
                    if distance < (core.bounding_radius() + n.radius):
                        total_mass = core.get_mass() + n.mass
                        new_vel_x = 1.5 * ((core.get_mass() * core.vel[0] + n.mass * n.vel[0]) / total_mass)
                        new_vel_y = 1.5 * ((core.get_mass() * core.vel[1] + n.mass * n.vel[1]) / total_mass)
                        core.vel = [new_vel_x, new_vel_y]
                        angle_offset = random.uniform(0, 2 * math.pi)
                        offset_distance = core.bounding_radius()
                        offset_x = int(offset_distance * math.cos(angle_offset))
                        offset_y = int(offset_distance * math.sin(angle_offset))
                        core.composition.append((offset_x, offset_y, GREY))
                        if core.decay_time is None:
                            delay = random.randint(2000, 10000)
                            core.decay_time = pygame.time.get_ticks() + delay
                        n.alive = False

    # Update explosions
    for exp in explosions:
        exp.update()

    # Remove dead objects
    neutrons = [n for n in neutrons if n.alive]
    cores = [c for c in cores if c.alive]
    explosions = [e for e in explosions if e.alive]

    screen.fill(BACKGROUND_COLOR)
    for n in neutrons:
        n.draw(screen)
    for core in cores:
        core.draw(screen)
    for exp in explosions:
        exp.draw(screen)
    pygame.display.flip()

pygame.quit()
