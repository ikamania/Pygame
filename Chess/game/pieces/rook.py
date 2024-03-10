from game.pieces.piece import Piece


class Rook(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.name = "ROOK"
        self.location = f"game/static/{self.color.lower()}/rook.png"
        self.castle = True

    def get_moves(self, board: list) -> list:
        x, y = self.position
        moves = self.horizontal_attack(x, y, board)

        return moves
