from config import *

class Fadein():
    def __init__(self, image, pos, speed, screen):
        self.image = image
        self.pos = pos
        self.screen = screen
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.image.set_alpha(0)
        self.alph = 0
    
    def update(self):
        if self.alph <= 250:
            self.alph += self.speed
            self.image.set_alpha(self.alph)

    def draw(self):
        # print(self.alph)
        self.update()
        self.screen.fill(BLACK)
        self.screen.blit(self.image, self.rect)