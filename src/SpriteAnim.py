import pygame
import os

class Animation:
    
    def __init__(self, img_name, img_size, kolom, baris):
        # ambil alamat directory (absolute)
        basepath = os.path.dirname(__file__)

        # ambil spritesheet dari folder assets
        self.sheet = pygame.image.load(os.path.join(basepath, os.pardir, "assets", img_name)).convert_alpha()

        # index frame yang sedang di draw
        self.__current_frame = 0

        # list frame yang dapat dari spritesheet
        self.frames = []
        
        # parsing frames dari spritesheet
        self.img_size = (img_size[0] // kolom , img_size[1] // baris)
        for j in range(baris):
            for i in range(kolom):
                pos = (self.img_size[0] * i, self.img_size[1] * j)
                self.frames.append(self.sheet.subsurface(pygame.Rect(pos, self.img_size)))
    
    # ganti frame yang di draw menjadi frame selanjutnya
    def next(self):
        self.__current_frame = ((self.__current_frame + 1) % (len(self.frames) - 1))
    

    def set_current_frame(self, idx):
        self.__current_frame = idx

    # draw frame sekarang
    def draw(self, window):
        window.layar.blit(self.frames[self.__current_frame], (0,0))
    
    