import pygame
import os
from ship import *
#from bg import Background

#class layar
class Papan:
    def __init__(self, besar_layar): 
        # inisialisasi pygame
        pygame.init()
        self.lebar = besar_layar[0]
        self.tinggi = besar_layar[1]
        # membuat object layar dengan sebesar {besar_layar}
        self.layar = pygame.display.set_mode(besar_layar)
        
        self.bgimage = pygame.image.load(os.path.join(basepath, os.pardir, "assets", "bg2.jpg"))
        self.rectBGimg = self.bgimage.get_rect()
 
        self.bgY1 = 0
        self.bgX1 = 0
 
        self.bgY2 = -self.rectBGimg.height
        self.bgX2 = 0
 
        self.gerak = 2
         
    def update(self):
        self.bgY1 += self.gerak
        self.bgY2 += self.gerak
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height

    def draw(self):
        self.layar.blit(self.bgimage, (self.bgX2, self.bgY2))
        self.layar.blit(self.bgimage, (self.bgX1, self.bgY1))

class Game:
    def __init__(self, papan):
        self.__dt = 0
        self.papan = papan
        self.ship = Ship((50, 50), 100, "tes1.png", (50, 100), 4, 1)
        #self.bg = Background()

    def game_loop(self):
        clock = pygame.time.Clock()
        while True:
            self.update()
            self.draw()
            self.__dt = self.delta_time(clock.tick(30))
            

    def draw(self):
        self.papan.draw()
        
        self.ship.draw(self.papan)
        #self.bg.render()
        pygame.display.flip()

    def update(self):
        events = pygame.event.get()
        for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
        
        self.ship.update(self.__dt)
        self.papan.update()
        #self.bg.update()
        

    # mendapatkan jarak waktu antara dua frame dalam satuan detik
    def delta_time(self, time_between):
        return time_between / 1000.0