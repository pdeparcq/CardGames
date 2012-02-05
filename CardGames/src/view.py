__author__ = 'GAG569'

import pygame
import pygame.image
import util

ResourceManager = util.ResourceManager()

class Component:
    def set_entity(self,entity):
        self.entity = entity
    def handle_event(self,event):
        pass
    def update(self):
        pass
    def draw(self,surface):
        pass

class Entity:
    def __init__(self):
        self.components = {}
    def add_component(self,component):
        self.components[component.__class__.__name__] = component
        component.set_entity(self)
    def get_component(self,name):
        if self.components.__contains__(name):
            return self.components[name]
        return None
    def get_components(self):
        return self.components.values()

class Position(Component):
    def set_entity(self,entity):
        Component.set_entity(self,entity)
        self.x = 0
        self.y = 0

class Draggable(Component):
    def set_entity(self,entity):
        Component.set_entity(self,entity)
        self.offset_x = 0
        self.offset_y = 0
        self.is_dragging = False
        self.position = entity.get_component("Position")
    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.offset_x = event.pos[0] - self.position.x
                self.offset_y = event.pos[1]- self.position.y
                self.is_dragging = True
        if event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                self.position.x = event.pos[0] - self.offset_x
                self.position.y = event.pos[1] - self.offset_y
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False

class CardRenderer(Component):
    def set_entity(self,entity):
        Component.set_entity(self,entity)
        self.position = entity.get_component("Position")
        self.image = ResourceManager.get_image(entity.card.suit.name + ("%02d" % entity.card.symbol.value))
    def draw(self,surface):
        surface.blit(self.image,(self.position.x,self.position.y))

class Card(Entity):
    def __init__(self,card):
        Entity.__init__(self)
        self.set_model(card)
        self.add_component(Position())
        self.add_component(Draggable())
        self.add_component(CardRenderer())
    def set_model(self,card):
        self.card = card

class EntityManager:
    def __init__(self):
        self.entities = []
    def add_entity(self,entity):
        self.entities.append(entity)
    def handle_event(self,event):
        for e in self.entities:
            for c in e.get_components():
                c.handle_event(event)
    def update(self):
        for e in self.entities:
            for c in e.get_components():
                c.update()
    def draw(self,surface):
        for e in self.entities:
            for c in e.get_components():
                c.draw(surface)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.isRunning = True
        self.entityManager = EntityManager()
        self.clock = pygame.time.Clock()
    def add_item(self,item):
        self.entityManager.add_entity(item)
    def handle_events(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.isRunning = False
        else:
            self.entityManager.handle_event(event)
    def update(self):
        self.entityManager.update()
    def display(self):
        self.screen.fill((0,0,0))
        self.entityManager.draw(self.screen)
        pygame.display.flip()
    def play(self):
        while self.isRunning:
            self.handle_events()
            self.update()
            self.display()
            self.clock.tick(30)