import pygame

from src.MenuState import MenuState


class App:
    def __init__(self, w, h, scaling):
        self.running = True
        self.screen = None
        self.clock = None
        self.scaling = scaling
        self.window_w = w
        self.window_h = h
        self.dt = None
        self.state = None
        self.board_rows = 12
        self.board_cols = 14
        self.board_mines = 10

    def _init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((int(self.window_w * self.scaling), int(self.window_h * self.scaling)))
        self.clock = pygame.time.Clock()
        self.state = MenuState()
        self.state.init(self)

    def _draw(self):
        self.state.draw(self)

    def _events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.state.events(self, event)

    def _update(self):
        self.state.update(self)
        pygame.display.flip()
        self.dt = self.clock.tick(60) / 1000.0

    def run(self):
        self._init()
        while self.running:
            self._events()
            self._draw()
            self._update()
        pygame.quit()
