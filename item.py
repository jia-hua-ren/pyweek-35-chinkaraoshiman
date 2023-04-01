import pygame
from config import *

class Item(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.item
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE / 2
        self.height = TILESIZE / 2

        self.image = self.game.terrain_spritesheet.get_sprite(184, 490, self.width, self.height)
        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill((0, 0, 100))
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    # def collide_player(self):
    #     hits = pygame.sprite.spritecollide(self, self.game.player, False)
    #     if hits:
    #         self.kill() #remove item from all sprites
    #         self.game.item_aquired = True

    # def update(self):
    #     self.collide_player()