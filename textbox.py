import pygame
from config import *
import math
import random

class Textbox(pygame.sprite.Sprite):
    def __init__(self, game):

        self.game = game
        self._layer = TEXTBOX_LAYER
        self.groups = self.game.all_sprites, self.game.textbox
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = self.game.player.rect.x
        self.y = self.game.player.rect.y
        self.width = WIN_WIDTH
        self.height = WIN_HEIGHT
        self.font = pygame.font.SysFont('Arial', 32)
        self.image = self.font.render('family and friends greetings press space to make dissapera', False, BLACK)

        # self.image = self.game.wall_spritesheet.get_sprite(0, 0, self.width, self.height)
        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()

        
        # self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    # def events(self):
    #     for event in pygame.event.get():
    #         print('event')
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_SPACE:
    #                 self.kill()
    #                 print('kill')

    def update(self):
        pygame.draw.rect(self.game.screen, WHITE, self.rect)
        pass
        # print('update')
        # self.events()
