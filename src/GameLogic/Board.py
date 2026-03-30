import random
from src.GameLogic.Cell import Cell

class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.initialized = False

    def get_grid(self):
        return self.grid

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def get_neighbors(self, r, c):
        neighbors = []
        for i in range(r - 1, r + 2):
            for j in range(c - 1, c + 2):
                if self.in_bounds(i, j) and not (i == r and j == c):
                    neighbors.append((i, j))
        return neighbors

    def fill_board(self, safe_r, safe_c):
        self.place_mines(safe_r, safe_c)
        self.calculate_numbers()
        self.initialized = True

    def place_mines(self, safe_r, safe_c):
        placed = 0
        safe_zone = self.get_neighbors(safe_r, safe_c)
        safe_zone.append((safe_r, safe_c))

        while placed < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)

            if (r, c) in safe_zone:
                continue

            cell = self.grid[r][c]
            if not cell.is_mine:
                cell.is_mine = True
                placed += 1

    def calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.is_mine:
                    continue
                count = 0
                for nr, nc in self.get_neighbors(r, c):
                    if self.grid[nr][nc].is_mine:
                        count += 1
                cell.neighbor_mines = count

    def reveal_cell(self, r, c):
        if not self.initialized:
            self.fill_board(r, c)

        cell = self.grid[r][c]
        result = cell.reveal()

        if result == "ignored":
            return "ignored"

        if result == "mine":
            self.reveal_all_mines()
            return "mine"

        # empty cell: open neighbors (recursive flood fill)
        if result == "empty":
            for nr, nc in self.get_neighbors(r, c):
                self.reveal_cell(nr, nc)

        return result

    def reveal_all_mines(self):
        for row in self.grid:
            for cell in row:
                if cell.is_mine:
                    cell.is_revealed = True

    def check_win(self):
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True