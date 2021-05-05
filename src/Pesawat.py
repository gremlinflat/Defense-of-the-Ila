import pygame
from Entitas import Entitas
from animasi_sprite import *



tombol = {
    pygame.K_w : (0, -1),
    pygame.K_s : (0,  1),
    pygame.K_d : (1,  0),
    pygame.K_a : (-1, 0),
}

class Pesawat(Entitas):
    def __init__(self, posisi, kecepatan, nama_gambar, ukuran, kolom, baris):
        super().__init__()
        self._tambah_animasi(Animasi(nama_gambar, kolom, baris, ukuran))
        self.kotak = pygame.Rect(posisi, ukuran)

        self.posisi = list(self.kotak.center)
        self.kecepatan = float(kecepatan)

        # (vektor[0], vektor[1]) == (x, y)
        self.vektor = (0.0, 0.0) 

    def gambar(self, jendela):
        self.animasi_animasi[self.animasi_terpilih].gambar(jendela, self.posisi)

    def perbarui(self, dt):
        kunci_kunci = pygame.key.get_pressed()
        self.gerak(kunci_kunci, dt)
        
    # methon pergerakan pesawat
    def gerak(self, kunci_kunci, dt):
        tidak_ditekan = True
        for kunci in tombol: # untuk setiap kunci di kunci_DECT
            if kunci_kunci[kunci]: # kondisi jika w, a, s, d di tekan
                tidak_ditekan = False
                self.vektor = tombol[kunci]
                self.posisi[0] += self.vektor[0] * self.kecepatan * dt
                self.posisi[1] += self.vektor[1] * self.kecepatan * dt
        if tidak_ditekan: # kondisi jika w, a, s, d tidak di tekan
            self.vektor = (0, 0)
        
        self.kotak.center = tuple(self.posisi)

        