__author__ = 'GAG569'

import pygame

class ResourceManager:
    BASE_PATH = "../res"
    IMAGE_PATH = "/img/"
    def __init__(self):
        self.images = {}
    def get_image(self,name):
        if not self.images.__contains__(name):
            self.images[name] = pygame.image.load(ResourceManager.BASE_PATH+ResourceManager.IMAGE_PATH+name+".gif")
        return self.images[name]

