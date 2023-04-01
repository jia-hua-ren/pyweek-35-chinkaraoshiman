import pygame
from config import *


class Shadow(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.shadow
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(32, 143, self.width, self.height)
        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill((0, 0, 100))
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y