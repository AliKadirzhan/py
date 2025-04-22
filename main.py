import pygame
import random
import math
import os
pygame.init()
WIDTH, HEIGHT = 800, 600
FPS = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nuclear Fission & Fusion Simulator")

WHITE = (255, 255, 255)
BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)

image_path = os.path.join(".venv", "images")
def load_and_scale(image_name, size):
    image = pygame.image.load(os.path.join(image_path, image_name))
    return pygame.transform.scale(image, size)

u235 = load_and_scale('u235.png', (200, 200))
u236 = load_and_scale('u236.png', (200, 200))
ba144 = load_and_scale('ba144.png', (100, 100))
kr89 = load_and_scale('kr89.png', (80, 80))
tritium = load_and_scale('tritium.png', (85, 76))
deuterium = load_and_scale('deuterium.png', (52, 75))
helium = load_and_scale('helium.png', (83, 89))
neutron_img = load_and_scale('neuteron.png', (29, 29))
fusion_neutron_img = load_and_scale('neutron2.png', (42, 42))

# Button
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)
        font = pygame.font.Font(None, 36)
        screen.blit(font.render(self.text, True, WHITE), self.rect.move(10, 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Particle
class Particle:
    def __init__(self, x, y, image, vx=0, vy=0):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx
        self.vy = vy
        self.active = True

    def move(self):
        if self.active:
            self.rect.x += self.vx
            self.rect.y += self.vy
            if self.rect.left < 0 or self.rect.right > WIDTH:
                self.vx *= -1
            if self.rect.top < 0 or self.rect.bottom > HEIGHT:
                self.vy *= -1

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)

# Fis
def fission():
    clock = pygame.time.Clock()

    neutron = Particle(50, HEIGHT // 2, neutron_img)
    u235_rect = u235.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    u236_active = False
    u236_disappear = False
    flash_timer = 0  # Flash
    wait_timer = 0  # Random delay
    waiting_for_fission = False
    fragments = []
    emitted_neutrons = []
    fission_complete = False  # Prevent multiple fission events

    while True:
        screen.fill(WHITE)

        if not u236_disappear:
            screen.blit(u236 if u236_active else u235, u235_rect)

        if neutron.active:
            neutron.move()
            neutron.draw(screen)

        handle_wasd_controls(neutron)

        # When neutron collides with U-235
        if not u236_active and neutron.active and neutron.rect.colliderect(u235_rect):
            u236_active = True
            waiting_for_fission = True
            wait_timer = random.randint(30, 90)  # 1 to 5 seconds (at 30 FPS)
            neutron.active = False  # Neutron disappears

        # Countdown for fission (after U-236 forms)
        if waiting_for_fission and wait_timer > 0:
            wait_timer -= 1

        if waiting_for_fission and wait_timer == 0 and not fission_complete:
            fission_complete = True
            waiting_for_fission = False  # Stop the waiting
            u236_disappear = True  # U-236 disappears
            flash_timer = 15  # Short flash (0.5 sec)

            # Spawn fragments & neutrons
            spawn_fission_products(u235_rect.center, fragments, emitted_neutrons)

        # Draw fragments & emitted neutrons
        for particle in fragments + emitted_neutrons:
            particle.move()
            particle.draw(screen)

        # Show bright flash after fission (for 0.5 sec)
        if flash_timer > 0:
            pygame.draw.circle(screen, YELLOW, u235_rect.center, 150)
            flash_timer -= 1

        if handle_quit():
            return

        pygame.display.flip()
        clock.tick(FPS)


# Fus
def fusion():
    clock = pygame.time.Clock()

    tritium_rect = tritium.get_rect(center=(300, 300))
    deuterium_rect = deuterium.get_rect(center=(500, 300))

    dragging = None
    fused = False
    flash_timer = 15
    helium_particle = None
    neutron_particle = None

    while True:
        screen.fill(WHITE)

        if not fused:
            screen.blit(tritium, tritium_rect)
            screen.blit(deuterium, deuterium_rect)

            if particles_collide(tritium_rect, deuterium_rect, 50):
                fused = True
                helium_particle = Particle(400, 300, helium)
                neutron_particle = Particle(400, 300, fusion_neutron_img, random.uniform(-3, 3), random.uniform(-3, 3))

        if fused:
            if flash_timer > 0:
                pygame.draw.circle(screen, YELLOW, (400, 300), 150)
                flash_timer -= 1
            else:
                helium_particle.draw(screen)
                neutron_particle.move()
                neutron_particle.draw(screen)

        dragging = handle_dragging(dragging, tritium_rect, deuterium_rect)

        if handle_quit():
            return

        pygame.display.flip()
        clock.tick(FPS)

# Helper functions
def handle_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

def handle_wasd_controls(neutron):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        neutron.rect.y -= 3
    if keys[pygame.K_s]:
        neutron.rect.y += 3
    if keys[pygame.K_a]:
        neutron.rect.x -= 3
    if keys[pygame.K_d]:
        neutron.rect.x += 3

def particles_collide(rect1, rect2, distance):
    dx = rect1.centerx - rect2.centerx
    dy = rect1.centery - rect2.centery
    return math.sqrt(dx**2 + dy**2) < distance

def handle_dragging(dragging, tritium_rect, deuterium_rect):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if tritium_rect.collidepoint(event.pos):
                return "tritium"
            elif deuterium_rect.collidepoint(event.pos):
                return "deuterium"
        elif event.type == pygame.MOUSEBUTTONUP:
            return None
        elif event.type == pygame.MOUSEMOTION:
            if dragging == "tritium":
                tritium_rect.center = event.pos
            elif dragging == "deuterium":
                deuterium_rect.center = event.pos
    return dragging

def spawn_fission_products(center, fragments, emitted_neutrons):
    for _ in range(3):
        vx, vy = random.uniform(-3, 3), random.uniform(-3, 3)
        emitted_neutrons.append(Particle(center[0], center[1], neutron_img, vx, vy))

    fragments.extend([
        Particle(center[0], center[1], ba144, random.uniform(-3, 3), random.uniform(-3, 3)),
        Particle(center[0], center[1], kr89, random.uniform(-3, 3), random.uniform(-3, 3))
    ])

# Main Menu
def main_menu():
    fission_button = Button(300, 200, 200, 50, "Fission")
    fusion_button = Button(300, 300, 200, 50, "Fusion")

    while True:
        screen.fill(WHITE)
        fission_button.draw(screen)
        fusion_button.draw(screen)

        if handle_quit():
            return False

        if pygame.mouse.get_pressed()[0]:
            if fission_button.is_clicked(pygame.mouse.get_pos()):
                fission()
            elif fusion_button.is_clicked(pygame.mouse.get_pos()):
                fusion()

        pygame.display.flip()

while main_menu():
    pass
pygame.quit()
