import pygame
from config import *

class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.door
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(35, 384, self.width, self.height)
        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill((0, 0, 100))
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        def door_open(self):
            pass

    # def collide_player(self):
    #     hits = pygame.sprite.spritecollide(self, self.game.player, False)
    #     if hits:
    #         self.game.running = False #next level


        # def update(self):
        #     if self.game.item_aquired:
        #         self.door_open()
        #         self.player_collide()
