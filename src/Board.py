class Board:
    def __init__(self, y, x):
        self.board = None
        self.height = y
        self.width = x
    
    def fill_board(self):
        for y in range(self.height):
            for x in range(self.width):
                self.board[y][x] = "."
    
    def click_target(self, y, x):
        pass
