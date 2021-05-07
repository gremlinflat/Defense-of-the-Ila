import pygame
from Entity import Entity
from SpriteAnim import Animation
import random

class Bullet():
    def __init__(self):
        pass

ASTEROID_PATH = "Meteor_05.png"
class Asteroid(Entity):
    def __init__(self, pos, scale):
        super().__init__()
        self.pos = pos
        self._addAnimation(Animation(ASTEROID_PATH, 1, 1, False))
        self.scale(scale)
        self.rect = pygame.Rect(pos, self.animations[0].frame_size)
        self.speed = 50
        self.vec = [random.uniform(-0.5, 0.5), 1]
        
        
    
    def update(self, dt):
        self.pos[0] = self.pos[0] + (self.vec[0] * self.speed * dt)
        self.pos[1] = self.pos[1] + (self.vec[1] * self.speed * dt)
        self.rect.center = tuple(self.pos)

    def collision(self, ship):
        #print(ship.rect)
        if pygame.sprite.collide_rect(self, ship):
            print('destroy')
            


    