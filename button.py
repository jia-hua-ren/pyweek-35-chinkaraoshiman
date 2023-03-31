import pygame
from config import *
from utility import *

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        """self, x, y, width, height, fg, bg, content, fontsize)"""
        self.font = pygame.font.Font(FONT_PATH, fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg =fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height)) 
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.center = (self.x, self.y)

        self.text = self.font.render(self.content, False, self.fg) #false antialiasing
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False