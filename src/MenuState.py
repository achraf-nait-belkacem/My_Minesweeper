import pygame

class MenuState:
    def __init__(self):
        self.setup = True

    def setup(self, app):
        self.setup = False

    def draw(self, app):
        app.screen.fill("purple")

    def events(self, app, event):
        pass

    def update(self, app):
        pass