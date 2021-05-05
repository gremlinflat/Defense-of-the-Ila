import pygame, sys
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum

RED = (128,0,0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0,0,0)


def create_surface_with_text(text, font_size, text_rgb):
    """ Returns surface with text written on """
    font = pygame.font.Font("assets\Vermin Vibes 1989.ttf", int(font_size))
    surface= font.render(text,True,text_rgb)
    return surface.convert_alpha()

class UIElement(Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
        """
        self.mouse_over = False  # indicates if the mouse is over the element

        # create the default image
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb
        )

        # create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=RED
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

def title_screen(screen,layar):
    start_btn = UIElement(
        center_position=(395, 325),
        font_size=45,
        text_rgb=YELLOW,
        text="PLAY",
        action=GameState.NEWGAME,
    )

    credit_btn = UIElement(
        center_position=(395, 400),
        font_size=45,
        text_rgb=YELLOW,
        text="CREDIT",
        action=GameState.NEWGAME,
    )

    quit_btn = UIElement(
        center_position=(400, 470),
        font_size=45,
        text_rgb=YELLOW,
        text="EXIT",
        action=GameState.QUIT,
    )

    buttons = [start_btn,credit_btn, quit_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            screen.blit(layar,(0,0))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()

def play_level(screen,layar):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=15,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.blit(layar,(0,0))

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(screen)

        pygame.display.flip()

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    surface_second = pygame.Surface((130,50))
    layar = pygame.image.load("assets/menu logo clear.png")
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            screen.blit(layar,(0,0))
            surface_second.fill(RED)
            screen.blit(surface_second,(330,300))
            
            game_state = title_screen(screen,layar)

        if game_state == GameState.NEWGAME:
            game_state = play_level(screen,layar)

        if game_state == GameState.QUIT:
            pygame.quit()
            return

if __name__ == "__main__":
    main()