import json

import pygame

from src.GameLogic.Board import Board
from src.StateAbstract import StateAbstract
from src.constants import CELL_SIZE, MARGIN, SCORES_FILE


class GameState(StateAbstract):
    def __init__(self, board):
        super().__init__()
        self.board = board
        self.font = None
        self.big_font = None
        self._start_time = 0
        self._game_over_screen = False
        self._overlay_title = ""
        self._overlay_sub = None

    def init(self, app):
        self.setup = False
        self._game_over_screen = False
        self._overlay_sub = None
        self._start_time = pygame.time.get_ticks()
        self.font = pygame.font.SysFont(None, 24)
        self.big_font = pygame.font.SysFont(None, 44)

    def draw(self, app):
        app.screen.fill((50, 50, 50))

        for r, row in enumerate(self.board.grid):
            for c, cell in enumerate(row):
                x = c * (CELL_SIZE + MARGIN)
                y = r * (CELL_SIZE + MARGIN)
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

                if cell.is_revealed:
                    if cell.is_mine:
                        pygame.draw.rect(app.screen, (255, 0, 0), rect)
                    else:
                        pygame.draw.rect(app.screen, (200, 200, 200), rect)
                        if cell.neighbor_mines > 0:
                            text = self.font.render(str(cell.neighbor_mines), True, (0, 0, 0))
                            app.screen.blit(text, (x + CELL_SIZE // 3, y + CELL_SIZE // 4))
                else:
                    pygame.draw.rect(app.screen, (100, 100, 100), rect)
                    if cell.is_flagged:
                        pygame.draw.circle(app.screen, (255, 255, 0), rect.center, CELL_SIZE // 4)

        if self._game_over_screen:
            w, h = app.screen.get_size()
            dim = pygame.Surface((w, h), pygame.SRCALPHA)
            dim.fill((0, 0, 0, 175))
            app.screen.blit(dim, (0, 0))

            title_surf = self.big_font.render(self._overlay_title, True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(w // 2, h // 2 - 40))
            app.screen.blit(title_surf, title_rect)

            if self._overlay_sub:
                sub_surf = self.font.render(self._overlay_sub, True, (180, 255, 180))
                sub_rect = sub_surf.get_rect(center=(w // 2, h // 2 + 10))
                app.screen.blit(sub_surf, sub_rect)

            hint = self.font.render("Click or press any key to return to menu", True, (255, 255, 120))
            hint_rect = hint.get_rect(center=(w // 2, h // 2 + 90))
            app.screen.blit(hint, hint_rect)

    def events(self, app, event):
        if self._game_over_screen:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self._go_to_menu(app)
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            col = mx // (CELL_SIZE + MARGIN)
            row = my // (CELL_SIZE + MARGIN)

            if row >= len(self.board.grid) or col >= len(self.board.grid[0]):
                return

            cell = self.board.grid[row][col]

            if event.button == 1:
                self.board.reveal_cell(row, col)
            elif event.button == 3:
                cell.toggle_flag()

    def update(self, app):
        if self._game_over_screen:
            return

        for row in self.board.grid:
            for cell in row:
                if cell.is_mine and cell.is_revealed:
                    self._overlay_title = "Game Over!"
                    self._overlay_sub = None
                    self._game_over_screen = True
                    print("Game Over!")
                    return

        won = all(cell.is_revealed or cell.is_mine for row in self.board.grid for cell in row)
        if won:
            seconds = (pygame.time.get_ticks() - self._start_time) / 1000.0
            seconds = round(seconds, 2)
            print("You Win!", seconds, "seconds")
            self._save_score_if_best(seconds)
            self._overlay_title = "You Win!"
            self._overlay_sub = f"Time: {seconds} s"
            self._game_over_screen = True

    def _save_score_if_best(self, seconds):
        best = None
        try:
            with open(SCORES_FILE, "r") as f:
                data = json.load(f)
            if isinstance(data, dict) and "best" in data:
                best = data["best"]
            elif isinstance(data, list) and data:
                best = min(data)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        if best is None or seconds < best:
            with open(SCORES_FILE, "w") as f:
                json.dump({"best": round(seconds, 2)}, f, indent=2)

    def _go_to_menu(self, app):
        from src.MenuState import MenuState

        app.board = Board(self.board.rows, self.board.cols, self.board.mines)
        app.state = MenuState()
        app.state.init(app)
