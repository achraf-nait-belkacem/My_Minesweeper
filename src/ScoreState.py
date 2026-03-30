import json

import pygame

from src.StateAbstract import StateAbstract
from src.constants import SCORES_FILE


class ScoreState(StateAbstract):
    def __init__(self):
        super().__init__()
        self.scores = []
        self.font = None
        self.title_font = None
        self.back_button = None

    @staticmethod
    def load_all_scores():
        try:
            with open(SCORES_FILE, "r") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
            # handle old format {"best": X}
            if isinstance(data, dict) and "best" in data:
                return [data["best"]]
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return []

    @staticmethod
    def load_best_score():
        scores = ScoreState.load_all_scores()
        return min(scores) if scores else None

    @staticmethod
    def save_score(seconds):
        scores = ScoreState.load_all_scores()
        scores.append(round(seconds, 2))
        scores.sort()
        with open(SCORES_FILE, "w") as f:
            json.dump(scores, f, indent=2)

    def init(self, app):
        self.setup = False
        self.font = pygame.font.SysFont(None, 32)
        self.title_font = pygame.font.SysFont(None, 48)
        self.scores = ScoreState.load_all_scores()
        w, h = app.screen.get_size()
        btn_w, btn_h = 120, 40
        self.back_button = pygame.Rect(w // 2 - btn_w // 2, h - 70, btn_w, btn_h)

    def draw(self, app):
        app.screen.fill((30, 30, 30))
        w, h = app.screen.get_size()

        title = self.title_font.render("Best Scores", True, (255, 255, 255))
        app.screen.blit(title, title.get_rect(centerx=w // 2, y=20))

        if not self.scores:
            msg = self.font.render("No wins recorded yet.", True, (180, 180, 180))
            app.screen.blit(msg, msg.get_rect(centerx=w // 2, y=100))
        else:
            header = self.font.render("Rank      Time (s)", True, (200, 200, 200))
            app.screen.blit(header, (w // 2 - 120, 80))
            pygame.draw.line(app.screen, (100, 100, 100), (w // 2 - 120, 108), (w // 2 + 120, 108), 1)

            for i, score in enumerate(self.scores[:10]):
                color = (255, 215, 0) if i == 0 else (255, 255, 255)
                if i + 1 == 10:
                    rank_text = f"#{i + 1:<8}   {score}"
                else:
                    rank_text = f"#{i + 1:<8}    {score}"
                line = self.font.render(rank_text, True, color)
                app.screen.blit(line, (w // 2 - 120, 118 + i * 30))

        pygame.draw.rect(app.screen, (160, 160, 160), self.back_button)
        back_text = self.font.render("BACK", True, (0, 0, 0))
        app.screen.blit(back_text, back_text.get_rect(center=self.back_button.center))

        hint = self.font.render("ESC to return", True, (120, 120, 120))
        app.screen.blit(hint, hint.get_rect(centerx=w // 2, y=h - 110))

    def events(self, app, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._go_to_menu(app)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                self._go_to_menu(app)

    def _go_to_menu(self, app):
        from src.MenuState import MenuState

        app.state = MenuState()
        app.state.init(app)

    def update(self, app):
        pass
