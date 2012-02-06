# To change this template, choose Tools | Templates
# and open the template in the editor.

import sys
import domain
import view

__author__="GAG569"
__date__ ="$29-jan-2012 8:54:54$"


def main():
    try:
        game = view.Game()
        deck = domain.DeckFactory().create_deck()
        deck.shuffle()
        game.add_component(view.Card(deck.get()))
        game.play()
        return 0
    except:
        for info in sys.exc_info():
            print info
        return -1
    
if __name__ == "__main__":
    sys.exit(main())
