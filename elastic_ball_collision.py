import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Elastic Ball Collision")

# Colors
BLACK = (0, 0, 0)

# Clock for FPS control
clock = pygame.time.Clock()
FPS = 144

damping = 1.0  # Energy loss factor

# Ball class
class Ball:
    def __init__(self, x, y, radius, vx, vy):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.vy = vy
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.mass = radius ** 2  # Mass proportional to the square of the radius

    def update(self):
        global damping
        if not self.dragging:
            self.x += self.vx
            self.y += self.vy
            self.vx *= damping
            self.vy *= damping
        
        # Prevent getting stuck at borders
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = abs(self.vx)
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx = -abs(self.vx)
        
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = abs(self.vy)
        elif self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy = -abs(self.vy)

    def draw(self):
        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        max_speed = 10  # Define the speed range for color mapping
        speed = min(speed, max_speed)  # Clamp speed to max_speed
        red = int((speed / max_speed) * 255)
        blue = int((1 - speed / max_speed) * 255)
        color = (red, 0, blue)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

    def check_collision(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return distance < (self.radius + other.radius)

    def resolve_collision(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 0:
            return

        # Normalized direction
        nx = dx / distance
        ny = dy / distance

        # Relative velocity
        dvx = self.vx - other.vx
        dvy = self.vy - other.vy

        # Velocity along the normal
        dot_product = dvx * nx + dvy * ny
        if dot_product > 0:
            return

        # Elastic collision response
        m1, m2 = self.mass, other.mass
        factor = (2 * m2 / (m1 + m2)) * dot_product
        self.vx -= factor * nx
        self.vy -= factor * ny

        factor = (2 * m1 / (m1 + m2)) * dot_product
        other.vx += factor * nx
        other.vy += factor * ny

# Initialize 15 balls of equal size with random positions and velocities
balls = []
radius = 40
for _ in range(15):
    x = random.randint(radius, WIDTH - radius)
    y = random.randint(radius, HEIGHT - radius)
    vx = random.uniform(-5, 5)
    vy = random.uniform(-5, 5)
    balls.append(Ball(x, y, radius, vx, vy))

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in balls:
                if math.sqrt((event.pos[0] - ball.x) ** 2 + (event.pos[1] - ball.y) ** 2) <= ball.radius:
                    ball.dragging = True
                    ball.offset_x = event.pos[0] - ball.x
                    ball.offset_y = event.pos[1] - ball.y
        elif event.type == pygame.MOUSEBUTTONUP:
            for ball in balls:
                ball.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            for ball in balls:
                if ball.dragging:
                    target_x = event.pos[0] - ball.offset_x
                    target_y = event.pos[1] - ball.offset_y
                    ball.vx = (target_x - ball.x) * 0.5  # Elastic dragging
                    ball.vy = (target_y - ball.y) * 0.5
                    ball.x += ball.vx
                    ball.y += ball.vy
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                damping = 0.98  # Reduce energy when space is pressed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                damping = 1.0  # Restore normal motion

    # Update and draw balls
    for ball in balls:
        ball.update()
        ball.draw()

    # Check and resolve collisions between all balls
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if balls[i].check_collision(balls[j]):
                balls[i].resolve_collision(balls[j])

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
