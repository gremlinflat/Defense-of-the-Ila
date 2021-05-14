from game import *

BESAR_LAYAR = (800, 600)

win = Papan(BESAR_LAYAR)
game = Game(win) 

def main():
    game.game_loop()
    game.quit()

 
if __name__ == "__main__":
    main()

