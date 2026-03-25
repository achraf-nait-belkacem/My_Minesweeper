from src.GameLogic.Board import Board



class GameManager:
    def __init__(self, board):
        self.board = board           
        self.game_over = False        
        self.win = False   

    def reveal(self, r, c):
        cell = self.board.grid[r][c]

        self.board.reveal_cell(r,c)

        if cell.is_mine == True:
            self.game_over = True

        self.check_win()

    def check_win(self):
        for rows in self.board.grid:
            for cell in rows:
                if not cell.is_mine and not cell.is_revealed:
                    return
                
        self.win = True

    def reset(self):
        
        self.board = Board(self.board.rows,self.board.cols, self.board.mines)
        self.game_over = False
        self.win = False