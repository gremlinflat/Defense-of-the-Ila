from game import *


win = Window((800, 600))
game = Game(win) 

def main():
    game.game_loop()
    game.quit()

 
if __name__ == "__main__":
    main()

