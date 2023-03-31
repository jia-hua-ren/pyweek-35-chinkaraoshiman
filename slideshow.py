import pygame
from config import *

# class CutsceneAnime():
# 	"""cutscene animation with text and image
#     example input:
#     ending_text = [["","",4],["cop","*gasp heh u are a quick one... kid *huff huff",5],["kid","mmm this is one tasty donut",4],["kid","*aggressively munches on donut",3],["cop",".............",2],["kid","*wolfs down donut and scratches chin",4],["","MISSION ACCOMPLISHED",3]]
#     ending_images = [[scene4,scene4],[scene5,scene5],[scene6,scene6],[scene7,scene8],[scene7,scene8],[scene9,scene9],[scene10,scene10]]    
#     """	
# 	def __init__(self,text,images, screen):
# 		self.screen = screen
# 		self.count_text = 0
# 		self.index = 0
# 		# self.count_image = 0

# 		# self.font_S = pygame.font.Font(None, 60)#person speaking
# 		self.font = pygame.font.Font(None, 80) 
# 		self.color = (255,255,255)

# 		self.text = text #text array
# 		self.current_text = self.text[self.count_text][1]
# 		# self.current_text_S = self.text[self.count_text][0]
# 		self.txt_surface = self.font.render(self.current_text, True, self.color)
# 		# self.txt_surface_S = self.font.render(self.current_text_S, True, self.color)
# 		self.txt_rect = self.txt_surface.get_rect()
# 		# self.txt_rect_S = self.txt_surface_S.get_rect()
# 		self.txt_x = self.txt_rect[2]#
# 		# self.txt_x_S = self.txt_rect_S[2]#
		

# 		self.backTexture = pygame.image.load("./assets/img/backTexture.png").convert_alpha()

# 		self.finished = False

# 		self.next_scene = False

# 		self.images = images
# 		self.image = self.images[self.count_text]
# 		self.current_image = self.image[self.index]
# 		self.image_rect = self.current_image.get_rect()
# 		self.image_rect.center = (WIN_WIDTH/2, WIN_HEIGHT/2)

# 		self.timer_text = 0
# 		# self.timer_images = 0
# 		self.clock = pygame.time.Clock()

# 		self.time_text = self.text[self.count_text][2] *15
# 		# self.time_images =self.images[self.count_image][1]*30

		

# 	def render_text(self):
# 		self.image = self.images[self.count_text]
# 		self.current_image = self.image[self.index]		


# 		self.time_text = self.text[self.count_text][2] *15
# 		self.current_text = self.text[self.count_text][1]
# 		# self.current_text_S = self.text[self.count_text][0]

# 		self.image = self.images[self.count_text]
# 		self.image_rect = self.current_image.get_rect()
# 		self.image_rect.center = (WIN_WIDTH/2, WIN_HEIGHT/2)
		
# 		self.txt_rect = self.txt_surface.get_rect()
# 		# self.txt_rect_S = self.txt_surface_S.get_rect()
# 		self.txt_surface = self.font.render(self.current_text, True, self.color)
# 		# self.txt_surface_S = self.font_S.render(self.current_text_S, True, self.color)

# 		self.screen.blit(self.current_image, self.image_rect.center)
# 		self.screen.blit(pygame.transform.scale(self.backTexture, (1280, 150)), (0, 570))
# 		# print(self.count_text,self.current_text,self.image)
# 		# screen.blit(self.txt_surface_S, (100, 580))#(1280/2)-self.txt_rect[2]/2
# 		self.screen.blit(self.txt_surface, (50, 640))

# 		# print(self.time_text)


# 		self.timer_text+=1

# 		if self.timer_text >= self.time_text:
# 			self.next_scene = True
# 			self.timer_text = 0
# 		else:
# 			self.next_scene = False

# 		self.clock.tick(15)


# 		pygame.display.flip()

# 	def update(self): #animation
# 		print(self.count_text, self.index)
# 		keys = pygame.key.get_pressed()
# 		if keys[pygame.K_SPACE]:
# 			self.finished = True
# 		# print(self.current_image)
# 		self.index += 1
# 		if self.index >= len(self.image):
# 			self.index = 0
# 		self.current_image = self.image[self.index]
# 		self.detect_next()
# 		self.render_text()

# 	def detect_next(self):

# 		if self.next_scene == True:
# 			if (self.count_text) >= len(self.text):
# 				self.count_text = self.count_text
# 				self.finished = True
# 			# print(self.finished)
# 			if self.finished == False:
# 				self.count_text +=1
# 				self.current_text = self.text[self.count_text]
# 			elif self.finished==True:
# 				self.count_text = self.count_text
# 				self.finished = True



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
        self.rect.center = (WIN_WIDTH/2, WIN_HEIGHT/2)

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

        self.flip = False

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
            print(self.index)
            self.image = self.images[self.index]
            self.bg_image = self.bg_images[self.index]
            #if at last image, the second image in this case will be a blank
            if self.index == len(self.images)-1: self.bottom_image = self.blank_image
            else: self.bottom_image = self.images[self.index+1]
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
        if self.flip:
            print('me too')
            self.screen.blit(self.image,self.rect)
            self.screen.blit(self.bg_image,self.rect) #GLITCH!!!!!!!!!!!!! 
            self.flip = False
            
        else:
            self.screen.blit(self.bottom_image,self.rect)
            self.screen.blit(self.image,self.rect)


        
        
  