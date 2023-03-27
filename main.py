import pygame
from sprites import *
from config import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        #self.font = pygame.font.Font('arial.ttf', 32)
        self.running = True

        self.character_spritesheet = Spritesheet('./assets/img/player.png')
        self.goat_spritesheet = Spritesheet('./assets/img/goat.png')
        self.terrain_spritesheet = Spritesheet('./assets/img/ground.png')
        self.enemy_spritesheet = Spritesheet('./assets/img/enemy.png')
        self.wall_spritesheet = Spritesheet('./assets/img/wall.png')
        self.shadow_spritesheet = Spritesheet('./assets/img/shadow.png')
        # self.attack_spritesheet = Spritesheet('img/attack.png')

        # self.intro_background = pygame.image.load('./img/introbackground.png')
        # self.go_background = pygame.image.load('./img/gameover.png')

    def createTilemap(self):
        # j is x position
        # i is the y position
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i) # ground
                if column == "B": #block wall
                    Block(self, j, i)
                if column == "S": #shadow 
                    Shadow(self, j, i)
                if column == "E": #enemy
                    Enemy(self, j, i)
                if column == "G": # goat
                    Goat(self, j, i)
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
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.playerAOE = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.goats = pygame.sprite.LayeredUpdates()
        self.shadow = pygame.sprite.LayeredUpdates()
        self.createTilemap()

    def events(self): # key presses and stuff
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
    def update(self): # make things move
        #game loop updates
        self.all_sprites.update() #find update function/method in every sprite and update it

    def draw(self): # draw sprites on screen
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen) # sprite group draw method
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
            pygame.display.set_caption("current FPS: "+str(self.clock.get_fps()))
        pygame.quit()
        sys.exit()
        
        # self.running = False

    def game_over(self):
        print('death')
        # text = self.font.render('you die', False, WHITE)
        # text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        # restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'restart', 32)

        # for sprite in self.all_sprites:
        #     sprite.kill()

        # while self.running:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             self.running = False 

        #     mouse_pos = pygame.mouse.get_pos()
        #     mouse_pressed = pygame.mouse.get_pressed()    

        #     if restart_button.is_pressed(mouse_pos, mouse_pressed):
        #         self.new()
        #         self.main()

        #     self.screen.blit(self.go_background, (0,0))     
        #     self.screen.blit(text, text_rect)
        #     self.screen.blit(restart_button.image, restart_button.rect)
        #     self.clock.tick(FPS)
        #     pygame.display.update() 

    def intro_screen(self):
        print('intro')
        # intro = True

        # title = self.font.render('rpg tutorial', False, BLACK)
        # title_rect = title.get_rect(x=10, y=10)
        
        # play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)

        # while intro:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             intro = False
        #             self.running = False

        #     mouse_pos = pygame.mouse.get_pos()
        #     mouse_pressed = pygame.mouse.get_pressed()

        #     if play_button.is_pressed(mouse_pos, mouse_pressed):
        #         intro = False
            
        #     self.screen.blit(self.intro_background, (0,0))
        #     self.screen.blit(title, title_rect)
        #     self.screen.blit(play_button.image, play_button.rect)
        #     self.clock.tick(FPS)
        #     pygame.display.update()


g = Game()
# g.intro_screen()
g.new()
while g.running:
    g.main()
    pygame.quit()
    # g.game_over()


sys.exit()