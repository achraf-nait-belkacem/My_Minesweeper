from abc import ABC, abstractmethod


class StateAbstract(ABC):
    def __init__(self):
        self.setup = True

    @abstractmethod
    def init(self, app):
        pass

    @abstractmethod
    def events(self, app, event):
        pass

    @abstractmethod
    def update(self, app):
        pass

    @abstractmethod
    def draw(self, app):
        pass
