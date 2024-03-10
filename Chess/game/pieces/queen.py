from game.pieces.piece import Piece


class Queen(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.name = "QUEEN"
        self.location = f"game/static/{self.color.lower()}/queen.png"

    def get_moves(self, board: list) -> list:
        x, y = self.position
        moves = []

        moves += self.horizontal_attack(x, y, board)
        moves += self.diagonal_attack(x, y, board)

        return moves
