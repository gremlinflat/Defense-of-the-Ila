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
CREDIT_IMAGE_PATH = "credit-pop up.png"
GAMEOVER_IMAGE_PATH = "game over1.png"
HEALTH_IMAGE_PATH = "health-bar 1.png"
MENU_FONT_PATH = "Vermin Vibes 1989.ttf"
SCORE_FONT_PATH = "Minecraft.ttf"
SHOT_SOUND = "laser2.mp3"
BACKGROUND_SOUND = "Background Menu Sound.mp3"
BONUS_SOUND = "item bonus sound.mp3"
DEAD_SOUND = "death.mp3"
EXPLOSION_SOUND = "explosion_sound.mp3"
FPS = 60
# class layar


class Window:
    def __init__(self, window_size):
        # inisialisasi pygame
        pygame.init()
        pygame.mixer.init()

        self.width = window_size[0]
        self.height = window_size[1]
        # membuat object layar dengan sebesar {window_size}
        self.display = pygame.display.set_mode(window_size)

        self.bgimage = pygame.image.load(os.path.join(
            BASE_ASSET_PATH, PARALLAX_BG_PATH_FROM_ASSET))

        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = -self.rectBGimg.height
        self.bgX2 = 0

        self.speed = 2

    def update(self):
        self.bgY1 += self.speed
        self.bgY2 += self.speed
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height

    def draw(self):
        self.display.blit(self.bgimage, (self.bgX2, self.bgY2))
        self.display.blit(self.bgimage, (self.bgX1, self.bgY1))


