import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.delta_x = 0
        self.delta_y = 0

        self.shadowForm = False

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.screen_width = 13 * TILESIZE * 0.5 - TILESIZE/2
        self.screen_height = 7.3 * TILESIZE * 0.5 - TILESIZE/2

        self.x = self.screen_width#WIN_WIDTH * TILESIZE * 0
        self.y = self.screen_height#WIN_HEIGHT * TILESIZE * 0
        self.width = TILESIZE/2
        self.height = TILESIZE/2

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 0

        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.animations = [
            self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(51, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height),
            self.game.character_spritesheet.get_sprite(51, 0, self.width, self.height)
        ]

        self.animations_shadow = [
            self.game.character_spritesheet.get_sprite(0, 52, self.width, self.height),
            self.game.character_spritesheet.get_sprite(51, 52, self.width, self.height),
            self.game.character_spritesheet.get_sprite(0, 52, self.width, self.height),
            self.game.character_spritesheet.get_sprite(51, 52, self.width, self.height)
        ]

    def update(self): # pygame sprite manditory function
        self.movement()
        self.animate()
        
        # keys = pygame.key.get_pressed()
        if self.shadow_condition(): #and keys[pygame.K_h]:
            # Turn into shadow on H key hold
            # need to decide between toggle or hold
            self.shadowForm = True
            # Red for now for testing purposes
            # self.image.fill((255, 0, 0))
        else:
            self.shadowForm = False
            # self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)
            self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.collide_door()
        self.collide_item()

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
        #used for enemy return to position
        self.delta_x += self.x_change
        self.delta_y += self.y_change
        # print(self.x_change, self.y_change, self.delta_x, self.delta_y)

    def shadow_condition(self):
        callable = pygame.sprite.collide_rect_ratio(1)
        
        # Get the sprites that the player sprite is touching
        touchingShadowSprites = pygame.sprite.spritecollide(self, self.game.shadow, False, callable)
        touchingGoatSprites = pygame.sprite.spritecollide(self, self.game.goats, False, callable)

        newShadowRect = pygame.Rect(0,0,0,0)
        newGoatsRect = pygame.Rect(0,0,0,0)

        if touchingShadowSprites:
            # make the bigger shadow rect
            for shadows in touchingShadowSprites:
                if not newShadowRect:
                    newShadowRect = shadows.rect
                else:
                    newShadowRect = pygame.Rect.union(newShadowRect, shadows.rect)
        if touchingGoatSprites:
            # make the bigger goats rect
            for goats in touchingGoatSprites:
                if not newGoatsRect:
                    newGoatsRect = goats.rect
                else:
                    newGoatsRect = pygame.Rect.union(newGoatsRect, goats.rect)

        newShadowRect = newShadowRect.scale_by(1.2)
        newGoatsRect = newGoatsRect.scale_by(1.2)

        if newShadowRect and newGoatsRect:
            return pygame.Rect.contains(newShadowRect, self.rect) or pygame.Rect.contains(newGoatsRect, self.rect)
        elif newShadowRect:
            return pygame.Rect.contains(newShadowRect, self.rect)
        elif newGoatsRect:
            return pygame.Rect.contains(newGoatsRect, self.rect)
        else:
            return False

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.game.state = 'lose'
            self.kill() #remove player from all sprites
            # self.game.running = False
            # self.game.playing = False #exit game

    def collide_item(self):
        hits = pygame.sprite.spritecollide(self, self.game.item, False)
        if hits:
            if not hits[0].gdp:
                self.game.item_aquired = True
            else:
                hits[0].item_popup()
                # text screen
            hits[0].kill() #remove item from all sprites
            

    def collide_door(self):
        hits = pygame.sprite.spritecollide(self, self.game.door, False)
        if hits and self.game.item_aquired:
            # print(self.game.playing)
            # self.game.playing = False
            self.game.state = 'cutscene'
            # self.game.level_clear = True
            # self.game.item_aquired = False
           
            # self.game.levelUpdate()
            #pygame.sprite.spritecollide(self, self.game.door, True)
            # self.game.running = False #next level
        else:
            self.collide_blocks('x', self.game.door)
            self.collide_blocks('y', self.game.door)

    def collide_blocks(self, direction, group = None):
        if not group:
            group = self.game.blocks
        hits = pygame.sprite.spritecollide(self, group, False) #check player rect and every block in the game
        #False is dont want to delete sprite when collide
        if direction == "x":
            if hits:
                if self.x_change > 0: #moving right
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
        if direction == "y":
            if hits:
                if self.y_change > 0: #moving down
                    self.rect.y = hits[0].rect.top - self.rect.height #hits is the block rect
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
    def animate(self):
        keys = pygame.key.get_pressed()

        if self.shadowForm:
            self.image = self.animations_shadow[int(self.animation_loop)]
        else:
            self.image = self.animations[int(self.animation_loop)]
        
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.animation_loop += 0.1

        if self.animation_loop > len(self.animations):
            self.animation_loop = 0

class PlayerAOE(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE * 6
        self.height = TILESIZE * 6

        self.image = pygame.Surface([self.width, self.height])
        # self.image.fill((255, 0, 0))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.center = self.game.player.rect.center

    def update(self): # pygame sprite manditory function
        self.movement()
        # self.collide_enemy()

    def movement(self):
        self.rect.center = self.game.player.rect.center

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            print("aoe")
            self.kill() #remove player from all sprites
            # self.game.playing = False #exit game