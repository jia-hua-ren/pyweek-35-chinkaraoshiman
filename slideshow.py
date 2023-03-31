import pygame
from config import *
from utility import *

class Slideshow(object):
    """ for some reason loading in an 
    identical copy of images called bg_images 
    gets rid of flashing image glitch 
    when index increases
    """
    def __init__(self, texts, images, bg_images, screen):
        self.texts = texts
        self.screen = screen
        #event controls
        self.stop = False
        self.kill_on_release = False
        #images
        self.blank_image = pygame.Surface((800, 600))
        self.blank_image.fill(BLACK)
        self.bg_image = pygame.Surface((800, 600))
        self.bg_image.fill(WHITE)
        self.images = images
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() #assume all images have same dimensions so same rect
        self.rect.center = WIN_CENTER

        #bg image to fix flashing glitch
        self.bg_images = bg_images
        self.bg_image = self.bg_images[self.index]

        if self.index == len(self.images)-1:
            # print('black one')
            self.bottom_image = self.images[self.index]
        else:
            self.bottom_image = self.images[self.index+1]
            # print('normal one')
        # self.most_bottom_image = self.images[self.index+1] #prevent glitchy flashing effect DIDNT WORK
        #crossfade
        self.wait_seconds = 3
        self.wait_clock_cycles = FPS * self.wait_seconds
        self.clock_cycles = 0
        self.fade_speed = 3
        self.fade_done = False
        self.max_alph = 300
        self.alph = self.max_alph
        self.image.set_alpha(self.alph)
        # self.most_bottom_image.set_alpha(self.max_alph)
        #for glitch
        self.flip = False
        #text
        self.currentText = Text(texts[self.index], (self.rect.center[0], self.rect.center[1]+300), 32, WHITE, True)

    def events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.kill_on_release = True
        elif self.kill_on_release == True and not keys[pygame.K_SPACE]:
            self.stop = True

    def crossfade(self):
        # print(self.clock_cycles)
        #wait some time at first image
        if self.clock_cycles < self.wait_clock_cycles and not self.fade_done:
            # print('waiting')
            self.alph = self.max_alph
            self.clock_cycles += 1
        else:
            # print('text')
            #first image becomes transparent after
            if self.alph >= 0: # if not transparent
                self.alph -= self.fade_speed
            #then its completely transpartent
            else: #if transparent
                self.fade_done = True #done fading
                self.clock_cycles = 0#reset clock cycle timer to wait again

        #so only second image show
        #then, update first image to second image
        #update original second image to next image
        if self.fade_done and self.index < len(self.images)-1: 
            self.image.set_alpha(self.alph) 
            self.flip = True
            self.index += 1
            # print(self.index)
            self.image = self.images[self.index]
            self.bg_image = self.bg_images[self.index]
            #if at last image, the second image in this case will be a blank
            if self.index == len(self.images)-1: self.bottom_image = self.blank_image
            else: self.bottom_image = self.images[self.index+1]
            self.currentText.update(self.texts[self.index])#CHANGE THE TEXT
            self.fade_done = False
        
        #after the last image, the slideshow ends
        if self.index == len(self.images)-1 and self.fade_done: self.stop = True

        self.image.set_alpha(self.alph)  

    def update(self):
        self.events()
        self.crossfade()
        self.draw()

        # self.screen.blit(self.blank_image,self.rect)
    def draw(self):
        self.screen.fill(BLACK)
        if self.flip:
            # print('me too')
            self.screen.blit(self.image,self.rect)
            self.screen.blit(self.bg_image,self.rect) #GLITCH!!!!!!!!!!!!! 
            self.flip = False
            
        else:
            self.screen.blit(self.bottom_image,self.rect)
            self.screen.blit(self.image,self.rect)
        self.currentText.draw(self.screen)
        
        


        
        
  