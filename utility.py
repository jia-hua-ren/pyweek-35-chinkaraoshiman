import pygame
from config import *
# import math

# def distance(x1, y1, x2, y2):
#     return (math.sqrt( (x1-x2)**2 + (y1-y2)**2 ))

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
    def __init__(self,text,pos,size,color,do_bg):
        self.do_bg = do_bg
        self.myFont = pygame.font.Font(FONT_PATH, size)
        self.pos = pos
        self.size = size
        self.text = text
        self.color = color
        self.label = self.myFont.render(self.text, self.size, color)
        self.rect = self.label.get_rect()
        self.rect.center = self.pos
        #background
        if self.do_bg:
            self.bg= pygame.Surface(self.rect.size)
            self.bg.fill(BLACK)
    def update(self, text):
        self.label = self.myFont.render(text, self.size, self.color)
        self.rect = self.label.get_rect()
        self.rect.center = self.pos
        self.bg= pygame.Surface(self.rect.size)
        if self.do_bg:
            self.bg.fill(BLACK)
    def draw(self,screen):
        if self.do_bg:
            screen.blit(self.bg, self.rect)
        screen.blit(self.label, self.rect)

