import pygame

from src.StateAbstract import StateAbstract
from src.GameState import GameState
from src.ScoreState import ScoreState


class MenuState(StateAbstract):
    def __init__(self):
        super().__init__()
        self.font = None
        self.bg_color = (51, 51, 51)
        self.button_color = (160, 160, 160)
        self.button_width = 250
        self.button_height = 60
        self.spacing = 20
        self.play_button = None
        self.scores_button = None
        self.quit_button = None

    def _layout_buttons(self, app):
        center_x = app.screen.get_width() // 2 - self.button_width // 2
        start_y = 150
        self.play_button = pygame.Rect(center_x, start_y, self.button_width, self.button_height)
        self.scores_button = pygame.Rect(
            center_x,
            start_y + (self.button_height + self.spacing),
            self.button_width,
            self.button_height,
        )
        self.quit_button = pygame.Rect(
            center_x,
            start_y + 2 * (self.button_height + self.spacing),
            self.button_width,
            self.button_height,
        )

    def init(self, app):
        self.setup = False
        self.font = pygame.font.Font(None, 50)
        self._layout_buttons(app)

    def draw(self, app):
        app.screen.fill(self.bg_color)

        pygame.draw.rect(app.screen, self.button_color, self.play_button)
        pygame.draw.rect(app.screen, self.button_color, self.scores_button)
        pygame.draw.rect(app.screen, self.button_color, self.quit_button)

        def draw_text(text, rect):
            surface = self.font.render(text, True, (0, 0, 0))
            rect_text = surface.get_rect(center=rect.center)
            app.screen.blit(surface, rect_text)

        draw_text("PLAY", self.play_button)
        draw_text("BEST SCORES", self.scores_button)
        draw_text("QUIT", self.quit_button)

    def events(self, app, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(event.pos):
                app.state = GameState(app.board_rows, app.board_cols, app.board_mines)
                app.state.init(app)
            elif self.scores_button.collidepoint(event.pos):
                app.state = ScoreState()
                app.state.init(app)
            elif self.quit_button.collidepoint(event.pos):
                app.running = False

    def update(self, app):
        pass
