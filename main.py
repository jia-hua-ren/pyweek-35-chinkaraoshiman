import pygame
import sys
import os

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()            #get a pygame clock object
running = True
dt=0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    pygame.display.flip()
    dt = clock.tick(60) / 1000


pygame.quit()