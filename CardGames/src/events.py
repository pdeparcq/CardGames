__author__ = 'GAG569'

class QuitEvent:
    def __init__(self):
        pass

class TickEvent:
    def __init__(self):
        pass

class DrawEvent:
    def __init__(self,surface):
        self.surface = surface

class MouseEvent:
    def __init__(self,event):
        self.detail = event

class KeyEvent:
    def __init__(self,event):
        self.detail = event