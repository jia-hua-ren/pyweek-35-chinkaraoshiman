import pygame
from config import *
from utility import *

class Textbox(pygame.sprite.Sprite):
    def __init__(self, game, text_list, size, clock):
        self.clock = clock
        self.text_list = text_list #all diologues to go through
        self.text_index = 0
        self.size = size - 1 # find maximum index for text_list

        self.game = game
        self._layer = TEXTBOX_LAYER
        self.groups = self.game.all_sprites, self.game.textbox
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = self.game.player.rect.x
        self.y = WIN_HEIGHT * 0.75
        self.width = WIN_WIDTH
        self.height = WIN_HEIGHT
        self.font = pygame.font.Font(FONT_PATH, 32)
        self.image = self.font.render(self.text_list[self.text_index], False, BLACK, RED)

        # self.image = self.game.wall_spritesheet.get_sprite(0, 0, self.width, self.height)
        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()

        
        # self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.kill_on_release = False

        self.wait_seconds = 3.5
        self.wait_clock_cycles = FPS * self.wait_seconds
        self.clock_cycles = 0

    def events(self):
        key_pressed = pygame.key.get_pressed() 

        if key_pressed[pygame.K_SPACE]:
            self.kill_on_release = True
        elif self.kill_on_release == True and not key_pressed[pygame.K_SPACE]:
            # self.kill()
            if self.text_index == self.size:
                self.kill()
            else:
                self.text_index += 1
                self.image = self.font.render(self.text_list[self.text_index], False, BLACK, RED)
                self.rect = self.image.get_rect()
                self.kill_on_release = False

        if self.clock_cycles > self.wait_clock_cycles:
            if self.text_index == self.size:
                self.kill()
            else:
                self.text_index += 1
                self.image = self.font.render(self.text_list[self.text_index], False, BLACK, RED)
                self.rect = self.image.get_rect()
            self.clock_cycles = 0

    def update(self):
        self.events()
        self.rect.center = (self.game.player.rect.x, self.y)

        pygame.draw.rect(self.game.screen, WHITE, self.rect)

        self.clock_cycles += 1
        # self.clock.tick(FPS)
