import random
from tetris.pieces import pieces

class Piece:
    grid = None
    
    def __init__(self) -> None:
        self.x, self.y = 4, 0
        self.shape = random.choice(pieces)
        self.color = random.choice(["CYAN", "YELLOW", "PURPLE", "GREEN", "BLUE", "RED", "ORANGE"])

    def check_y(self, board: list) -> bool:
        for i, line in enumerate(self.shape):
            for x in range(len(line)):
                if line[x] == 1:
                    y = self.y + i

                    if y > 17:
                        return False

                    if board[y][self.x + x] != 0:
                        return False
        return True
            
    def check_x(self, board: list, value: int) -> bool:
        for y, line in enumerate(self.shape):
            for x in range(len(line)):
                if line[x] == 1:
                    if self.x + x + value > 9 or self.x + x + value < 0:
                        return False
                    elif board[self.y + y][self.x + x + value] != 0:
                        return False
        return True

    def rotate(self) -> None:
        width = len(self.shape[0])
        new_grid = [[] for _ in range(width)]

        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                new_grid[width - 1 - x].append(cell)

        self.shape = new_grid