from game.pieces.piece import Piece


class Knight(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.name = "KNIGHT"
        self.location = f"game/static/{self.color.lower()}/knight.png"

    def get_moves(self, board: list) -> list:
        x, y = self.position

        return self.knight_attack(x, y, board)