class menu():
    def __init__(self, window_size, window):

        self.gambar = pygame.image.load(
            os.path.join(BASE_ASSET_PATH, MENU_IMAGE_PATH))
        self.credit_image = pygame.image.load(
            os.path.join(BASE_ASSET_PATH, CREDIT_IMAGE_PATH))
        self.gameover_image = pygame.image.load(
            os.path.join(BASE_ASSET_PATH, GAMEOVER_IMAGE_PATH))
        self.window = window

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
            self.window.display.blit(self.gambar, (0, 0))

            for button in self.buttons:
                self.ui_action = button.update(
                    pygame.mouse.get_pos(), mouse_up)
                if self.ui_action is not None:
                    return self.ui_action
                button.draw(self.window.display)

            pygame.display.flip()

    def credit_screen(self):
        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            self.window.display.blit(self.credit_image, (0, 0))

            self.ui_action = self.return_btn.update(
                pygame.mouse.get_pos(), mouse_up)
            if self.ui_action is not None:
                return self.ui_action

            self.return_btn.draw(self.window.display)

            pygame.display.flip()

    def gameover_screen(self):
        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            self.window.display.blit(self.gameover_image, (0, 0))

            self.ui_action = self.return_btn.update(
                pygame.mouse.get_pos(), mouse_up)
            if self.ui_action is not None:
                return self.ui_action

            self.return_btn.draw(self.window.display)

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
    def __init__(self, window):
        self.__dt = 0
        self.window = window
        self.bg_sfx = pygame.mixer.Sound(
            os.path.join(BASE_ASSET_PATH, BACKGROUND_SOUND))
        self.bonus_sfx = pygame.mixer.Sound(
            os.path.join(BASE_ASSET_PATH, BONUS_SOUND))
        self.explosion_sfx = pygame.mixer.Sound(
            os.path.join(BASE_ASSET_PATH, EXPLOSION_SOUND))
        #self.ship = None
        self.asteroids = []
        self.bullets = []
        self.bonuses = []
        self.vfxs = []
        self.bonus_timer = 0
        self.spawn_delay = 0
        self.shoot_delay = 0
        self.score = 0
        self.bonus_taken = 0
        self.return_btn = Write(
            center_position=(140, 570),
            font_size=15,
            text_rgb=(255, 255, 255),
            text="Return to main menu",
            action=GameState.TITLE,
        )
        self.Menu = menu((self.window.width, self.window.height), self.window)
        self.game_state = GameState.TITLE
        #self.mouse_up = False
        self.heart = Heart()
        self.shot_sfx = pygame.mixer.Sound(
            os.path.join(BASE_ASSET_PATH, SHOT_SOUND))
        self.dead_sfx = pygame.mixer.Sound(
            os.path.join(BASE_ASSET_PATH, DEAD_SOUND))

    def show_score(self, window):
        font = pygame.font.Font(os.path.join(
            BASE_ASSET_PATH, SCORE_FONT_PATH), SCORE_FONT_SIZE)
        score_txt = font.render(f"Score : {self.score}", True, (255, 255, 255))
        self.window.display.blit(score_txt, (0, self.heart.rect.width))

    def show_health(self, window, health):
        x = 0
        for i in range(health):
            self.heart.draw_pos(self.window, (x, 0))
            x += self.heart.rect.width

    def game_loop(self):
        clock = pygame.time.Clock()

        while True:

            if self.game_state == GameState.TITLE:
                pygame.mixer.Sound.play(self.bg_sfx)
                self.game_state = self.Menu.title_screen()

            if self.game_state == GameState.NEWGAME:
                pygame.mixer.Sound.stop(self.bg_sfx)
                self.game_state = self.start_game(clock)

            if self.game_state == GameState.credit:
                self.game_state = self.Menu.credit_screen()

            if self.game_state == GameState.GAMEOVER:
                self.game_state = self.Menu.gameover_screen()

            if self.game_state == GameState.QUIT:
                pygame.quit()
                return

    def draw(self):
        self.window.draw()

        if self.ship != None:
            self.ship.draw(self.window)

        for Asteorid in self.asteroids:
            Asteorid.draw(self.window)

        for bullet in self.bullets:
            # pygame.mixer.Sound.play(self.window.shot)
            bullet.draw(self.window)

        for bonus in self.bonuses:
            bonus.draw(self.window)

        for vfx in self.vfxs:
            vfx.draw(self.window)

        self.show_score(self.window)
        self.show_health(self.window, self.ship.health)
        self.return_btn.draw(self.window.display)
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
                self.ship.reset_pos()
                self.create_explosions(
                    asteroid.pos, asteroid.animations[0].frame_size)
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
                    self.create_explosions(
                        asteroid.pos, asteroid.animations[0].frame_size)
                    self.score += 1 if asteroid.rect.width <= 80 else 5
                    self.asteroid_shooted += 1
                    if self.asteroid_shooted >= 5:
                        self.asteroid_shooted = 0
                        self.create_bonus(asteroid.pos)

            bullet.update(self.__dt)

        for bonus in self.bonuses:
            if pygame.sprite.collide_rect(bonus, self.ship):
                self.bonuses.remove(bonus)
                self.get_bonus()
                self.bonus_taken += 1
                if self.bonus_taken % 10 == 0:
                    self.ship.upgrade_ship()
            bonus.update(self.__dt)

        for vfx in self.vfxs:
            if vfx.anim_done():
                self.vfxs.remove(vfx)

        if self.ship != None:
            self.ship.update(self.window, self.__dt)

        if self.ship.isDestroyed():
            self.play = False

        self.Menu.ui_action = self.return_btn.update(
            pygame.mouse.get_pos(), mouse_up)
        if self.Menu.ui_action:
            self.play = False

        self.window.update()
    # mendapatkan jarak waktu antara dua frame dalam satuan detik

    def mili_to_second(self, time_between):
        return time_between / 1000.0

    def get_bonus(self):
        self.bonus_timer = 3
        pygame.mixer.Sound.play(self.bonus_sfx)

    def spawn_asteroid(self):
        rand_scale = randint(40, 100)
        y = -rand_scale
        x = randint(0, self.window.width - rand_scale)
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
        self.bonuses.append(new_bonus)

    def create_explosions(self, pos, scale):
        x = pos[0]
        y = pos[1]
        new_explosions = Explosions_vfx([x, y], scale)
        self.vfxs.append(new_explosions)
        pygame.mixer.Sound.play(self.explosion_sfx)

    def start_game(self, clock):
        self.ship = Ship((400, 600), 150)
        self.asteroids = []
        self.bullets = []
        self.bonuses = []
        self.vfxs = []
        self.shoot_delay = 0
        self.score = 0
        self.bonus_taken = 0
        self.asteroid_shooted = 0
        self.play = True

        while self.play:
            # print(self.play)
            self.update()

            self.draw()
            # print(self.vfxs)
            self.__dt = self.mili_to_second(clock.tick(FPS))

        if self.ship.isDestroyed():
            pygame.mixer.Sound.play(self.dead_sfx)
            return GameState.GAMEOVER
        else:
            return GameState.TITLE
