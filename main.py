import pygame
import sys
from random import getrandbits
from utility import *
from button import *
from textbox import *
from goat import *
from attack import *
from ground import *
from shadow import *
from player import *
from enemy import *
from block import *
from config import *
from levels import *
from item import *
from door import *
from slideshow import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init()
        self.bgm = pygame.mixer.music.load('./assets/music/goat2.ogg')
        pygame.mixer.music.play(-1)
        self.running = True
        self.FullScreen = False

        self.state = 'title'

        self.level = 0
        self.level_description = level_descrip[0]
        self.level_clear = False

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 32)

        self.character_spritesheet = Spritesheet('./assets/img/player_spritesheet.png')
        self.goat_spritesheet = Spritesheet('./assets/img/goat_spritesheet.png')
        self.terrain_spritesheet = Spritesheet('./assets/img/ground.png')
        self.enemy_spritesheet = Spritesheet('./assets/img/enemy.png')
        self.wall_spritesheet = Spritesheet('./assets/img/wall.png')
        self.shadow_spritesheet = Spritesheet('./assets/img/shadow.png')
        self.door_spritesheet = Spritesheet('./assets/img/door.png')
        self.item_spritesheet = Spritesheet('./assets/img/item.png')
        # self.attack_spritesheet = Spritesheet('img/attack.png')
        self.bg_img = pygame.image.load('./assets/img/bg.png').convert_alpha()

        self.F1 = load_new_image('./assets/img/Goat1/Goast1_MoveF_1.png', 100, 100, WHITE)
        self.F2 = load_new_image('./assets/img/Goat1/Goast1_MoveF_2.png', 100, 100, WHITE)
        self.B1 = load_new_image('./assets/img/Goat1/Goat1_MoveB_1.png', 100, 100, WHITE)
        self.B2 = load_new_image('./assets/img/Goat1/Goat1_MoveB_2.png', 100, 100, WHITE)
        self.L1 = load_new_image('./assets/img/Goat1/Goat1_MoveL_1.png', 100, 100, WHITE)
        self.L2 = load_new_image('./assets/img/Goat1/Goat1_MoveL_2.png', 100, 100, WHITE)
        self.R1 = load_new_image('./assets/img/Goat1/Goat1_MoveR_1.png', 100, 100, WHITE)
        self.R2 = load_new_image('./assets/img/Goat1/Goat1_MoveR_2.png', 100, 100, WHITE)


        self.intro_background = pygame.image.load('./assets/img/bg_copy.png').convert_alpha()
        self.go_background = self.bg_img
        self.backTexture = load_new_image('./assets/img/backTexture.png', 1280, 150, WHITE)

        self.item_aquired = False

        self.intro_images = [
            pygame.image.load(intro_images[0]).convert_alpha(),
            pygame.image.load(intro_images[1]).convert_alpha(),
            pygame.image.load(intro_images[2]).convert_alpha(),
            pygame.image.load(intro_images[3]).convert_alpha(),
            pygame.image.load(intro_images[4]).convert_alpha()
        ]

    def createTilemap(self, level):
        # j is x position
        # i is the y position
        for i, row in enumerate(level):
            for j, column in enumerate(row):
                if column == ".": #normal ground
                    Ground(self, j, i)
                if column == "R": #restricted move area
                    Ground(self, j, i, True)
                if column == "B": #block wall
                    Ground(self, j, i)
                    Block(self, j, i)
                if column == "S": #shadow 
                    Ground(self, j, i)
                    Shadow(self, j, i)
                if column == "D": #goal, exit, door
                    Ground(self, j, i, True)
                    Door(self, j, i)
                if column == "I": # item/ key
                    Ground(self, j, i, True)
                    self.item_object = Item(self, j, i)
                    
                # moving objects by default should have restricted
                # area under them
                if column == "G": # goat
                    Ground(self, j, i, True)
                    if getrandbits(1):
                        Goat(self, j, i, 1)
                    else:
                        Goat(self, j, i, 0)
                if column == "E": #enemy
                    Ground(self, j, i, True)
                    Enemy(self, j, i)
                # if column == "P": #player
                #     self.player = Player(self, j , i)
                #     # Attack(self, j, i)
        self.player = Player(self, WIN_HEIGHT/2 , WIN_WIDTH/2)
        self.playerAOE = PlayerAOE(self, self.player.x, self.player.y)

    def new(self):
        print('newgame')
        # a new game starts
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.item = pygame.sprite.LayeredUpdates()
        self.door = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.grounds = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.playerAOE = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.goats = pygame.sprite.LayeredUpdates()
        self.shadow = pygame.sprite.LayeredUpdates()
        self.textbox = pygame.sprite.LayeredUpdates()
        # self.intro_screen()
        
        #self.createTilemap()
        #Textbox(self, self.level_description, len(self.level_description))

    def levelUpdate(self):
        # zeroth "level" (intro screen)
        if self.level_clear:
            self.level += 1
            self.level_clear = False

        if self.level >= len(levels):
            # insert real game over screen
            pygame.quit()
            sys.exit()
        
        # else don't change level
        for sprite in self.all_sprites:
            sprite.kill()
        self.createTilemap(levels[self.level])
        Textbox(self, level_descrip[self.level], len(level_descrip[self.level]))
            
    def update(self): # make things move
        # game loop updates        
        self.all_sprites.update() #find update function/method in every sprite and update it        

    def draw(self): # draw sprites on screen
        self.screen.fill(BLACK)
        self.screen.blit(self.bg_img, (0, 0))
        self.all_sprites.draw(self.screen) # sprite group draw method
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # game loop
        self.events()
        self.update()
        self.draw()
        pygame.display.set_caption("current FPS: "+str(self.clock.get_fps()))
        # pygame.quit()
        # sys.exit()
        # self.running = False

    def events(self): # key presses and stuff
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('done')
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                if self.FullScreen:#if already fullscreen go to windowed
                    pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
                    self.FullScreen = False
                else: # if windowed, go to fullscreen
                    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    self.FullScreen = True
                # pygame.quit()
                # self.playing = False
                # self.running = False

    def game_over(self):
        # print('death')

        gameover = True

        for sprite in self.all_sprites:
            sprite.kill()

        text = self.font.render('you die', False, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'restart', 32)

        while gameover:
            self.events()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                gameover = False
                self.state = 'game'
                self.level_clear = False
                self.levelUpdate()
            
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_anime(self):

        intro_cutscene = Slideshow(intro_text, self.intro_images, self.screen)

        intro_done = intro_cutscene.stop
        # intro = True
        # print(intro_done)

        title = self.font.render('rpg tutorial', False, BLACK)
        title_rect = title.get_rect(x=10, y=10)
        
        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)

        while not intro_done:
            # print(intro_done)
            intro_done = intro_cutscene.stop
            # print(intro_done)
            self.events()

            # mouse_pos = pygame.mouse.get_pos()
            # mouse_pressed = pygame.mouse.get_pressed()

            if intro_done == True:
                intro_done = True
                self.state = 'game'
                self.level_clear = True
                self.levelUpdate()
            
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            intro_cutscene.update()
            self.clock.tick(FPS)


            pygame.display.update()
        # intro_done = True
        # self.level_clear = True
        # self.state = 'game'
        # self.levelUpdate()

    def intro_screen(self):

        intro_done = False
        # intro = True

        title = self.font.render('rpg tutorial', False, BLACK)
        title_rect = title.get_rect(x=10, y=10)
        
        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)

        while not intro_done:
            self.events()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro_done = True
                self.state = 'intro'
            
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)


            pygame.display.update()

        

    def cutscene(self):
        # print('death')

        cutscene = True

        for sprite in self.all_sprites:
            sprite.kill()

        text = self.font.render('cutscene', False, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        next_level_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'next level', 32)

        while cutscene:
            self.events()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if next_level_button.is_pressed(mouse_pos, mouse_pressed):
                self.level_clear = True
                self.item_aquired = False
                self.levelUpdate()
                cutscene = False
                self.state = 'game'

            
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(next_level_button.image, next_level_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def state_manager(self):
        # print(self.state)
        if self.state == 'game':
            self.main()
        elif self.state == 'title':
            self.intro_screen()
        elif self.state == 'intro':
            self.intro_anime()
        elif self.state == 'lose':
            self.game_over()
        elif self.state == 'cutscene':
            self.cutscene()
        

        
# class GameStateController:
#     # control what level or state
#     # the game is in
#     # ex: intro --> menu -->
#     # lvl1 --> lvl2 --> lvl3
#     def __init__(self):
#         self.state = 'main_game'

g = Game()
# g.intro_screen()
g.new()
while g.running:
    g.state_manager()
    # pygame.quit()

pygame.quit()
sys.exit()