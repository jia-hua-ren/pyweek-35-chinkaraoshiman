import pygame
from config import *


class MapObject(pygame.sprite.Sprite):
    def __init__(self, game, x, y, images, wait_seconds):
        self.x = x
        self.y = y
        self.images = images
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.map_object
        pygame.sprite.Sprite.__init__(self, self.groups)

        
        self.width = TILESIZE
        self.height = TILESIZE

        # self.image = self.game.terrain_spritesheet.get_sprite(32, 143, self.width, self.height)
        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill((0, 0, 100))
        self.index = 0
        self.image = self.images[int(self.index)]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x * TILESIZE + TILESIZE/2, self.y * TILESIZE + TILESIZE/2)

        self.clock_cycles = 0
        self.animation_loop = 0

        self.wait_seconds = wait_seconds
        self.wait_clock_cycles = self.wait_seconds * FPS

    def update(self):
        self.clock_cycles += 1
        # print(self.clock_cycles, self.index)
        if self.clock_cycles > self.wait_clock_cycles:
            if self.index < len(self.images)-1:
                self.index += 1
            else:
                self.index = 0
            self.image = self.images[int(self.index)]
            self.clock_cycles = 0


class MapObjectStatic(pygame.sprite.Sprite):
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

        self.rect = self.image.get_rect()
        self.rect.center = (self.x * TILESIZE + TILESIZE/2, self.y * TILESIZE + TILESIZE/2)