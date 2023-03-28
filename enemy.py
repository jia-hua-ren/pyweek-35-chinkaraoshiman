import pygame
from config import *
import math
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0   

        self.facing = random.choice(['left', 'right']) 
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30) # enemy move back forth 7 to 30 pixels


        self.image = self.game.enemy_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(BLACK) #get transparent background

        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill((100, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.close_to_player = False
        # self.left_animations = [
        #     self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
        #     self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
        #     self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height)]

        # self.right_animations = [
        #     self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
        #     self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
        #     self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
        #     self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height)]        

    def update(self):
        self.movement()
        # self.animate()
        self.see_player()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def see_player(self):
        hits = pygame.Rect.colliderect(self.rect, self.game.playerAOE.rect)
        if hits and not self.game.player.hidden_in_shadow:
            self.close_to_player = True
        else:
            self.close_to_player = False
            
    def follow_player(self):
        # distance = (math.hypot(self.x  - self.game.player.x, self.y - self.game.player.y) )
        angle_radians = (math.atan2(self.rect.y - self.game.player.y , self.rect.x - self.game.player.x))

        self.rect.y -= math.sin(angle_radians) * ENEMY_SPEED * ENEMY_CHASE_BOOST
        self.rect.x -= math.cos(angle_radians)  * ENEMY_SPEED * ENEMY_CHASE_BOOST


    def movement(self):
        if self.close_to_player:
            self.follow_player()

        else:
            if self.facing == 'left':
                self.x_change -= ENEMY_SPEED
                self.movement_loop -= 1
                if self.movement_loop <= -self.max_travel:
                    self.facing = 'right'
            elif self.facing == 'right':
                self.x_change += ENEMY_SPEED
                self.movement_loop += 1
                if self.movement_loop >= self.max_travel:
                    self.facing = 'left'

    def animate(self):

        if self.facing == "left":
            if self.x_change ==0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        elif self.facing == "right":
            if self.x_change ==0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
