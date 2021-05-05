import pygame 

class Entitas(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animasi_animasi = []
        self.animasi_terpilih = 0
        self.posisi = [0,0]
        
    def gambar(self):
        pass

    def perbarui(self):
        pass
    
    def _tambah_animasi(self, Animasi):
        self.animasi_animasi.append(Animasi)

    def _tetapkan_animasi(self, indeks):
        self.animasi_terpilih = indeks