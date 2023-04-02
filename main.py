import pygame
from sys import exit
from random import getrandbits
from utility import *
from button import *
from textbox import *
from goat import *
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
from fadein import *
from mapobject import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init()
        self.bgm = pygame.mixer.music.load('./assets/music/goat2.ogg')
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)
        self.can_switch_music = True
        self.running = True
        self.FullScreen = False

        self.state = 'title'

        self.level = 0
        self.level_description = level_descrip[0]
        self.level_clear = False
        self.cutscene_level = 0


        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_PATH, 32)

        self.character_spritesheet = Spritesheet('./assets/img/player_spritesheet.png')
        self.goat_spritesheet = Spritesheet('./assets/img/goat_spritesheet.png')
        self.terrain_spritesheet = Spritesheet('./assets/img/terrain_spritesheet.png')
        self.enemy_spritesheet = Spritesheet('./assets/img/enemy.png')
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
        # self.backTexture = load_new_image('./assets/img/backTexture.png', 1280, 150, WHITE)

        self.item_aquired = False

        self.intro_images = [
            pygame.image.load(intro_images[0]).convert_alpha(),
            pygame.image.load(intro_images[1]).convert_alpha(),
            pygame.image.load(intro_images[2]).convert_alpha(),
            pygame.image.load(intro_images[3]).convert_alpha(),
            pygame.image.load(intro_images[4]).convert_alpha()
        ]

        self.bg_intro_images = [
            pygame.image.load(intro_images[0]).convert_alpha(),
            pygame.image.load(intro_images[1]).convert_alpha(),
            pygame.image.load(intro_images[2]).convert_alpha(),
            pygame.image.load(intro_images[3]).convert_alpha(),
            pygame.image.load(intro_images[4]).convert_alpha()
        ]

        self.ending_images = [
            pygame.image.load(end_images[0]).convert_alpha(),
            pygame.image.load(end_images[1]).convert_alpha(),
            pygame.image.load(end_images[2]).convert_alpha()
        ]

        self.bg_ending_images = [
            pygame.image.load(end_images[0]).convert_alpha(),
            pygame.image.load(end_images[1]).convert_alpha(),
            pygame.image.load(end_images[2]).convert_alpha()
        ]

        self.end_img = pygame.image.load('./assets/img/ending/endingscene5.png').convert_alpha()
        self.FinalEnd= Fadein(self.end_img, WIN_CENTER, 0.5, self.screen)

        self.hair_brushing_imgs = (
            load_new_image('./assets/img/objects/hairing1.png', 300, 300, BLACK),
            load_new_image('./assets/img/objects/hairing2.png', 300, 300, BLACK),
            load_new_image('./assets/img/objects/hairing3.png', 300, 300, BLACK),
            load_new_image('./assets/img/objects/hairing2.png', 300, 300, BLACK)
        )
        self.hair_machine_imgs = (
            load_new_image('./assets/img/objects/hairmachine1.png', 300, 300, BLACK),
            load_new_image('./assets/img/objects/hairmachine2.png', 300, 300, BLACK),
            load_new_image('./assets/img/objects/hairmachine3.png', 300, 300, BLACK),
            load_new_image('./assets/img/objects/hairmachine4.png', 300, 300, BLACK),
            load_new_image('./assets/img/objects/hairmachine5.png', 300, 300, BLACK)
        )
        self.slapping_imgs = (
            load_new_image('./assets/img/objects/slap1.png', 300, 300, WHITE),
            load_new_image('./assets/img/objects/slap2.png', 300, 300, WHITE)

        )
        self.ice_img = load_new_image('./assets/img/New_image/Frozen_Goat.png', 300, 300, WHITE)
        self.shipping_img = load_new_image('./assets/img/New_image/Shipping.png', 300, 300, WHITE)
        self.car_img = self.terrain_spritesheet.get_sprite(157, 153, 300, 250)
        self.back_texture = self.terrain_spritesheet.get_sprite(35, 511, 100, 100)
        self.back_texture = pygame.transform.scale(self.back_texture, (1280, 720))

    def createTilemap(self, level):
        self.player = Player(self)
        self.playerAOE = PlayerAOE(self, self.player.x, self.player.y)
        # j is x position
        # i is the y position
        for i, row in enumerate(level):
            for j, column in enumerate(row):
                if column == ".": #normal ground
                    Ground(self, j, i)
                if column == "~": #grass ground
                    Ground(self, j, i, True, 'grass')
                if column == "_": #metal ground
                    Ground(self, j, i, False, 'metal')
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
                if column == "!": # special collectible item
                    Ground(self, j, i, True)
                    self.item_object = Item(self, j, i, True)
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
                
                #map objects
                if column == "H": #hair brushing chima san
                    Ground(self, j, i, True)
                    MapObject(self, j, i, self.hair_brushing_imgs, 0.1)
                if column == "C": #my car
                    Ground(self, j, i, True)
                    MapObjectStatic(self, j, i, self.car_img)
                if column == "M":# goat machine crying goat
                    Ground(self, j, i, True)
                    MapObject(self, j, i, self.hair_machine_imgs, 0.1)
                if column == "X":#slapping guy
                    Ground(self, j, i, True)
                    MapObject(self, j, i, self.slapping_imgs, 0.5)
                if column == "#":#ice
                    Ground(self, j, i, True, 'metal')
                    MapObjectStatic(self, j, i, self.ice_img)
                if column == "+":#shipping goat
                    Ground(self, j, i, True, 'metal')
                    MapObjectStatic(self, j, i, self.shipping_img)
                

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
        self.goats = pygame.sprite.LayeredUpdates()
        self.shadow = pygame.sprite.LayeredUpdates()
        self.textbox = pygame.sprite.LayeredUpdates()
        self.map_object = pygame.sprite.LayeredUpdates()

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
            # pygame.quit()
            # sys.exit()
            print('ending')
            self.state = 'ending'
        
        # else don't change level
        for sprite in self.all_sprites:
            sprite.kill()
        self.createTilemap(levels[self.level])
        Textbox(self, level_descrip[self.level], len(level_descrip[self.level]), self.clock)
            
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
                exit()
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

    def reset(self):
        # this method RESETS the game, do NOT call for restarting level
        self.level = 0
        self.cutscene_level = 0
        self.level_clear = False
        self.item_aquired = False


    def game_over(self):
        # print('death')

        gameover = True

        for sprite in self.all_sprites:
            sprite.kill()

        text = Text('you die', (WIN_WIDTH/2, WIN_HEIGHT/6), 50, WHITE, False)
        text.update('you die')

        restart_button = Button(WIN_WIDTH/2, 4*WIN_HEIGHT/6, 300, 150, WHITE, BLACK, 'restart level', 50)
        title_button = Button(200, 5*WIN_HEIGHT/6, 300, 150, WHITE, BLACK, 'title screen', 50)


        while gameover:
            self.events()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                gameover = False
                self.state = 'game'
                self.level_clear = False
                self.item_aquired = False
                self.levelUpdate()

            if title_button.is_pressed(mouse_pos, mouse_pressed):
                gameover = False
                self.state = 'title'
                self.reset()
            
            self.screen.blit(self.bg_img, (0,0))
            text.draw(self.screen)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.screen.blit(title_button.image, title_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()

    def intro_anime(self):
        intro_cutscene = Slideshow(intro_text, self.intro_images, self.bg_intro_images, self.screen)
        intro_done = intro_cutscene.stop

        while not intro_done:
            intro_done = intro_cutscene.stop
            self.events()

            if intro_done == True:
                intro_done = True
                self.state = 'game'
                self.level_clear = True
                self.levelUpdate()
            
            intro_cutscene.update()
            self.clock.tick(FPS)
            pygame.display.update()

    def end_anime(self):
        end_cutscene = Slideshow(ending_text, self.ending_images, self.bg_ending_images, self.screen)
        end_done = end_cutscene.stop

        while not end_done:
            end_done = end_cutscene.stop
            self.events()

            if end_done == True:
                end_done = True
                self.state = 'end_screen'
                # self.level_clear = True
                # self.levelUpdate()
            
            end_cutscene.update()
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):

        intro_done = False
        # intro = True

        title = Text('chinkara goat paradise', (WIN_WIDTH/2, WIN_HEIGHT/7), 100, WHITE, False)
        title.update('chinkara goat paradise')

        subtitle = Text('If red is your color, and what do you rejoice. When the war is over. Or….',
                        (WIN_WIDTH/2, 2*WIN_HEIGHT/7), 30, WHITE, False)
        subtitle.update('If red is your color, and what do you rejoice. When the war is over. Or….')
        
        footer = Text('this is a game for pyweek35 "In the shadows". by all the people in team chinkaraoshiman',
                        (WIN_WIDTH/2, 12*WIN_HEIGHT/13), 20, WHITE, True)
        footer.update('this is a game for pyweek35 "In the shadows". by all the people in team chinkaraoshiman')

        play_button = Button(WIN_WIDTH/2, 12*WIN_HEIGHT/20, 300, 70, WHITE, BLACK, 'Play', 60)
        about_button = Button(WIN_WIDTH/2, 15*WIN_HEIGHT/20, 300, 70, WHITE, BLACK, 'credits', 60)

        while not intro_done:
            self.events()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro_done = True
                self.state = 'intro'
            if about_button.is_pressed(mouse_pos, mouse_pressed):
                intro_done = True
                self.state = 'about'
            
            self.screen.blit(self.intro_background, (0,0))
            title.draw(self.screen)
            subtitle.draw(self.screen)
            footer.draw(self.screen)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(about_button.image, about_button.rect)
            self.clock.tick(FPS)

            pygame.display.update()

    def about_screen(self):

        intro_done = False
        # intro = True

        title = Text('about team chinkaraoshiman', (WIN_WIDTH/2, WIN_HEIGHT/7), 70, WHITE, False)
        title.update('about team chinkaraoshiman')
        subtitle = Text('like best quality chinkara always | strive for glory only | number one tetam',
                        (WIN_WIDTH/2, 2*WIN_HEIGHT/7), 30, WHITE, False)
        subtitle.update('like best quality chinkara always | strive for glory only | number one tetam')
        
        line1 = Text('meatyy: code', (WIN_WIDTH/2, 9*WIN_HEIGHT/20), 40, WHITE, False)
        line2 = Text('name642: art', (WIN_WIDTH/2, 11*WIN_HEIGHT/20), 40, WHITE, False)
        line3 = Text('speedlimit35: music, art, code', (WIN_WIDTH/2, 13*WIN_HEIGHT/20), 40, WHITE, False)
        line1.update('meatyy: code')
        line2.update('name642: art')
        line3.update('speedlimit35: music, art, code')

        line4 = Text('this game made for pyweek35 "In the shadows".', (WIN_WIDTH/2, 15*WIN_HEIGHT/20), 30, WHITE, False)
        line5 = Text('development time: March 25th to April 1st in year 2023', (WIN_WIDTH/2, 16*WIN_HEIGHT/20), 30, WHITE, False)
        line4.update('this game made for pyweek35 "In the shadows".')
        line5.update('development time: March 25th to April 1st in year 2023')
        back_button = Button(WIN_WIDTH/2, 18*WIN_HEIGHT/20, 300, 70, WHITE, BLACK, 'back', 60)
        while not intro_done:
            self.events()
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if back_button.is_pressed(mouse_pos, mouse_pressed):
                intro_done = True
                self.state = 'title'
            
            self.screen.blit(self.bg_img, (0,0))
            self.screen.blit(self.back_texture, (0, 0))
            title.draw(self.screen)
            subtitle.draw(self.screen)
            line1.draw(self.screen)
            line2.draw(self.screen)
            line3.draw(self.screen)
            line4.draw(self.screen)
            line5.draw(self.screen)
            self.screen.blit(back_button.image, back_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()

    def cutscene(self):
        # print('death')

        cutscene = True

        for sprite in self.all_sprites:
            sprite.kill()

        self.cutscene_level += 1
        i = 0
        sentences = []

        for text in cutscenes[self.cutscene_level]:
            sentences.append(Text(text, (WIN_WIDTH/2, WIN_HEIGHT/6 + i * 50), 50, WHITE, False))
            sentences[i].update(text)
            i+=1

        next_level_button = Button(WIN_WIDTH/2, 4*WIN_HEIGHT/6, 300, 150, WHITE, BLACK, 'next level', 50)
        
        while cutscene:
            self.events()

            if self.level == len(levels)-1:
                self.state = 'ending'
                return

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            # print(self.level, len(levels))
            if next_level_button.is_pressed(mouse_pos, mouse_pressed):
                self.level_clear = True
                self.item_aquired = False

                if self.level >= len(levels)-1:
                    self.state = 'ending'
                    cutscene = False

                else:
                    self.levelUpdate()
                    self.state = 'game'
                    cutscene = False
            
            self.screen.blit(self.bg_img, (0,0))
            for sen in sentences:
                sen.draw(self.screen)
            # print('cutscene active')
            self.screen.blit(next_level_button.image, next_level_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def final_ending_screen(self):
        title = Text('chinkaraoshiman presents this pyweek35 game "chinkara goat paradise"', (WIN_WIDTH/2, WIN_HEIGHT/30), 30, WHITE, True)
        title.update('chinkaraoshiman presents this pyweek35 game "chinkara goat paradise"')
        congrats_text = Text('you win and thank you for playing this game, we hope we win, we hope we get the part.', (WIN_WIDTH/2, WIN_HEIGHT-WIN_HEIGHT/30), 30, WHITE, True)
        congrats_text.update('you win and thank you for playing this game, we hope we win, we hope we get the part.')
        self.events()
        self.state = 'end_screen' #lock this state
        if self.can_switch_music:
            pygame.mixer.music.set_volume(0.5)
            self.bgm = pygame.mixer.music.load('./assets/music/newspaper.ogg')
            pygame.mixer.music.play(-1)
            self.can_switch_music = False
        # print(self.state)
        self.FinalEnd.draw()
        title.draw(self.screen)
        congrats_text.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def state_manager(self):
        # print(self.state)
        if self.state == 'game':
            self.main()
        elif self.state == 'title':
            self.intro_screen()
        elif self.state == 'about':
            self.about_screen()
        elif self.state == 'intro':
            self.intro_anime()
        elif self.state == 'lose':
            self.game_over()
        elif self.state == 'cutscene':
            self.cutscene()
        elif self.state == 'ending':
            self.end_anime()
        elif self.state == 'end_screen':
            # print('end now')
            self.final_ending_screen()

if __name__ == "__main__":    
    g = Game()
    # g.intro_screen()
    g.new()
    while g.running:
        pygame.display.set_caption("current FPS: "+str(g.clock.get_fps()))

        g.state_manager()
        # pygame.quit()

    pygame.quit()
    exit()