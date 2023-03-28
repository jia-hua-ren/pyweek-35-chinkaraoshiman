import pygame
from config import *
import math
import random

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        # self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # self.right_animations = [
        #     self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        # self.down_animations = [
        #     self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        # self.left_animations = [
        #     self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        # self.up_animations = [
        #     self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
        #     self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print('space')
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    elif self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    elif self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    elif self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y - TILESIZE)
        # print('evet')
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print('space')
        #     if self.player.facing == 'up':
        #         Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
        #     elif self.player.facing == 'down':
        #         Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
        #     elif self.player.facing == 'left':
        #         Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
        #     elif self.player.facing == 'right':
        #         Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y - TILESIZE)

    def update(self):
        print('update')
        self.events()
        # self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True) #if collision true, kill enemy

    def animate(self):
        direction = self.game.player.facing


        
        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)] # math.floor round number down
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        elif direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)] # math.floor round number down
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        elif direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)] # math.floor round number down
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
        elif direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)] # math.floor round number down
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()