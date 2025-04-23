import pygame

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Horse Animation")

background = pygame.transform.scale(pygame.image.load("images/backgroundS.jpg"), (WIDTH, HEIGHT))

horse_images_left = [pygame.image.load(f"images/horse{i}.jpg") for i in range(1, 13)]
horse_images_right = [pygame.transform.flip(img, True, False) for img in horse_images_left]

horse_x, horse_y = 100, 200
horse_speed = 5
frame = 0
direction = "left"
moving = False
clock = pygame.time.Clock()

running = True
while running:
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        horse_x -= horse_speed
        direction = "left"
        moving = True
    elif keys[pygame.K_RIGHT]:
        horse_x += horse_speed
        direction = "right"
        moving = True
    else:
        moving = False
    
    if moving:
        frame = (frame + 1) % len(horse_images_left)
    
    current_image = horse_images_right[frame] if direction == "right" else horse_images_left[frame]
    screen.blit(current_image, (horse_x, horse_y))
    
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
