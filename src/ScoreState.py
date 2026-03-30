import json

import pygame

from src.StateAbstract import StateAbstract
from src.constants import SCORES_FILE


class ScoreState(StateAbstract):
    def __init__(self):
        super().__init__()
        self.best = None
        self.font = None

    def init(self, app):
        self.setup = False
        self.font = pygame.font.SysFont(None, 36)
        self.load_best()

    def load_best(self):
        self.best = None
        try:
            with open(SCORES_FILE, "r") as f:
                data = json.load(f)
            if isinstance(data, dict) and "best" in data:
                self.best = data["best"]
            elif isinstance(data, list) and data:
                self.best = min(data)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def draw(self, app):
        app.screen.fill((0, 0, 0))
        title = self.font.render("Best score", True, (255, 255, 255))
        app.screen.blit(title, (50, 20))

        if self.best is not None:
            line = self.font.render(f"Best time: {self.best} s (lower is better)", True, (255, 255, 255))
            app.screen.blit(line, (50, 80))
        else:
            line = self.font.render("No win recorded yet.", True, (180, 180, 180))
            app.screen.blit(line, (50, 80))

        text2 = self.font.render("Click anywhere to return", True, (255, 255, 0))
        app.screen.blit(text2, (50, 400))

    def events(self, app, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            from src.MenuState import MenuState

            app.state = MenuState()
            app.state.init(app)

    def update(self, app):
        pass
