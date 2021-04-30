import pygame
from SpriteAnim import *
from assets import *



KEY_DICT = {
    pygame.K_w : (0, -1),
    pygame.K_s : (0,  1),
    pygame.K_d : (1,  0),
    pygame.K_a : (-1, 0),
}

class Ship(pygame.sprite.Sprite):
    def __init__(self, pos, speed, img_name, size, kolom, baris):
        super().__init__()
        self.animation = Animation(img_name, kolom, baris, size)
        #self.animation.scale(size)
        self.rect = pygame.Rect(pos, self.animation.frame_size)

        self.pos = list(self.rect.center)
        self.speed = float(speed)

        # (vec[0], vec[1]) == (x, y)
        self.vec = (0.0, 0.0) 
player = pygame.image.load("assets/pesawat 1.1.png")
    def draw(self, window):
        # kondisi untuk menentukan frame mana yang akan di draw
        #if self.vec[0] > 0:
        #    self.animation.set_target_frame(4)
        #elif self.vec[0] < 0:
        #    self.animation.set_target_frame(0)
        #else:
        #    self.animation.set_target_frame(2)
        self.animation.draw(window, self.rect.topleft)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.move(keys, dt)
        
    # methon pergerakan pesawat
    def move(self, keys, dt):
        notPressed = True
        for key in KEY_DICT: # untuk setiap key di KEY_DECT
            if keys[key]: # kondisi jika w, a, s, d di tekan
                notPressed = False
                self.vec = KEY_DICT[key]
                self.pos[0] += self.vec[0] * self.speed * dt
                self.pos[1] += self.vec[1] * self.speed * dt
        if notPressed: # kondisi jika w, a, s, d tidak di tekan
            self.vec = (0, 0)
        
        self.rect.center = tuple(self.pos)

        