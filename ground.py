import pygame
from config import *

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y, restricted = False, type = 'ground'):
        # determine if this block is part of restricted area.
        # defaults false.
        self.restricted = restricted

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        if not restricted:
            self.groups = self.game.all_sprites, self.game.grounds

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        # self.image = pygame.Surface([self.width, self.height])
        self.type = type #determine the type of ground image

        if self.type == 'grass':
            self.image = self.game.terrain_spritesheet.get_sprite(36, 647, self.width, self.height)
        elif self.type == 'metal':
            self.image = self.game.terrain_spritesheet.get_sprite(183, 23, self.width, self.height)
        elif self.type == 'ground':
            #default is the sandy dirt
            self.image = self.game.terrain_spritesheet.get_sprite(30, 23, self.width, self.height)
        # self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        
