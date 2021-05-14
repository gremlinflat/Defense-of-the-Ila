import pygame
import os
from ship import *
from item import *
#from bg import Background

PARALLAX_BG_PATH_FROM_ASSET = "bg2.jpg"
#class layar
class Papan:
    def __init__(self, besar_layar): 
        # inisialisasi pygame
        pygame.init()
        self.lebar = besar_layar[0]
        self.tinggi = besar_layar[1]
        # membuat object layar dengan sebesar {besar_layar}
        self.layar = pygame.display.set_mode(besar_layar)
        self.bgimage = pygame.image.load(os.path.join(BASE_ASSET_PATH, PARALLAX_BG_PATH_FROM_ASSET))
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


SPAWN_COOLDOWN = 1000

class Game:
    def __init__(self, papan):
        self.__dt = 0
        self.papan = papan
        self.ship = Ship((800, 600), 100, 4, 1)
        self.Asteroids = []
        self.last = pygame.time.get_ticks()
        #self.bg = Background()

    def game_loop(self):
        clock = pygame.time.Clock()
        while True:
            self.update()
            self.draw()
            self.__dt = self.delta_time(clock.tick(30))
            

    def draw(self):
        self.papan.draw()
        if self.ship != None:
            self.ship.draw(self.papan)

        for Asteorid in self.Asteroids:
            Asteorid.draw(self.papan)
        self.bul.draw(self.papan)
        #self.bg.render()
        pygame.display.flip()

    def update(self):
        events = pygame.event.get()
        for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
        
        for As in self.Asteroids:
            if pygame.sprite.collide_rect(As, self.ship):
                self.Asteroids.remove(As)

            As.update(self.__dt)
        
        if self.ship != None: 
            self.ship.update(self.papan ,self.__dt)
        
        self.papan.update()
        self.bul.update(self.__dt)
        now = pygame.time.get_ticks()
        if (now - self.last) >= SPAWN_COOLDOWN:
            self.spawn_asteroid()
            self.last = now

        

    # mendapatkan jarak waktu antara dua frame dalam satuan detik
    def delta_time(self, time_between):
        return time_between / 1000.0
    
    def spawn_asteroid(self):
        rand_scale = random.randint(50, 100)
        y = -rand_scale
        x = random.randint(0, self.papan.lebar - rand_scale)
        new_asteroid = Asteroid([x, y], (rand_scale, rand_scale))
        self.Asteroids.append(new_asteroid)

