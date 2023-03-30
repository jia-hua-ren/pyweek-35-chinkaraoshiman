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



class CutsceneAnime(object):
    """docstring for CutsceneAnime"""
    def __init__(self, texts, images, screen):
        self.texts = texts
        self.screen = screen
        self.images = images
        self.index = 0
        self.image = self.images[self.index]
        self.rect=self.image.get_rect()
        self.alph = 10
        self.image.set_alpha(self.alph)
        self.mode = 1
        self.stop = False

        self.isboss = True

        if self.isboss==True:
            self.max_alph = 500
            self.min_alph = -100
        else:
            self.max_alph = 400
            self.min_alph = 0

    def update(self):
        self.screen.fill(BLACK)
        if self.alph >=self.max_alph:
            self.mode =-1
        elif self.alph <=-0:
            self.index+=1
            if self.index>len(self.images)-1:
                if self.isboss==True:
                    self.index=self.index>len(self.images)-1
                    self.stop=True
                else:
                    self.index=0
            self.image = self.images[self.index]
            self.mode=1

        self.alph +=10*self.mode
        self.image.set_alpha(self.alph)



        self.screen.blit(self.image,self.rect)
        # if self.isboss==False:
        #     self.text_group.update(True)
        #     self.text_group.draw(self.screen)
    # def StopNow(self):
    #     if self.stop == True:
    #         return True
    # def MyIndex(self):
    #     return self.index    