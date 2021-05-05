import pygame
import os
from Pesawat import *


#class layar
class Papan:
    def __init__(self, besar_layar): 
        # inisialisasi pygame
        pygame.init()
        self.lebar = besar_layar[0]
        self.tinggi = besar_layar[1]
        # membuat object layar dengan sebesar {besar_layar}
        self.layar = pygame.display.set_mode(besar_layar)
        
        self.latar = pygame.image.load(os.path.join(alamat_proyek, os.pardir, "aset", "bg2.jpg"))
        self.latar_kotak = self.latar.get_rect()
 
        self.latar_y1= 0
        self.latar_x1 = 0
 
        self.latar_y2 = -self.latar_kotak.height
        self.latar_x2 = 0
 
        self.gerak = 2
         
    def perbarui(self):
        self.latar_y1+= self.gerak
        self.latar_y2 += self.gerak
        if self.latar_y1>= self.latar_kotak.height:
            self.latar_y1= -self.latar_kotak.height
        if self.latar_y2 >= self.latar_kotak.height:
            self.latar_y2 = -self.latar_kotak.height

    def gambar(self):
        self.layar.blit(self.latar, (self.latar_x2, self.latar_y2))
        self.layar.blit(self.latar, (self.latar_x1, self.latar_y1))

class Permainan:
    def __init__(self, papan):
        self.__dt = 0
        self.papan = papan
        self.pesawat = Pesawat((50, 100), 100, "pesawat_level1.png", (64, 64), 4, 5)
 

    def perulangan_permainan(self):
        clock = pygame.time.Clock()
        while True:
            self.perbarui()
            self.gambar()
            self.__dt = self.selisih_waktu(clock.tick(30))
            

    def gambar(self):
        self.papan.gambar()
        
        self.pesawat.gambar(self.papan)

        pygame.display.flip()

    def perbarui(self):
        peristiwa = pygame.event.get()
        for kejadian in peristiwa:
                if kejadian.type == pygame.QUIT:
                    pygame.quit()
        
        self.pesawat.perbarui(self.__dt)
        self.papan.perbarui()
        

    # mendapatkan jarak waktu antara dua frame dalam satuan detik
    def selisih_waktu(self, selang_waktu):
        return selang_waktu / 1000.0