import pygame 

 

pygame.init() 

 

screen_size = 400 

screen = pygame.display.set_mode((screen_size, screen_size)) 

pygame.display.set_caption('Bouncing Circle') 

 

background_color = 'black' 

circle_color = 'yellow' 

 

circle_radius = 20 

y = circle_radius 

speed = 5 

direction = 1 

 

running = True 

while running: 

    for event in pygame.event.get(): 

        if event.type == pygame.QUIT: 

            running = False 

 

    y += speed * direction 

 

    if y >= screen_size - circle_radius or y <= circle_radius: 

        direction *= -1 

 

    screen.fill(background_color) 

    pygame.draw.circle(screen, circle_color, (screen_size // 2, y), circle_radius) 

    pygame.display.update() 

    pygame.time.Clock().tick(60) 

 

pygame.quit() 
