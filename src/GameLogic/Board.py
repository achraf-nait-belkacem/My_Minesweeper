import random
from src.GameLogic.cell import Cell

class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.initialized = False
    
    def get_grid(self):
        return self.grid

    def fill_board(self, safe_x, safe_y):
        self.place_mines(safe_x, safe_y)
        self.calculate_numbers()
        self.initialized = True
    
    def get_neighbors(self, r, c):
        neighbors = []
        for i in range(r - 1, r + 2):
            for j in range(c - 1, c + 2):
                if 0 <= i < self.rows and 0 <= j < self.cols:
                    if not (i == r and j == c):
                        neighbors.append((i, j))
        return neighbors

    def place_mines(self, safe_r, safe_c):
        placed = 0
        while placed < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)

            if (r == safe_r and c == safe_c):
                continue

            if not self.grid[r][c].is_mine:
                self.grid[r][c].is_mine = True
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
            self.initialize_board(r, c)

        cell = self.grid[r][c]
        if cell.is_revealed or cell.is_flagged:
            return

        cell.is_revealed = True

        
        if cell.neighbor_mines == 0 and not cell.is_mine:
            for nr, nc in self.get_neighbors(r, c):
                self.reveal_cell(nr, nc)