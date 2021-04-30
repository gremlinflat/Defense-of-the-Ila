from game import *


win = Papan((800, 600))
game = Game(win) 

def main():
    game.game_loop()
    game.quit()

 
if __name__ == "__main__":
    main()

