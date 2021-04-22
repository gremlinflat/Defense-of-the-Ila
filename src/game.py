import pygame
from  SpriteAnim import *
import os

#class layar
class Window:
    def __init__(self, besar_layar): 
        # inisialisasi pygame
        pygame.init()
        self.lebar = besar_layar[0]
        self.tinggi = besar_layar[1]
        # membuat object layar dengan sebesar {besar_layar}
        self.layar = pygame.display.set_mode(besar_layar)


class Game:
    def __init__(self, window):
        self.window = window
        self.ship = Animation("ship.png", (80, 48), 5, 2)
    

    def game_loop(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.ship.set_current_frame(4)
                    if event.key == pygame.K_a:
                        self.ship.set_current_frame(0)

            self.update()
            self.draw()
            clock.tick(60)

    def quit(self):
        pygame.quit()

    def draw(self):
        self.ship.draw(self.window)
        pygame.display.flip()

    def update(self):
        pass