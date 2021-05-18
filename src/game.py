import pygame
import os
from ship import Ship
from item import Bonus, Asteroid, Bullet, BULLET_SCALE, Heart, Explosions_vfx
from random import randint
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from SpriteAnim import BASE_ASSET_PATH, BASE_PATH


PARALLAX_BG_PATH_FROM_ASSET = "bg2.jpg"
MENU_IMAGE_PATH = "menu logo clear.png"
CREDIT_IMAGE_PATH = "credit-pop up.jpg"
GAMEOVER_IMAGE_PATH = "game over1.png"
HEALTH_IMAGE_PATH = "health-bar 1.png"
MENU_FONT_PATH = "Vermin Vibes 1989.ttf"
SCORE_FONT_PATH = "Minecraft.ttf"
SHOT_SOUND =  "laser2.mp3"
DEAD_SOUND = "death.mp3"
FPS = 60
#class layar

class Papan:
    def __init__(self, besar_layar):
        # inisialisasi pygame
        pygame.init()
        pygame.mixer.init()
        
        self.lebar = besar_layar[0]
        self.tinggi = besar_layar[1]
        # membuat object layar dengan sebesar {besar_layar}
        self.layar = pygame.display.set_mode(besar_layar)

        self.bgimage = pygame.image.load(os.path.join(
            BASE_ASSET_PATH, PARALLAX_BG_PATH_FROM_ASSET))


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


class menu():
    def __init__(self, besar_layar, papan):
        self.gambar = pygame.image.load(
            os.path.join(BASE_ASSET_PATH, MENU_IMAGE_PATH))
        self.credit_image = pygame.image.load(
            os.path.join(BASE_ASSET_PATH, CREDIT_IMAGE_PATH))
        self.gameover_image = pygame.image.load(
            os.path.join(BASE_ASSET_PATH, GAMEOVER_IMAGE_PATH))
        self.papan = papan

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
            text_rgb=(255, 255, 255),
            text="Return to main menu",
            action=GameState.TITLE,
        )

    def title_screen(self):
        self.buttons = [self.start_btn, self.credit_btn, self.quit_btn]
        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            self.papan.layar.blit(self.gambar, (0, 0))

            for button in self.buttons:
                self.ui_action = button.update(
                    pygame.mouse.get_pos(), mouse_up)
                if self.ui_action is not None:
                    return self.ui_action
                button.draw(self.papan.layar)

            pygame.display.flip()

    def credit_screen(self):
        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            self.papan.layar.blit(self.credit_image, (0, 0))

            self.ui_action = self.return_btn.update(
                pygame.mouse.get_pos(), mouse_up)
            if self.ui_action is not None:
                return self.ui_action

            self.return_btn.draw(self.papan.layar)

            pygame.display.flip()

    def gameover_screen(self):
        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            self.papan.layar.blit(self.gameover_image, (0, 0))

            self.ui_action = self.return_btn.update(
                pygame.mouse.get_pos(), mouse_up)
            if self.ui_action is not None:
                return self.ui_action

            self.return_btn.draw(self.papan.layar)

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
            text=text, font_size=font_size * 1.2, text_rgb=(128, 0, 0)
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
    credit = 2
    GAMEOVER = -2


def create_surface_with_text(text, font_size, text_rgb):
    """ Returns surface with text written on """
    font = pygame.font.Font(os.path.join(
        BASE_ASSET_PATH, MENU_FONT_PATH), int(font_size))
    surface = font.render(text, True, text_rgb)
    return surface.convert_alpha()


SPAWN_COOLDOWN = 0.3
SHOOT_COOLDOWN = 0.5
SCORE_FONT_SIZE = 30


