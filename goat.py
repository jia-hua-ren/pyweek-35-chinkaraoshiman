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
        self.max_travel = random.randint(7, 30) # goat move back forth 7 to 30 pixels


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

        # check collision for walls
        self.collide_blocks()
        # ensures staying inside restricted area
        self.collide_blocks(self.game.grounds)

        self.x_change = 0
        self.y_change = 0


    def movement(self):
        if self.facing == 'left':
            self.x_change -= GOAT_SPEED
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(('right', 'up', 'down'))
                self.movement_loop = 0
                self.max_travel = random.randint(7, 30)

        elif self.facing == 'right':
            self.x_change += GOAT_SPEED
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(('left', 'up', 'down'))
                self.movement_loop = 0
                self.max_travel = random.randint(7, 30)


        elif self.facing == 'up':
            self.y_change -= GOAT_SPEED
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(('right', 'down', 'left'))
                self.movement_loop = 0
                self.max_travel = random.randint(7, 30)

        elif self.facing == 'down':
            self.y_change += GOAT_SPEED
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(('right', 'up', 'left'))
                self.movement_loop = 0
                self.max_travel = random.randint(7, 30)


        self.movement_loop += 1

    def collide_blocks(self, group = None):
        if not group:
            group = self.game.blocks
        hits = pygame.sprite.spritecollide(self, group, False) #check player rect and every block in the game
        if not hits: return False
        if hits:
            if self.x_change > 0: #moving right
                self.rect.x = hits[0].rect.left - self.rect.width
            if self.x_change < 0:
                self.rect.x = hits[0].rect.right
            if self.y_change > 0: #moving down
                self.rect.y = hits[0].rect.top - self.rect.height #hits is the block rect
            if self.y_change < 0:
                self.rect.y = hits[0].rect.bottom
        return True

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