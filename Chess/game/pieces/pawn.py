from game.pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.name = "PAWN"
        self.location = f"game/static/{self.color.lower()}/pawn.png"

    def get_promotion_status(self) -> bool:
        x, y = self.position

        if (y == 7 and self.direction == 1) or (y == 0 and self.direction == -1):
            return True
        return False

    def get_moves(self, board: list) -> list:
        x, y = self.position
        moves = []

        move = [x, y + (1 * self.direction)]

        if self.get_promotion_status():
            return []

        if board[move[1]][move[0]] == 0:
            moves.append(move)

        if (y == 6 and self.direction == -1) or (y == 1 and self.direction == 1):
            move = [x, y + (2 * self.direction)]

            if board[move[1]][move[0]] == 0:
                moves.append(move)

        moves += self.pawn_attack(x, y, board)

        return moves
