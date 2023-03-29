import pygame
from config import *
import math
import random

def distance(x1, y1, x2, y2):
    return (math.sqrt( (x1-x2)**2 + (y1-y2)**2 ))


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite