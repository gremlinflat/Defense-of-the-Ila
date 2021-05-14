import pygame
from Entity import Entity
from SpriteAnim import *

WIN_SIZE = (800, 600)

KEY_DICT = {
    pygame.K_w: (0, -1),
    pygame.K_s: (0,  1),
    pygame.K_d: (1,  0),
    pygame.K_a: (-1, 0),
}




SHIP_ANIMATIONS_PATH = {
    "idle" : "ship/ship_normal_level1.png",
    "left" : "ship/ship_left_level1.png",
    "right": "ship/ship_right_level1.png",
    "sleft" : "ship/ship_sleft_level1.png",
    "sright": "ship/ship_sright_level1.png",
    
}

class Ship(Entity):
    def __init__(self, pos, speed, kolom, baris):
        super().__init__()
        self._addAnimation([
            Animation(SHIP_ANIMATIONS_PATH["left"], 4, 1, True),
            Animation(SHIP_ANIMATIONS_PATH["sleft"], 4, 1, True),
            Animation(SHIP_ANIMATIONS_PATH["idle"], 4, 1, True),
            Animation(SHIP_ANIMATIONS_PATH["sright"], 4, 1, True),
            Animation(SHIP_ANIMATIONS_PATH["right"], 4, 1, True)
        ])
        self.rect = pygame.Rect(pos, self.animations[0].frame_size)

        self.pos = list(self.rect.center)
        self.speed = float(speed)
        
        # (vec[0], vec[1]) == (x, y)
        self.vec = (0.0, 0.0)
        self.bullet_list = [] 


    def update(self, screen, dt):
        keys = pygame.key.get_pressed()
        self.move(keys, dt)

        self.pos[0] = min(max(self.pos[0], 0), screen.lebar - (self.rect.width))
        self.pos[1] = min(max(self.pos[1], 0), screen.tinggi - (self.rect.height))
        

        ##IMPLEMENT SHOOTING

    # methon pergerakan pesawat
    def move(self, keys, dt):
        notPressed = True
        for key in KEY_DICT:  # untuk setiap key di KEY_DECT
            if keys[key]:  # kondisi jika w, a, s, d di tekan
                notPressed = False
                self.vec = KEY_DICT[key]
                self.pos[1] += self.vec[1] * self.speed * dt
                self.pos[1] %= WIN_SIZE[1]
                self.pos[0] += self.vec[0] * self.speed * dt
                self.pos[0] %= WIN_SIZE[0]
        if notPressed:  # kondisi jika w, a, s, d tidak di tekan
            self.vec = (0, 0)

        
        
            
        
        if self.vec[0] > 0:
            self._setnextAnim(4)
        elif self.vec[0] < 0:
            self._setnextAnim(0)
        else:
            self._setnextAnim(2)
        
        self.rect.topleft = tuple(self.pos)
