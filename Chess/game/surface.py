from game.pieces.pawn import Pawn
from game.pieces.king import King
from game.pieces.rook import Rook
from game.pieces.bishop import Bishop
from game.pieces.knight import Knight
from game.pieces.queen import Queen


class Surface:
    def __init__(self) -> None:
        w, b = "WHITE", "BLACK"

        self.board = [[Rook(b), Knight(b), Bishop(b), Queen(b), King(b), Bishop(b), Knight(b), Rook(b)],
                      [Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b)],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w)],
                      [Rook(w), Knight(w), Bishop(w), Queen(w), King(w), Bishop(w), Knight(w), Rook(w)]]

    def move_piece(self, start: tuple, end: tuple) -> None:
        x, y = start
        a, b = end

        self.board[b][a] = self.board[y][x]
        self.board[y][x] = 0

    def change_piece(self, position: tuple, piece: str) -> None:
        x, y = position
        color = self.board[y][x].color

        if piece == "QUEEN":
            piece_object = Queen(color)
        elif piece == "ROOK":
            piece_object = Rook(color)
        elif piece == "BISHOP":
            piece_object = Bishop(color)
        elif piece == "KNIGHT":
            piece_object = Knight(color)
        else:
            piece_object = Pawn(color)

        self.board[y][x] = piece_object


surface = Surface()
