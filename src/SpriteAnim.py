import pygame
import os

BASE_PATH = os.path.dirname(__file__)
BASE_ASSET_PATH = os.path.join(BASE_PATH, os.pardir, "assets")

DRAW_COOLDOWN = 100
class Animation:
    def __init__(self, img_name, frame_count, loop):
        # ambil alamat directory (absolute)

        # ambil spritesheet dari folder assets
        self.sheet = pygame.image.load(os.path.join(BASE_ASSET_PATH, img_name)).convert_alpha()
        
        # index frame yang sedang di draw
        self.__current_frame = 0

        self.loop = loop

        self.cooldown = DRAW_COOLDOWN
        self.frame_count = frame_count
        self.last = pygame.time.get_ticks()
        # list frame yang dapat dari spritesheet
        self.frames = []
        spritesheet_size = self.sheet.get_size()
        # parsing frames dari spritesheet
        self.frame_size = (spritesheet_size[0] // frame_count , spritesheet_size[1])
        for i in range(frame_count):
            pos = (self.frame_size[0] * i, 0)
            frame = self.sheet.subsurface(pygame.Rect(pos, self.frame_size))
            self.frames.append(frame)
    
    def get_current_frame(self):
        return self.__current_frame

    def scale(self, size):
        new_frames = []
        self.frame_size = size
        for frame in self.frames:
            
            new_frame = pygame.transform.scale(frame, size)
            new_frames.append(new_frame)
        self.frames = new_frames
    # ganti frame yang di draw menjadi frame selanjutnya
    def next(self):
        self.__current_frame = ((self.__current_frame + 1) % (len(self.frames) - 1))
    
    # set current drawn frame
    def set_current_frame(self, idx):
        if idx < len(self.frames):
            self.__current_frame = idx

    # draw frame di pojok kiri atas
    def draw(self, window):
        window.display.blit(self.frames[self.__current_frame], (0,0))

    # draw frame di pos
    def draw(self, window, pos):
        now = pygame.time.get_ticks()
        if self.loop:
            if now - self.last >= self.cooldown:
                self.__current_frame = (self.__current_frame + 1) % len(self.frames)
                self.last = now
        else:
            if now - self.last >= self.cooldown and self.__current_frame < len(self.frames) - 1:
                self.__current_frame = (self.__current_frame + 1)
                self.last = now

        window.display.blit(self.frames[self.__current_frame], pos) 
    
    