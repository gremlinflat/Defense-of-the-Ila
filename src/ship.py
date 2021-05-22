import pygame
from Entity import Entity
from SpriteAnim import Animation

WIN_SIZE = (800, 600)

KEY_DICT = {
    pygame.K_w: (0, -1),
    pygame.K_s: (0,  1),
    pygame.K_d: (1,  0),
    pygame.K_a: (-1, 0),
}


SHIP_ANIMATIONS_PATH = [{
    "idle": "ship/ship_normal_level1.png",
    "left": "ship/ship_left_level1.png",
    "right": "ship/ship_right_level1.png",
    "sleft": "ship/ship_sleft_level1.png",
    "sright": "ship/ship_sright_level1.png",

},
    {
    "idle": "ship/ship_normal_level2.png",
    "left": "ship/ship_left_level2.png",
    "right": "ship/ship_right_level2.png",
    "sleft": "ship/ship_sleft_level2.png",
    "sright": "ship/ship_sright_level2.png",
}]


class Ship(Entity):
    def __init__(self, pos, speed):
        super().__init__()
        self.current_ship = 0
        self._addAnimation([
            Animation(
                SHIP_ANIMATIONS_PATH[self.current_ship]["left"], 4, True),
            Animation(
                SHIP_ANIMATIONS_PATH[self.current_ship]["sleft"], 4, True),
            Animation(
                SHIP_ANIMATIONS_PATH[self.current_ship]["idle"], 4, True),
            Animation(
                SHIP_ANIMATIONS_PATH[self.current_ship]["sright"], 4, True),
            Animation(
                SHIP_ANIMATIONS_PATH[self.current_ship]["right"], 4, True)
        ])
        self.start_pos = [pos[0], pos[1] - self.animations[0].frame_size[1]]
        self.rect = pygame.Rect(
            [pos[0], pos[1] - self.animations[0].frame_size[1]], self.animations[0].frame_size)

        self.pos = list(self.rect.topleft)
        self.speed = float(speed)

        # (vec[0], vec[1]) == (x, y)
        self.vec = (0.0, 0.0)
        self.health = 3

    def reset_pos(self):
        print(self.start_pos)
        self.reset_ship()
        self.pos = [self.start_pos[0], self.start_pos[1]]

    def upgrade_ship(self):
        if self.current_ship + 1 >= len(SHIP_ANIMATIONS_PATH):
            return
        self.current_ship += 1

        new_animations = [
            Animation(
                SHIP_ANIMATIONS_PATH[self.current_ship]["left"], 4, True),
            Animation(
                SHIP_ANIMATIONS_PATH[self.current_ship]["sleft"], 4, True),
            Animation(
                SHIP_ANIMATIONS_PATH[self.current_ship]["idle"], 4, True),
            Animation(
                SHIP_ANIMATIONS_PATH[self.current_ship]["sright"], 4, True),
            Animation(
                SHIP_ANIMATIONS_PATH[self.current_ship]["right"], 4, True)
        ]
        self.animations = new_animations

    def reset_ship(self):
        self.current_ship = 0

        new_animations = [
            Animation(
                SHIP_ANIMATIONS_PATH[self.current_ship]["left"], 4, True),
            Animation(
                SHIP_ANIMATIONS_PATH[self.current_ship]["sleft"], 4, True),
            Animation(
                SHIP_ANIMATIONS_PATH[self.current_ship]["idle"], 4, True),
            Animation(
                SHIP_ANIMATIONS_PATH[self.current_ship]["sright"], 4, True),
            Animation(
                SHIP_ANIMATIONS_PATH[self.current_ship]["right"], 4, True)
        ]
        self.animations = new_animations

    def update(self, window, dt):
        keys = pygame.key.get_pressed()
        self.move(keys, dt)

        self.pos[1] = min(max(self.pos[1], 0),
                          window.height - (self.rect.height))

    # methon pergerakan pesawat

    def move(self, keys, dt):
        notPressed = True
        for key in KEY_DICT:  # untuk setiap key di KEY_DECT
            if keys[key]:  # kondisi jika w, a, s, d di tekan
                notPressed = False
                self.vec = KEY_DICT[key]
                self.pos[1] += self.vec[1] * self.speed * dt
                self.pos[0] += self.vec[0] * self.speed * dt
                if self.pos[0] < (-0.5*self.rect.width):
                    self.pos[0] = (WIN_SIZE[0] - (0.5*self.rect.width))
                elif self.pos[0] > WIN_SIZE[0]-(0.5*self.rect.width):
                    self.pos[0] = (-0.5*self.rect.width)

        if notPressed:  # kondisi jika w, a, s, d tidak di tekan
            self.vec = (0, 0)

        if self.vec[0] > 0:
            self._setnextAnim(4)
        elif self.vec[0] < 0:
            self._setnextAnim(0)
        else:
            self._setnextAnim(2)

        self.rect.topleft = tuple(self.pos)
        #print(self.pos)

    def damage(self):
        self.health -= 1

    def isDestroyed(self):
        return self.health <= 0
