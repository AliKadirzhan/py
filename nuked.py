import pygame
import random
import math
import os

pygame.init()



WIDTH, HEIGHT, FPS = 800, 600, 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nuclear Fission & Fusion Simulator")

WHITE, BLUE, YELLOW = (255, 255, 255), (173, 216, 230), (255, 255, 0)

image_path = os.path.join(".venv", "images")
def load_and_scale(image_name, size):
    return pygame.transform.scale(pygame.image.load(os.path.join(image_path, image_name)), size)

u235 = load_and_scale('u235.png', (200, 200))
u236 = load_and_scale('u236.png', (200, 200))
ba144 = load_and_scale('ba144.png', (100, 100))
kr89 = load_and_scale('kr89.png', (80, 80))
tritium = load_and_scale('tritium.png', (85, 76))
deuterium = load_and_scale('deuterium.png', (52, 75))
helium = load_and_scale('helium.png', (83, 89))
neutron_img = load_and_scale('neuteron.png', (29, 29))
fusion_neutron_img = load_and_scale('neutron2.png', (42, 42))

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect, self.text = pygame.Rect(x, y, w, h), text

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)
        screen.blit(pygame.font.Font(None, 36).render(self.text, True, WHITE), self.rect.move(10, 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Particle:
    def __init__(self, x, y, image, vx=0, vy=0):
        self.image = image
        self.rect = image.get_rect(center=(x, y))
        self.vx, self.vy, self.active = vx, vy, True

    def move(self):
        if self.active:
            self.rect.x += self.vx
            self.rect.y += self.vy
            if self.rect.left < 0 or self.rect.right > WIDTH: self.vx *= -1#BORDER COLLIDE
            if self.rect.top < 0 or self.rect.bottom > HEIGHT: self.vy *= -1

    def draw(self):
        if self.active:
            screen.blit(self.image, self.rect)

# Fission
def fission():
    clock = pygame.time.Clock()
    neutron = Particle(50, HEIGHT // 2, neutron_img)
    u235_rect = u235.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    u236_active, u236_disappear = False, False
    flash_timer, wait_timer = 0, 0
    waiting_for_fission, fission_complete = False, False
    fragments, emitted_neutrons = [], []

    font = pygame.font.Font(None, 36)


    while True:
        screen.fill(WHITE)

        instructions = font.render("Move neutron with WASD", True, (0, 0, 0))
        screen.blit(instructions, (10, 10))

        if not u236_disappear:
            screen.blit(u236 if u236_active else u235, u235_rect)

        if neutron.active:
            neutron.move()
            neutron.draw()

        handle_wasd(neutron)

        if not u236_active and neutron.active and neutron.rect.colliderect(u235_rect):
            u236_active, waiting_for_fission, neutron.active = True, True, False
            wait_timer = random.randint(30, 90)  # from 1 to 3 seconds delay

        if waiting_for_fission and wait_timer > 0:
            timer_text = font.render(f"Fission in {wait_timer // 30:.1f} seconds", True, (200, 0, 0))
            screen.blit(timer_text, (10, 40))
            wait_timer -= 1

        if waiting_for_fission and wait_timer == 0 and not fission_complete:
            fission_complete, waiting_for_fission, u236_disappear = True, False, True
            flash_timer = 15
            spawn_fission_products(u235_rect.center, fragments, emitted_neutrons)#AFTER COUNTDOWN


        for p in fragments + emitted_neutrons:
            p.move()
            p.draw()

        if flash_timer > 0:
            pygame.draw.circle(screen, YELLOW, u235_rect.center, 150)
            flash_timer -= 1

        if fission_complete:
            complete_text = font.render("Fission Complete!", True, (0, 0, 0))  # Green text
            text_rect = complete_text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
            screen.blit(complete_text, text_rect)

        if handle_quit(): return
        pygame.display.flip()
        clock.tick(FPS)

# Fusion
def fusion():
    clock = pygame.time.Clock()
    tritium_rect, deuterium_rect = tritium.get_rect(center=(300, 300)), deuterium.get_rect(center=(500, 300))
    dragging, fused, flash_timer = None, False, 15
    helium_particle, neutron_particle = None, None
    font = pygame.font.Font(None, 36)

    while True:
        screen.fill(WHITE)

        instructions = font.render("Move neutron with WASD", True, (0, 0, 0))
        screen.blit(instructions, (10, 10))

        if not fused:
            screen.blit(tritium, tritium_rect)
            screen.blit(deuterium, deuterium_rect)

            if particles_collide(tritium_rect, deuterium_rect, 50):#DISTANCE CHECK
                fused = True
                helium_particle = Particle(400, 300, helium)
                neutron_particle = Particle(400, 300, fusion_neutron_img, random.uniform(-5, 5), random.uniform(-5, 5))

        if fused:
            if flash_timer > 0:
                pygame.draw.circle(screen, YELLOW, (400, 300), 150)
                flash_timer -= 1
            else:
                helium_particle.draw()
                neutron_particle.move()
                neutron_particle.draw()

                instructions = font.render("Fusion completed", True, (0, 0, 0))
                screen.blit(instructions, (300, 550))

        dragging = handle_dragging(dragging, tritium_rect, deuterium_rect)
        if handle_quit(): return
        pygame.display.flip()
        clock.tick(FPS)


#OTHER FUNCTIONS

# Help
def handle_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

def handle_wasd(neutron):#WASD CONTROL
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: neutron.rect.y -= 3
    if keys[pygame.K_s]: neutron.rect.y += 3
    if keys[pygame.K_a]: neutron.rect.x -= 3
    if keys[pygame.K_d]: neutron.rect.x += 3

def particles_collide(r1, r2, dist):
    return math.dist((r1.centerx, r1.centery), (r2.centerx, r2.centery)) < dist#DISTANCE CHECK

def handle_dragging(dragging, tritium_rect, deuterium_rect):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if tritium_rect.collidepoint(event.pos): return "tritium"
            if deuterium_rect.collidepoint(event.pos): return "deuterium"
        elif event.type == pygame.MOUSEBUTTONUP:
            return None
        elif event.type == pygame.MOUSEMOTION:
            if dragging == "tritium": tritium_rect.center = event.pos
            if dragging == "deuterium": deuterium_rect.center = event.pos
    return dragging

def spawn_fission_products(center, fragments, emitted_neutrons):
    for _ in range(3):
        vx, vy = random.uniform(-3, 3), random.uniform(-3, 3)
        emitted_neutrons.append(Particle(center[0], center[1], neutron_img, vx, vy))

    fragments.extend([
        Particle(center[0], center[1], ba144, random.uniform(-3, 3), random.uniform(-3, 3)),
        Particle(center[0], center[1], kr89, random.uniform(-3, 3), random.uniform(-3, 3))
    ])

# MENU SWITCH
def main_menu():
    fission_button = Button(300, 200, 200, 50, "Fission")
    fusion_button = Button(300, 300, 200, 50, "Fusion")

    while True:
        screen.fill(WHITE)

        fission_button.draw()
        fusion_button.draw()

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
