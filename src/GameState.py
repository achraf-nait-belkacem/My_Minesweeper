import pygame

class GameState:
    def __init__(self):
        self.setup = True

    @staticmethod
    def _print_board(board):
        for i in range(len(board.grid)):
            for j in range(len(board.grid[i])):
                if board.grid[i][j].is_mine:
                    print("💣", end="")
                elif board.grid[i][j].is_revealed:
                    print("👀", end="")
                elif board.grid[i][j].is_flagged:
                    print("⛳️", end="")
                else:
                    print("🙈", end="")

            print("")


    def init(self, app):
        self.setup = False
        print("Setup called.")
        self._print_board(app.board)

    def draw(self, app):
        app.screen.fill("gray")

    def events(self, app, event):
        pass

    def update(self, app):
        pass