class Game:
    def __init__(self, papan):
        self.__dt = 0
        self.papan = papan

        #self.ship = None
        self.asteroids = []
        self.bullets = []
        self.bonuses = []
        self.vfxs = []
        self.bonus_timer = 0
        self.spawn_delay = 0
        self.shoot_delay = 0
        self.return_btn = Write(
            center_position=(140, 570),
            font_size=15,
            text_rgb=(255, 255, 255),
            text="Return to main menu",
            action=GameState.TITLE,
        )
        self.Menu = menu((self.papan.lebar, self.papan.tinggi), self.papan)
        self.game_state = GameState.TITLE
        #self.mouse_up = False
        self.score = 0
        self.heart = Heart()
        self.bonus_taken = 0
        self.shot_sfx= pygame.mixer.Sound(os.path.join(BASE_ASSET_PATH, SHOT_SOUND))
        self.dead_sfx= pygame.mixer.Sound(os.path.join(BASE_ASSET_PATH, DEAD_SOUND))

    def show_score(self, papan):
        font = pygame.font.Font(os.path.join(
            BASE_ASSET_PATH, SCORE_FONT_PATH), SCORE_FONT_SIZE)
        score_txt = font.render(f"Score : {self.score}", True, (255, 255, 255))
        self.papan.layar.blit(score_txt, (0, self.heart.rect.width))

    def show_health(self, papan, health):
        x = 0
        for i in range(health):
            self.heart.draw_pos(self.papan, (x, 0))
            x += self.heart.rect.width

    def game_loop(self):
        clock = pygame.time.Clock()

        while True:

            if self.game_state == GameState.TITLE:
                self.game_state = self.Menu.title_screen()

            if self.game_state == GameState.NEWGAME:
                self.game_state = self.start_game(clock)

            if self.game_state == GameState.credit:
                self.game_state = self.Menu.credit_screen()

            if self.game_state == GameState.GAMEOVER:
                self.game_state = self.Menu.gameover_screen()

            if self.game_state == GameState.QUIT:
                pygame.quit()
                return

    def draw(self):
        self.papan.draw()

        if self.ship != None:
            self.ship.draw(self.papan)

        for Asteorid in self.asteroids:
            Asteorid.draw(self.papan)

        for bullet in self.bullets:
            # pygame.mixer.Sound.play(self.papan.shot)
            bullet.draw(self.papan)

        for bonus in self.Bonuses:
            bonus.draw(self.papan)

        for vfx in self.vfxs:
            vfx.draw(self.papan)

        self.show_score(self.papan)
        self.show_health(self.papan, self.ship.health)
        self.return_btn.draw(self.papan.layar)
        pygame.display.flip()

    def update(self):
        mouse_up = False

        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        if self.spawn_delay > 0:
            self.spawn_delay -= self.__dt
        else:
            self.spawn_asteroid()
            self.spawn_delay = SPAWN_COOLDOWN

        if self.bonus_timer > 0:
            self.bonus_timer -= self.__dt
        else:
            self.bonus_timer = 0

        if self.shoot_delay > 0:
            self.shoot_delay -= self.__dt
        else:
            if keys[pygame.K_SPACE]:
                pygame.mixer.Sound.play(self.shot_sfx)
                self.shoot()
                self.shoot_delay = SHOOT_COOLDOWN

        for asteroid in self.asteroids:
            if pygame.sprite.collide_rect(asteroid, self.ship):
                self.ship.damage()
                self.create_explosions(asteroid.pos, asteroid.animations[0].frame_size)
                self.asteroids.remove(asteroid)
            asteroid.update(self.__dt)

        for bullet in self.bullets:
            if bullet.pos[1] < 0:
                self.bullets.remove(bullet)
                continue

            for asteroid in self.asteroids:
                if pygame.sprite.collide_rect(bullet, asteroid):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    self.create_explosions(asteroid.pos, asteroid.animations[0].frame_size)
                    self.score += 1 if asteroid.rect.width <= 80 else 5
                    self.asteroid_shooted += 1
                    if self.asteroid_shooted >= 5:
                        self.asteroid_shooted = 0
                        self.create_bonus(asteroid.pos)

            bullet.update(self.__dt)

        for bonus in self.Bonuses:
            if pygame.sprite.collide_rect(bonus, self.ship):
                self.Bonuses.remove(bonus)
                self.get_bonus()
                self.bonus_taken += 1
                if self.bonus_taken % 10 == 0:
                    self.ship.upgrade_ship()
            bonus.update(self.__dt)

        for vfx in self.vfxs:
            if vfx.anim_done():
                self.vfxs.remove(vfx)

        if self.ship != None:
            self.ship.update(self.papan, self.__dt)

        if self.ship.isDestroyed():
            self.play = False

        self.Menu.ui_action = self.return_btn.update(
            pygame.mouse.get_pos(), mouse_up)
        if self.Menu.ui_action:
            self.play = False

        self.papan.update()
    # mendapatkan jarak waktu antara dua frame dalam satuan detik

    def delta_time(self, time_between):
        return time_between / 1000.0

    def get_bonus(self):
        self.bonus_timer = 3

    def spawn_asteroid(self):
        rand_scale = randint(40, 100)
        y = -rand_scale
        x = randint(0, self.papan.lebar - rand_scale)
        new_asteroid = Asteroid([x, y], (rand_scale, rand_scale))
        self.asteroids.append(new_asteroid)

    def shoot(self):

        if self.bonus_timer <= 0:
            x = self.ship.rect.topleft[0] + \
                (self.ship.rect.width/2) - (BULLET_SCALE[0]/2) - 2
            y = self.ship.rect.topleft[1] - (BULLET_SCALE[1]/2)
            new_bullet = Bullet([x, y])
            self.bullets.append(new_bullet)
        else:
            x = self.ship.rect.topleft[0] + \
                (self.ship.rect.width/2) - (BULLET_SCALE[0]/2) - 2
            y = self.ship.rect.topleft[1] - (BULLET_SCALE[1]/2)
            new_bullet = Bullet([x, y])

            self.bullets.append(new_bullet)

            x = self.ship.rect.topleft[0] + \
                (self.ship.rect.width/2) - (BULLET_SCALE[0]/2) - 22
            y = self.ship.rect.topleft[1] - (BULLET_SCALE[1]/2) + 20
            new_bullet = Bullet([x, y])

            self.bullets.append(new_bullet)

            x = self.ship.rect.topleft[0] + \
                (self.ship.rect.width/2) - (BULLET_SCALE[0]/2) + 18
            y = self.ship.rect.topleft[1] - (BULLET_SCALE[1]/2) + 20
            new_bullet = Bullet([x, y])

            self.bullets.append(new_bullet)

    def create_bonus(self, pos):
        x = pos[0]
        y = pos[1]
        new_bonus = Bonus([x, y])
        self.Bonuses.append(new_bonus)
    
    def create_explosions(self, pos, scale):
        x = pos[0]
        y = pos[1]
        new_explosions = Explosions_vfx([x, y], scale)
        self.vfxs.append(new_explosions)
        
    def start_game(self, clock):
        self.ship = Ship((800, 600), 150, 4, 1)
        self.asteroids = []
        self.bullets = []
        self.Bonuses = []
        self.score = 0
        self.asteroid_shooted = 0
        self.play = True

        while self.play:
            # print(self.play)
            self.update()

            self.draw()
            #print(self.vfxs)
            self.__dt = self.delta_time(clock.tick(FPS))

        if self.ship.isDestroyed():
            pygame.mixer.Sound.play(self.dead_sfx)
            return GameState.GAMEOVER
        else:
            return GameState.TITLE
