import pygame
import os

alamat_proyek = os.path.dirname(__file__)
class Animasi:
    
    def __init__(self, nama_gambar, kolom, baris, ukuran_skala):
        # ambil alamat directory (absolute)

        # ambil spritelembaran dari folder aset
        self.lembaran = pygame.image.load(os.path.join(alamat_proyek, os.pardir, "aset", nama_gambar)).convert_alpha()
        
        # index bingkai yang sedang di gambar
        self.__bingkai_sekarang = 0

        self.__bingkai_target = self.__bingkai_sekarang

        # list bingkai yang dapat dari spritelembaran
        self.bingkai_bingkai = []
        ukuran_lembar_sprite = self.lembaran.get_size()
        # parsing bingkai_bingkai dari spritelembaran
        self.ukuran_bingkai = (ukuran_lembar_sprite[0] // kolom , ukuran_lembar_sprite[1] // baris)
        for j in range(baris):
            for i in range(kolom):
                posisi = (self.ukuran_bingkai[0] * i, self.ukuran_bingkai[1] * j)
                bingkai = self.lembaran.subsurface(pygame.Rect(posisi, self.ukuran_bingkai))
                bingkai = pygame.transform.scale(bingkai, ukuran_skala)
                self.bingkai_bingkai.append(bingkai)
    

    def skala(self, ukuran):
        bingkai_bingkai_baru = []
        for bingkai in self.bingkai_bingkai:
            bingkai_baru = pygame.transform.scale(bingkai, ukuran)
            bingkai_bingkai_baru.append(bingkai_baru)
        self.bingkai_bingkai = bingkai_bingkai_baru
    # ganti bingkai yang di gambar menjadi bingkai selanjutnya
    def lanjutan(self):
        self.__bingkai_sekarang = ((self.__bingkai_sekarang + 1) % (len(self.bingkai_bingkai) - 1))
    
    # set current gambar bingkai
    def set_bingkai_sekarang(self, indeks):
        if indeks < len(self.bingkai_bingkai):
            self.__bingkai_sekarang = indeks

    def set_bingkai_target(self, indeks):
        if indeks < len(self.bingkai_bingkai):
            self.__bingkai_target = indeks
    # gambar bingkai di pojok kiri atas
    def gambar(self, jendela):
        jendela.layar.blit(self.bingkai_bingkai[self.__bingkai_sekarang], (0,0))

    # gambar bingkai di posisi
    def gambar(self, jendela, posisi):
        if self.__bingkai_sekarang > self.__bingkai_target:
            self.__bingkai_sekarang -= 1
        elif self.__bingkai_sekarang < self.__bingkai_target:
            self.__bingkai_sekarang += 1
            
        jendela.layar.blit(self.bingkai_bingkai[self.__bingkai_sekarang], posisi)    
    
    