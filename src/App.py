import pygame

class App:
    def __init__(self):
        self.running = True
        self.screen = None
        self.clock = None

    def init(self, w, h):
        pygame.init()
        self.screen = pygame.display.set_mode((w, h))
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
        while self.running:
            self._events()
            self._draw()
            self._update()

pygame.quit()