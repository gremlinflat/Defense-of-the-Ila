import pygame 

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animations = []
        self.next_animation = 0
        self.selected_animation = 0
        self.pos = [0,0]
        
    def draw(self, window):
        if self.selected_animation > self.next_animation:
            self.selected_animation -= 1
        elif self.selected_animation < self.next_animation:
            self.selected_animation += 1

        self.animations[self.selected_animation].draw(window, self.pos)

    def update(self):
        pass
    
    def _addAnimation(self, Animation):
        if type(Animation) is list:
            self.animations.extend(Animation)
        else:
            self.animations.append(Animation)
    def _setnextAnim(self, idx):
        self.next_animation = idx
    def _setAnimation(self, idx):
        self.selected_animation = idx
        self.next_animation = idx