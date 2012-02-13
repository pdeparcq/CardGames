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
        if not self.entity is None:
            return self.entity.get_component(name)
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
        self.sprite = entity.get_component("Sprite")
    def handle_event(self,event):
        if isinstance(event,events.MouseEvent):
            event = event.detail
            if event.type == pygame.MOUSEBUTTONDOWN and self.sprite.get_bounding_rectangle().collidepoint(event.pos[0],event.pos[1]):
                if event.button == 1:
                    self.offset_x = event.pos[0] - self.position.x
                    self.offset_y = event.pos[1]- self.position.y
                    self.is_dragging = True
                    self.sprite.set_layer("front")
            if event.type == pygame.MOUSEMOTION:
                if self.is_dragging:
                    self.position.x = event.pos[0] - self.offset_x
                    self.position.y = event.pos[1] - self.offset_y
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.is_dragging:
                    self.is_dragging = False
                    self.sprite.set_layer("back")



class Sprite(Component):
    def set_entity(self,entity):
        Component.set_entity(self,entity)
        self.position = entity.get_component("Position")
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.Surface((0,0))
        self.sprite.rect = pygame.Rect(0,0,0,0)
    def set_layer(self,name):
        screen = self.entity.get_component("Screen")
        screen.set_layer(name,self)
    def set_image(self,image):
        self.image = image
    def get_width(self):
        return self.image.get_width()
    def get_height(self):
        return self.image.get_height()
    def get_bounding_rectangle(self):
        return pygame.Rect(self.position.x,self.position.y,self.get_width(),self.get_height())
    def handle_event(self,event):
        if isinstance(event,events.TickEvent):
            self.sprite.image = self.image
            self.sprite.rect = self.get_bounding_rectangle()

class Card(Entity):
    def __init__(self,card):
        Entity.__init__(self)
        self.add_component(Position())
        self.add_component(Sprite())
        self.add_component(Draggable())
        self.set_model(card)
    def set_entity(self,entity):
        Component.set_entity(self,entity)
        self.get_component("Sprite").set_layer("back")
    def set_model(self,card):
        self.card = card
        self.get_component("Sprite").set_image(ResourceManager.get_image(card.suit.name + ("%02d" % card.symbol.value)))

class Screen(Component):
    def __init__(self):
        Component.__init__(self)
        self.surface = pygame.display.set_mode((800, 600))
        self.layers = {}
    def set_layer(self,name,sprite):
        if not self.layers.has_key(name):
            self.layers[name] = pygame.sprite.LayeredUpdates()
        for group in self.layers.values():
            if group.has(sprite.sprite):
                group.remove(sprite.sprite)
        self.layers[name].add(sprite.sprite)
    def handle_event(self,event):
        if isinstance(event,events.TickEvent):
            self.surface.fill((0,0,0))
            #self.post_event(events.DrawEvent(self.surface))
            for group in self.layers.values():
                group.draw(self.surface)
            pygame.display.flip()

class MouseController(Component):
    def __init__(self):
        Component.__init__(self)
    def handle_event(self,event):
        if isinstance(event,events.TickEvent):
            if pygame.event.peek(pygame.QUIT):
                self.post_event(events.QuitEvent())
            for me in pygame.event.get([pygame.MOUSEBUTTONDOWN,pygame.MOUSEBUTTONUP,pygame.MOUSEMOTION]):
                self.post_event(events.MouseEvent(me))

class KeyboardController(Component):
    def __init__(self):
        Component.__init__(self)
    def handle_event(self,event):
        if isinstance(event,events.TickEvent):
            for ke in pygame.event.get([pygame.KEYDOWN,pygame.KEYUP]):
                self.post_event(events.KeyEvent(ke))

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
            #only send ticks at certain frame rate
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
        self.add_component(KeyboardController())
    def play(self):
        self.engine.run()
    def handle_event(self,event):
        if isinstance(event,events.KeyEvent):
            if event.detail.type==pygame.KEYUP and event.detail.key==pygame.K_ESCAPE:
                self.post_event(events.QuitEvent())
        Entity.handle_event(self,event)