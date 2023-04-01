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
        self.max_travel = random.randint(30, 150) # enemy move back forth 7 to 30 pixels

        self.image = self.game.enemy_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(BLACK) #get transparent background

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # for the return to original function
        # self.original_x = (self.rect.x - self.max_travel, self.rect.x, self.rect.x + self.max_travel)
        # self.original_y = self.rect.y
        self.original_x_respect_player = self.x
        self.original_y_respect_player = self.y


        self.close_to_player = False
        self.can_returning_to_position = False

    def update(self):
        self.original_x_respect_player = self.x - self.game.player.delta_x
        self.original_y_respect_player = self.y - self.game.player.delta_y
        # print(self.original_x_respect_player, self.original_y_respect_player)
        # print(self.game.player.y_change)
        self.movement()
        # self.animate()
        
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def collide_blocks(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False) #check player rect and every block in the game
        #False is dont want to delete sprite when collide
        if direction == "x":
            if hits:
                if self.x_change > 0: #moving right
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
        if direction == "y":
            if hits:
                if self.y_change > 0: #moving down
                    self.rect.y = hits[0].rect.top - self.rect.height #hits is the block rect
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def return_original_position(self):
        angle_radians = (math.atan2(self.rect.y - self.original_y_respect_player , self.rect.x - self.original_x_respect_player))
        if(self.rect.y != self.original_y_respect_player):
            self.y_change = -1 * math.sin(angle_radians) * ENEMY_SPEED * ENEMY_CHASE_BOOST
        if(self.rect.x != self.original_x_respect_player):
            self.x_change = -1 * math.cos(angle_radians) * ENEMY_SPEED * ENEMY_CHASE_BOOST
        near_original_y = self.rect.y >= self.original_y_respect_player - 10 and self.rect.y <= self.original_y_respect_player + 10
        near_original_x = self.rect.x >= self.original_x_respect_player - 10 and self.rect.x <= self.original_x_respect_player + 10
        near_original = near_original_x and near_original_y
        if near_original:
            # print('enemy returned')
            self.can_returning_to_position = False
        # print(self.can_returning_to_position)

    def see_player(self):
        hits = pygame.Rect.colliderect(self.rect, self.game.playerAOE.rect)
        return hits and not self.game.player.shadowForm

    def movement(self):
        if self.see_player():
            self.can_returning_to_position = True
            angle_radians = (math.atan2(self.rect.y - self.game.player.y , self.rect.x - self.game.player.x))
            self.y_change = -1 * math.sin(angle_radians) * ENEMY_SPEED * ENEMY_CHASE_BOOST
            self.x_change = -1 * math.cos(angle_radians) * ENEMY_SPEED * ENEMY_CHASE_BOOST
        else:
            # at_original = self.rect.y == self.original_y and self.rect.x >= self.original_x[0] and self.rect.x <= self.original_x[2]
            at_original = self.rect.y == self.original_y_respect_player and self.rect.x == self.original_x_respect_player
            if(not at_original) and self.can_returning_to_position:
                self.return_original_position()
                
            else:
            #when the player moves its no longer at the orignal x
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
