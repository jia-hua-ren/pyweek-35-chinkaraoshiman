import pygame
from config import *


class MapObject(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.map_object
        pygame.sprite.Sprite.__init__(self, self.groups)

        
        self.width = TILESIZE
        self.height = TILESIZE

        # self.image = self.game.terrain_spritesheet.get_sprite(32, 143, self.width, self.height)
        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill((0, 0, 100))
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.x * TILESIZE + TILESIZE/2, self.y * TILESIZE + TILESIZE/2)