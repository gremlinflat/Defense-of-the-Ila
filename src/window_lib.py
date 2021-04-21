import pygame

class Window:
    def __init__(self, besar_layar): 
        pygame.init()
        self.lebar = besar_layar[0]
        self.tinggi = besar_layar[1]
        self.layar = pygame.display.set_mode(besar_layar)


class Game:
    def __init__(self, window):
        self.window = window
    

    def game_loop(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.update()
            self.draw()

    def quit(self):
        pygame.quit()

    def draw(self):
        pass

    def update(self):
        pass
    