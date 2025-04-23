import pygame 

pygame.init() 

a = pygame.display.set_mode((400, 400)) 

b= False 

x=200 

y=200 

pygame.draw.circle(a, "yellow", (x, y), 40 ) 

while not b: 

    for c in pygame.event.get(): 

        if c.type == pygame.QUIT: 

            b = True 

        if c.type==pygame.KEYDOWN and c.key==pygame.K_SPACE: 

            pygame.draw.circle(a, "yellow", (x, y), 80) 

        if c.type==pygame.KEYUP: 

            a.fill('black') 

            pygame.draw.circle(a, "yellow", (x, y), 40) 

    pygame.display.update() 
