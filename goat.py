import pygame
from config import *
import math
import random

class Goat(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.goats
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0   

        self.facing = 'left'#random.choice(['left', 'right', 'up', 'down']) 
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30) # enemy move back forth 7 to 30 pixels


        self.image = self.game.goat_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(BLACK) #get transparent background

        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill((100, 100, 30))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # self.left_animations = [
        #     self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
        #     self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
        #     self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        # self.right_animations = [
        #     self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
        #     self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
        #     self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]
        

    def update(self):
        self.movement()
        # self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        print('stuck', self.facing, self.max_travel, self.movement_loop)
        if self.facing == 'left':
            self.x_change -= GOAT_SPEED
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(('right', 'up', 'down'))
                self.movement_loop = 0
                self.max_travel = random.randint(7, 30)
                print('stuck', self.facing, self.max_travel, self.movement_loop)


        elif self.facing == 'right':
            self.x_change += GOAT_SPEED
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(('left', 'up', 'down'))
                self.movement_loop = 0
                self.max_travel = random.randint(7, 30)
                print('stuck', self.facing, self.max_travel, self.movement_loop)


        elif self.facing == 'up':
            self.y_change -= GOAT_SPEED
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(('right', 'down', 'left'))
                self.movement_loop = 0
                self.max_travel = random.randint(7, 30)
                print('stuck', self.facing, self.max_travel, self.movement_loop)

        elif self.facing == 'down':
            self.y_change += GOAT_SPEED
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(('right', 'up', 'left'))
                self.movement_loop = 0
                self.max_travel = random.randint(7, 30)
                print('stuck', self.facing, self.max_travel, self.movement_loop)


        self.movement_loop += 1


    def animate(self):

        if self.facing == "left":
            if self.x_change ==0:
                self.image = self.game.goat_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        elif self.facing == "right":
            if self.x_change ==0:
                self.image = self.game.goat_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1