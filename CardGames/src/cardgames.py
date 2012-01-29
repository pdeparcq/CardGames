# To change this template, choose Tools | Templates
# and open the template in the editor.

import sys
import pygame

__author__="GAG569"
__date__ ="$29-jan-2012 8:54:54$"

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.isRunning = True
    def handle_events(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.isRunning = False
    def update(self):
        pass
    def display(self):
        self.screen.fill((0,0,255))
        pygame.display.flip()
    def play(self):
        while self.isRunning:
            self.handle_events()
            self.update()
            self.display()
            
def main():
    try:
        Game().play()
        return 0
    except:
        return -1
    
if __name__ == "__main__":
    sys.exit(main())
