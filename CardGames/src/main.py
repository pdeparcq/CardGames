# To change this template, choose Tools | Templates
# and open the template in the editor.

import sys
import view

__author__="GAG569"
__date__ ="$29-jan-2012 8:54:54$"


def main():
    try:
        game = view.Game()
        game.add_item(view.Card())
        game.play()
        return 0
    except:
        return -1
    
if __name__ == "__main__":
    sys.exit(main())
