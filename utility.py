import pygame
from config import *
import math

def distance(x1, y1, x2, y2):
    return (math.sqrt( (x1-x2)**2 + (y1-y2)**2 ))

def load_new_image(image_path, width, height, colorkey):
    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, (width, height))
    image.set_colorkey(colorkey)
    return image

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite
    

class Text:
    def __init__(self,text,x,y,size,color):
        myFont = pygame.font.SysFont('Arial', size)
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.label = myFont.render(text, self.size, color)
    def update(self, screen):
        screen.blit(self.label, (self.x, self.y))

