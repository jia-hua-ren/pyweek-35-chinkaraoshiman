import pygame
import sys
import os

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()            #get a pygame clock object
running = True

dt=0

x, y = 0, 0 #starting position
i = 1 #x direction pointing right
j = 1 #y direction pointing down
speed = 5
width = 100
screen.fill("white")
color = (x%249,x%249,x%249)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    if x <= 0:
        i = 1
    elif x >= 640-width:
        i = -1
    else:
        i = i
    
    if y <= 0:
        j = 1
    elif y >= 480-width:
        j = -1
    else:
        j = j
        
    x+=speed*i
    y+=speed*j
    speed+=1*i
    color = (x%249,y%249,(x*y)%249)

    pygame.draw.rect(screen,color,(x,y,width,width))

    pygame.display.flip()
    dt = clock.tick(60) / 1000


pygame.quit()