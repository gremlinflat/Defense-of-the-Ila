import pygame 

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animations = []
        self.selected_animation = 0
        self.pos = [0,0]
        
    def draw(self, window):
        self.animations[self.selected_animation].draw(window, self.pos)

    def update(self):
        pass
    
    def _addAnimation(self, Animation, count):
        self.animations.append(Animation)

    def _setAnimation(self, idx):
        self.selected_animation = idx