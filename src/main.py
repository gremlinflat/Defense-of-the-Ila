from game import Game, Window

DISPLAY_SIZE = (800, 600)

win = Window(DISPLAY_SIZE)
game = Game(win)


def main():
    game.game_loop()


if __name__ == "__main__":
    main()
