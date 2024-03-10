from game.pieces.piece import Piece


class Bishop(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.name = "BISHOP"
        self.location = f"game/static/{self.color.lower()}/bishop.png"

    def get_moves(self, board: list) -> list:
        x, y = self.position
        moves = self.diagonal_attack(x, y, board)

        return moves
