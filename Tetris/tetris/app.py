import pygame as pg
from tetris.piece import Piece

class App:
    def __init__(self) -> None:
        self.square = 40

        self.board = [[0] * 10 for _ in range(18)]
        self.screen = pg.display.set_mode([10 * self.square, 18 * self.square])


    def display_board(self) -> None:
        sqr = self.square

        for y, line in enumerate(self.board):
            for x, piece in enumerate(line):
                if piece != 0:
                    pg.draw.rect(self.screen, piece, (x * sqr, y * sqr, sqr, sqr))

    def check_board(self, piece: type(Piece), pos: list) -> bool:
        if x + piece.x > 9 or x + piece.x < 0:
            return False

        if self.board[y + piece.y][x + piece.x] != 0:
            return False


    def display_piece(self, piece: type(Piece)) -> None:
        sqr = self.square

        for y, line in enumerate(piece.shape):
            for x, square in enumerate(line):
                if square == 1:
                    cell, row = x * sqr + piece.x * sqr, y * sqr + piece.y * sqr
                    
                    if x + piece.x > 9 or x + piece.x < 0 or self.board[y + piece.y][x + piece.x] != 0:
                        piece.rotate()
                        self.display_piece(piece)
                    else:
                        pg.draw.rect(self.screen, piece.color, (cell, row, sqr, sqr))

    def add_piece(self, piece: type(Piece)) -> None:
        for y, line in enumerate(piece.shape):
            for x, square in enumerate(line):
                if square == 1:
                    self.board[piece.y + y - 1][piece.x + x] = piece.color

    def check_y(self) -> int:
        for y, line in enumerate(self.board):
            num = 0
            for square in line:
                if square != 0:
                    num += 1
                
                if num == 10:
                    return y
        return -1

    def gravity(self) -> None:
        y = self.check_y()

        if y != -1:
            for j in range(y):
                self.board[y - j] = self.board[y - j - 1]

    def end(self) -> bool:
        if any(self.board[0]) != 0:
            return True
        return False

    def run(self) -> None:
        pg.display.set_caption("Tetris")

        running = True
        spawned = False
        delay = 0

        piece = Piece()

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        if piece.check_x(self.board, -1):
                            piece.x -= 1
                    
                    if event.key == pg.K_RIGHT:
                        if piece.check_x(self.board, 1):
                            piece.x += 1

                    if event.key == pg.K_a:
                        piece.rotate()


            self.screen.fill("black")
            self.display_board()
            
            if spawned:
                self.display_piece(piece)

                if delay > 250:
                    piece.y += 1
                    delay = 0

                    if not piece.check_y(self.board):
                        self.add_piece(piece)
                        spawned = False
            else:
                if self.end():
                    running = False
                self.gravity()
                piece = Piece()
                spawned = True
            
            delay += 1
            pg.display.flip()
        pg.quit()