import window_lib

win = window_lib.Window((800, 600))
game = window_lib.Game(win)

game.game_loop()
game.quit()
