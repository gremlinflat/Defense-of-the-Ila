import pygame 

class Entity():
    def __init__(self):
        #super().__init__()
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

    def draw_pos(self, window, pos):
        if self.selected_animation > self.next_animation:
            self.selected_animation -= 1
        elif self.selected_animation < self.next_animation:
            self.selected_animation += 1
        
        self.animations[self.selected_animation].draw(window, pos)

    
    def update(self):
        pass
    
    def _add_animation(self, Animation):
        if type(Animation) is list:
            self.animations.extend(Animation)
        else:
            self.animations.append(Animation)
    def _set_next_anim(self, idx):
        self.next_animation = idx
    def _set_animation(self, idx):
        self.selected_animation = idx
        self.next_animation = idx

    def scale(self, size):
        for an in self.animations:
            an.scale(size)