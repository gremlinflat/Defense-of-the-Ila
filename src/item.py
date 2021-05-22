import pygame
from Entity import Entity
from SpriteAnim import Animation
from random import uniform, randint

BULLET_PATH = "bullet.png"
BULLET_SCALE = (10, 20)
BULLET_SPEED = 300
class Bullet(Entity):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self._add_animation(Animation(BULLET_PATH, 1, False))
        self.rect = pygame.Rect(pos, self.animations[0].frame_size)
        self.speed = BULLET_SPEED
        self.vec = [0, -1]
        self.scale(BULLET_SCALE)

    def update(self, dt):
        self.pos[0] = self.pos[0] + (self.vec[0] * self.speed * dt)
        self.pos[1] = self.pos[1] + (self.vec[1] * self.speed * dt)
        self.rect.center = tuple(self.pos)

ASTEROID_PATH = "meteor3.png"
BONUS_PATH = "rocket bonus.png"
HEART_PATH = "health-bar 1.png"
EXPLOSION_PATH = "explosionsprite.png"
class Asteroid(Entity):
    def __init__(self, pos, scale):
        super().__init__()
        self.pos = pos
        self._add_animation(Animation(ASTEROID_PATH, 1, False))
        self.scale(scale)
        self.rect = pygame.Rect(pos, self.animations[0].frame_size)
        self.speed = randint(100, 300)
        x = uniform(0.1, 0.5) if self.pos[0] < 400 else uniform(-0.5, -0.1)
        self.vec = [x, 1]
        
        
    
    def update(self, dt):
        self.pos[0] = self.pos[0] + (self.vec[0] * self.speed * dt)
        self.pos[1] = self.pos[1] + (self.vec[1] * self.speed * dt)
        self.rect.topleft = tuple(self.pos)

BONUS_SCALE = (30, 30)

class Bonus(Entity):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self._add_animation(Animation(BONUS_PATH, 1, False))
        self.scale(BONUS_SCALE)
        self.rect = pygame.Rect(pos, self.animations[0].frame_size)
        self.speed = 60
        x = uniform(-0.5, 0.5)
        self.vec = [x, 1]

    def update(self, dt):
        self.pos[0] = self.pos[0] + (self.vec[0] * self.speed * dt)
        self.pos[1] = self.pos[1] + (self.vec[1] * self.speed * dt)
        self.rect.topleft = tuple(self.pos)

class Heart(Entity):
    def __init__(self):
        super().__init__()
        self._add_animation(Animation(HEART_PATH, 1, False))
        self.scale(BONUS_SCALE)
        self.rect = pygame.Rect((0, 0), self.animations[0].frame_size)
    
class Explosions_vfx(Entity):
    def __init__(self, pos, scale):
        super().__init__()
        self.pos = pos
        self._add_animation(Animation(EXPLOSION_PATH, 4, False))
        self.scale(scale)
        self.rect = pygame.Rect(pos, self.animations[0].frame_size)
    
    def anim_done(self):
        return  self.animations[self.selected_animation].get_current_frame() >= self.animations[self.selected_animation].frame_count - 1