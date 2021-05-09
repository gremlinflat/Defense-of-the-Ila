import pygame
import os
from ship import *
from item import *
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum

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

class menu(Papan):
    def __init__(self,besar_layar):
        self.gambar=pygame.image.load("menu logo clear.png")
        self.credit_image=pygame.image.load("credit-pop up.jpg")
        Papan.__init__(self, besar_layar)

        self.start_btn = Write(
            center_position=(395, 325),
            font_size=45,
            text_rgb=(255, 255, 0),
            text="PLAY",
            action=GameState.NEWGAME,
        )

        self.credit_btn = Write(
            center_position=(395, 400),
            font_size=45,
            text_rgb=(255, 255, 0),
            text="CREDIT",
            action=GameState.credit,
        )

        self.quit_btn = Write(
            center_position=(400, 470),
            font_size=45,
            text_rgb=(255, 255, 0),
            text="EXIT",
            action=GameState.QUIT,
        )

        self.return_btn = Write(
            center_position=(140, 570),
            font_size=15,
            text_rgb=(255,255,255),
            text="Return to main menu",
            action=GameState.TITLE,
        )

    def title_screen(self):
        self.buttons = [self.start_btn,self.credit_btn, self.quit_btn]

        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
                self.layar.blit(self.gambar,(0,0))

            for button in self.buttons:
                self.ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
                if self.ui_action is not None:
                    return self.ui_action
                button.draw(self.layar)

            pygame.display.flip()
    
    def credit_screen(self):
        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            self.layar.blit(self.credit_image,(0,0))

            self.ui_action = self.return_btn.update(pygame.mouse.get_pos(), mouse_up)
            if self.ui_action is not None:
                return self.ui_action
            self.return_btn.draw(self.layar)

            pygame.display.flip()

class Write(Sprite):
    def __init__(self, center_position, text, font_size, text_rgb, action=None):
        self.mouse_over = False  # indicates if the mouse is over the element

        # create the default image
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb
        )

        # create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=(128,0,0)
        )

        # add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]
        self.action = action
        # calls the init method of the parent sprite class
        super().__init__()

        # properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ Updates the element's appearance depending on the mouse position
            and returns the button's action if clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    credit=2

def create_surface_with_text(text, font_size, text_rgb):
    """ Returns surface with text written on """
    font = pygame.font.Font("D:\Vermin Vibes 1989.ttf", int(font_size))
    surface= font.render(text,True,text_rgb)
    return surface.convert_alpha()


SPAWN_COOLDOWN = 1000

class Game:
    def __init__(self, papan):
        self.__dt = 0
        self.papan = papan
        self.ship = Ship((800, 600), 100, 4, 1)
        self.Asteroids = []
        self.last = pygame.time.get_ticks()
        

    def game_loop(self):
        clock = pygame.time.Clock()
        game_state=GameState.TITLE
        Menu=menu((self.papan.lebar,self.papan.tinggi))
        while True:
            if game_state == GameState.TITLE:     
                game_state = Menu.title_screen()

            if game_state == GameState.NEWGAME:
                return_btn = Write(
                center_position=(140, 570),
                font_size=15,
                text_rgb=(255,255,255),
                text="Return to main menu",
                action=GameState.TITLE,
                )

                mouse_up = False
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        mouse_up = True
                Menu.layar.blit(Menu.bgimage,(0,0))            
                self.update()
                self.draw()
                self.__dt = self.delta_time(clock.tick(30))

                Menu.ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
                if Menu.ui_action is not None:
                    game_state = Menu.title_screen()
                return_btn.draw(Menu.layar)

                pygame.display.flip()

            if game_state == GameState.credit:
                game_state = Menu.credit_screen()

            if game_state == GameState.QUIT:
                pygame.quit()
                return


    def draw(self):
        self.papan.draw()
        if self.ship != None:
            self.ship.draw(self.papan)

        for Asteorid in self.Asteroids:
            Asteorid.draw(self.papan)
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
