import pygame
import math

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Elastic Collision - Ball Cannot Pass Through Cubes")

# Colors
BLACK = (0, 0, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Circle parameters (for moving cubes)
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
RADIUS = 100  # Radius of rotation
SPEED = 0.05  # Speed of rotation
CUBE_SIZE = 20  # Size of red cubes
NUM_CUBES = 4  # Number of cubes

# Masses for elastic collision
MASS_BALL = 1  # Ball is lighter
MASS_CUBE = 3  # Cube is heavier

# Ball parameters
BALL_RADIUS = 15
ball_x, ball_y = WIDTH // 2, HEIGHT // 2 + 150  # Start position
ball_speed_x, ball_speed_y = 0, 0  # Initial velocity
ball_speed = 4  # Ball movement speed

# Initial cube angles
angles = [i * (2 * math.pi / NUM_CUBES) for i in range(NUM_CUBES)]

# Clock for FPS control
clock = pygame.time.Clock()

def elastic_collision(ball_x, ball_y, ball_vx, ball_vy, cube_x, cube_y, cube_vx, cube_vy):
    """Calculate new velocities after an elastic collision."""
    # Position difference
    dx = ball_x - cube_x
    dy = ball_y - cube_y
    dist = math.sqrt(dx ** 2 + dy ** 2)
    
    if dist == 0:
        return ball_vx, ball_vy  # Avoid division by zero
    
    # Normalized direction vector
    nx, ny = dx / dist, dy / dist
    
    # Relative velocity
    dvx, dvy = ball_vx - cube_vx, ball_vy - cube_vy
    
    # Dot product for velocity along the normal
    dot_product = dvx * nx + dvy * ny
    
    # Elastic collision formula
    impulse = (2 * MASS_CUBE * dot_product) / (MASS_BALL + MASS_CUBE)
    
    # Update ball velocity
    ball_vx -= impulse * nx
    ball_vy -= impulse * ny

    return ball_vx, ball_vy

# Main loop
running = True
while running:
    screen.fill(BLACK)  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ball movement (Arrow keys)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: ball_speed_x = -ball_speed
    if keys[pygame.K_RIGHT]: ball_speed_x = ball_speed
    if keys[pygame.K_UP]: ball_speed_y = -ball_speed
    if keys[pygame.K_DOWN]: ball_speed_y = ball_speed
    if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]): ball_speed_x = 0
    if not (keys[pygame.K_UP] or keys[pygame.K_DOWN]): ball_speed_y = 0

    # Tentative ball position
    next_ball_x = ball_x + ball_speed_x
    next_ball_y = ball_y + ball_speed_y

    # Ball rectangle for collision detection
    ball_rect = pygame.Rect(next_ball_x - BALL_RADIUS, next_ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

    # Update and draw cubes
    for i in range(NUM_CUBES):
        # Move cubes in circular path
        angles[i] += SPEED
        cube_x = CENTER_X + RADIUS * math.cos(angles[i]) - CUBE_SIZE // 2
        cube_y = CENTER_Y + RADIUS * math.sin(angles[i]) - CUBE_SIZE // 2
        cube_vx = -SPEED * RADIUS * math.sin(angles[i])  # Velocity in x-direction
        cube_vy = SPEED * RADIUS * math.cos(angles[i])   # Velocity in y-direction
        cube_rect = pygame.Rect(cube_x, cube_y, CUBE_SIZE, CUBE_SIZE)

        # Draw cube
        pygame.draw.rect(screen, RED, cube_rect)

        # Check collision before moving
        if ball_rect.colliderect(cube_rect):
            # Apply elastic collision physics
            ball_speed_x, ball_speed_y = elastic_collision(
                ball_x, ball_y, ball_speed_x, ball_speed_y,
                cube_x, cube_y, cube_vx, cube_vy
            )

            # Adjust ball position so it doesn't overlap
            overlap_x = max(0, BALL_RADIUS + CUBE_SIZE // 2 - abs(ball_x - cube_x))
            overlap_y = max(0, BALL_RADIUS + CUBE_SIZE // 2 - abs(ball_y - cube_y))
            
            if abs(ball_x - cube_x) > abs(ball_y - cube_y):
                if ball_x > cube_x:
                    ball_x += overlap_x
                else:
                    ball_x -= overlap_x
            else:
                if ball_y > cube_y:
                    ball_y += overlap_y
                else:
                    ball_y -= overlap_y

    # Update ball position only if no collision
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Keep ball inside screen boundaries
    ball_x = max(BALL_RADIUS, min(WIDTH - BALL_RADIUS, ball_x))
    ball_y = max(BALL_RADIUS, min(HEIGHT - BALL_RADIUS, ball_y))

    # Draw ball
    pygame.draw.circle(screen, YELLOW, (ball_x, ball_y), BALL_RADIUS)

    pygame.display.flip()  # Update display
    clock.tick(60)  # Limit FPS

pygame.quit()
