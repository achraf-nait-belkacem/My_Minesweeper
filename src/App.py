import pygame

class App:
    def __init__(self, w, h, scaling):
        self.running = True
        self.screen = None
        self.clock = None
        self.scaling = scaling
        self.window_w = w
        self.window_h = h

    def _init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((int(self.window_w * self.scaling), int(self.window_h * self.scaling)))
        self.clock = pygame.time.Clock()

    def _draw(self):
        self.screen.fill("purple")

    def _events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self):
        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        self._init()
        while self.running:
            self._events()
            self._draw()
            self._update()

pygame.quit()