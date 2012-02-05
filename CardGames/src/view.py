__author__ = 'GAG569'

import pygame
import pygame.image
import util

ResourceManager = util.ResourceManager()

class Card:
    def __init__(self,card):
        self.x = 0
        self.y = 0
        self.set_model(card)
    def set_model(self,card):
        self.card = card
        self.image = ResourceManager.get_image(self.card.suit.name + ("%02d" % self.card.symbol.value))
    def draw(self,surface):
        surface.blit(self.image,(self.x,self.y))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.isRunning = True
        self.items = []
        self.clock = pygame.time.Clock()
    def add_item(self,item):
        self.items.append(item)
    def handle_events(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.isRunning = False
    def update(self):
        pass
    def display(self):
        self.screen.fill((0,0,0))
        for i in self.items:
            i.draw(self.screen)
        pygame.display.flip()
    def play(self):
        while self.isRunning:
            self.handle_events()
            self.update()
            self.display()
            self.clock.tick(30)