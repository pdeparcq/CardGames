__author__ = 'GAG569'

import pygame
import util
import events

ResourceManager = util.ResourceManager()

class Component:
    def __init__(self):
        self.entity = None
    def set_entity(self,entity):
        self.entity = entity
    def post_event(self,event):
        if not self.entity is None:
            self.entity.post_event(event)
        else:
            self.handle_event(event)
    def handle_event(self,event):
        pass

class Entity(Component):
    def __init__(self):
        Component.__init__(self)
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
    def handle_event(self,event):
        for c in self.get_components():
            c.handle_event(event)

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
        if isinstance(event,events.MouseEvent):
            event = event.detail
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
    def handle_event(self,event):
        if isinstance(event,events.DrawEvent):
            event.surface.blit(self.image,(self.position.x,self.position.y))

class Card(Entity):
    def __init__(self,card):
        Entity.__init__(self)
        self.set_model(card)
        self.add_component(Position())
        self.add_component(Draggable())
        self.add_component(CardRenderer())
    def set_model(self,card):
        self.card = card


class Screen(Component):
    def __init__(self):
        Component.__init__(self)
        self.surface = pygame.display.set_mode((800, 600))
    def handle_event(self,event):
        if isinstance(event,events.TickEvent):
            self.surface.fill((0,0,0))
            self.post_event(events.DrawEvent(self.surface))
            pygame.display.flip()

class MouseController(Component):
    def __init__(self):
        Component.__init__(self)
    def handle_event(self,event):
        if isinstance(event,events.TickEvent):
            for me in pygame.event.get([pygame.MOUSEBUTTONDOWN,pygame.MOUSEBUTTONUP,pygame.MOUSEMOTION]):
                self.post_event(events.MouseEvent(me))


class GameEngine(Component):
    def __init__(self):
        Component.__init__(self)
        self.isRunning = True
        self.clock = pygame.time.Clock()
    def run(self):
        while self.isRunning:
            self.post_event(events.TickEvent())
            #clear pygame events that were not handled
            pygame.event.clear()
            self.clock.tick(30)
    def handle_event(self,event):
        if isinstance(event,events.QuitEvent):
            self.isRunning = False

class Game(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.engine = GameEngine()
        self.add_component(self.engine)
        self.add_component(Screen())
        self.add_component(MouseController())
    def play(self):
        self.engine.run()
