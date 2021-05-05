from permainan import *


jendela_1 = Papan((800, 600))
permainan = Permainan(jendela_1) 

def main():
    permainan.perulangan_permainan()
    permainan.quit()

 
if __name__ == "__main__":
    main()

