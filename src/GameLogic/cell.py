class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0

    def reveal(self):
        if self.is_flagged or self.is_revealed:
            return "ignored"

        self.is_revealed = True

        if self.is_mine:
            return "mine"
        if self.neighbor_mines == 0:
            return "empty"
        return "number"

    def toggle_flag(self):
        if self.is_revealed:
            return False
        self.is_flagged = not self.is_flagged
        return self.is_flagged
