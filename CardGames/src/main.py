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
        card = deck.get()
        i=0
        while card is not None:
            c = view.Card(card)
            c.x = ((i%10)*80)+3
            c.y = ((i/10)*100)+3
            game.add_item(c)
            card = deck.get()
            i+=1
        game.play()
        return 0
    except:
        for info in sys.exc_info():
            print info
        return -1
    
if __name__ == "__main__":
    sys.exit(main())
