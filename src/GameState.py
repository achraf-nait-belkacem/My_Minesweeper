import pygame

from src.GameLogic.Board import Board
from src.StateAbstract import StateAbstract
from src.constants import CELL_SIZE, MARGIN, LEFT_PANEL, RIGHT_PANEL
from src.ScoreState import ScoreState

class GameState(StateAbstract):
    def __init__(self, rows, cols, mines):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = Board(rows, cols, mines)
        self.font = None
        self.big_font = None
        self.ui_font = None
        self._start_time = 0
        self._final_time = None
        self._game_over_screen = False
        self._overlay_title = ""
        self._overlay_sub = None
        self.board_x = 0
        self.board_y = 0
        self.back_button = None
        self.reset_button = None

    def _compute_layout(self, app):
        w, h = app.screen.get_size()
        board_pixel_w = self.cols * (CELL_SIZE + MARGIN) - MARGIN
        board_pixel_h = self.rows * (CELL_SIZE + MARGIN) - MARGIN
        available_w = w - LEFT_PANEL - RIGHT_PANEL
        self.board_x = LEFT_PANEL + max(0, (available_w - board_pixel_w) // 2)
        self.board_y = max(0, (h - board_pixel_h) // 2)

        btn_w, btn_h = 120, 40
        btn_x = (LEFT_PANEL - btn_w) // 2
        self.back_button = pygame.Rect(btn_x, 20, btn_w, btn_h)
        self.reset_button = pygame.Rect(btn_x, 70, btn_w, btn_h)

    def init(self, app):
        self.setup = False
        self._game_over_screen = False
        self._overlay_sub = None
        self._final_time = None
        self._start_time = pygame.time.get_ticks()
        self.font = pygame.font.SysFont(None, 24)
        self.big_font = pygame.font.SysFont(None, 44)
        self.ui_font = pygame.font.SysFont(None, 30)
        self._compute_layout(app)

    def draw(self, app):
        app.screen.fill((50, 50, 50))
        self._draw_board(app)
        self._draw_buttons(app)
        self._draw_stats(app)
        if self._game_over_screen:
            self._draw_overlay(app)

    def _draw_board(self, app):
        for r, row in enumerate(self.board.grid):
            for c, cell in enumerate(row):
                x = self.board_x + c * (CELL_SIZE + MARGIN)
                y = self.board_y + r * (CELL_SIZE + MARGIN)
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

    def _draw_buttons(self, app):
        pygame.draw.rect(app.screen, (160, 160, 160), self.back_button)
        back_text = self.ui_font.render("BACK", True, (0, 0, 0))
        app.screen.blit(back_text, back_text.get_rect(center=self.back_button.center))

        pygame.draw.rect(app.screen, (160, 160, 160), self.reset_button)
        reset_text = self.ui_font.render("RESET", True, (0, 0, 0))
        app.screen.blit(reset_text, reset_text.get_rect(center=self.reset_button.center))

    def _draw_stats(self, app):
        w, h = app.screen.get_size()
        rx = w - RIGHT_PANEL + 15
        ry = h // 2 - 60

        if self._final_time is not None:
            elapsed = self._final_time
        else:
            elapsed = round((pygame.time.get_ticks() - self._start_time) / 1000.0, 1)

        flags_placed = sum(cell.is_flagged for row in self.board.grid for cell in row)
        mines_left = self.board.mines - flags_placed

        time_label = self.ui_font.render("Time", True, (200, 200, 200))
        time_value = self.ui_font.render(f"{elapsed} s", True, (255, 255, 255))
        mines_label = self.ui_font.render("Mines", True, (200, 200, 200))
        mines_value = self.ui_font.render(str(mines_left), True, (255, 100, 100))

        app.screen.blit(time_label, (rx, ry))
        app.screen.blit(time_value, (rx, ry + 28))
        app.screen.blit(mines_label, (rx, ry + 70))
        app.screen.blit(mines_value, (rx, ry + 98))

    def _draw_overlay(self, app):
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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._go_to_menu(app)
            return

        if self._game_over_screen:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self._go_to_menu(app)
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._go_to_menu(app)
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                self._go_to_menu(app)
                return
            if self.reset_button.collidepoint(event.pos):
                self._reset(app)
                return

            mx, my = event.pos
            col = (mx - self.board_x) // (CELL_SIZE + MARGIN)
            row = (my - self.board_y) // (CELL_SIZE + MARGIN)

            if row < 0 or col < 0 or row >= len(self.board.grid) or col >= len(self.board.grid[0]):
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
                    self._final_time = round((pygame.time.get_ticks() - self._start_time) / 1000.0, 2)
                    self._overlay_title = "Game Over!"
                    self._overlay_sub = None
                    self._game_over_screen = True
                    return

        if self.board.check_win():
            seconds = round((pygame.time.get_ticks() - self._start_time) / 1000.0, 2)
            self._final_time = seconds
            ScoreState.save_score(seconds)
            self._overlay_title = "You Win!"
            self._overlay_sub = f"Time: {seconds} s"
            self._game_over_screen = True

    def _reset(self, app):
        self.board = Board(self.rows, self.cols, self.mines)
        self._game_over_screen = False
        self._overlay_sub = None
        self._final_time = None
        self._start_time = pygame.time.get_ticks()

    def _go_to_menu(self, app):
        from src.MenuState import MenuState

        app.state = MenuState()
        app.state.init(app)
