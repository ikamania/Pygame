class Piece:
    def __init__(self, color: str) -> None:
        self.color = color
        self.position = ()
        self.direction = -1 if color == "WHITE" else 1
        self.opponent = "BLACK" if color == "WHITE" else "WHITE"

    def add_square(self, x: int, y: int, board: list) -> tuple:  # true if no more moves
        moves = []

        if x < 0 or y < 0 or x > 7 or y > 7:
            return moves, True
        else:
            piece = board[y][x]

        if piece == 0:
            moves.append([x, y])
            return moves, False
        elif piece.color == self.opponent:
            moves.append([x, y])

        return moves, True

    def pawn_attack(self, x: int, y: int, board: list) -> list:
        moves = []

        attack_squares = [[x - 1, y + (1 * self.direction)],
                          [x + 1, y + (1 * self.direction)]]

        for sqr in attack_squares:
            x, y = sqr[0], sqr[1]

            if x in [-1, 8]:
                continue

            piece = board[y][x]
            if piece != 0 and piece.color == self.opponent:
                moves.append(sqr)

        return moves

    def horizontal_attack(self, x: int, y: int, board: list) -> list:
        final_moves = []

        for i in range(x - 1, 0 - 1, -1):
            moves, stop = self.add_square(i, y, board)
            final_moves += moves
            if stop:
                break

        for i in range(x + 1, 8):
            moves, stop = self.add_square(i, y, board)
            final_moves += moves
            if stop:
                break

        for i in range(y - 1, 0 - 1, -1):
            moves, stop = self.add_square(x, i, board)
            final_moves += moves
            if stop:
                break

        for i in range(y + 1, 8):
            moves, stop = self.add_square(x, i, board)
            final_moves += moves
            if stop:
                break

        return final_moves

    def diagonal_attack(self, x: int, y: int, board: list) -> list:
        final_moves = []

        for i in range(x - 1, 0 - 1, -1):
            a, b = i, y - (x - i)

            moves, stop = self.add_square(a, b, board)
            final_moves += moves
            if stop:
                break

        for i in range(x + 1, 8):
            a, b = i, y - (x - i)

            moves, stop = self.add_square(a, b, board)
            final_moves += moves
            if stop:
                break

        for i in range(x - 1, 0 - 1, -1):
            a, b = i, y + (x - i)

            moves, stop = self.add_square(a, b, board)
            final_moves += moves
            if stop:
                break

        for i in range(x + 1, 8):
            a, b = i, y + (x - i)

            moves, stop = self.add_square(a, b, board)
            final_moves += moves
            if stop:
                break

        return final_moves

    def knight_attack(self, x: int, y: int, board: list) -> list:
        final_moves = []

        possible_moves = [
            (x + 1, y - 2), (x - 1, y - 2),
            (x + 2, y - 1), (x - 2, y - 1),
            (x - 2, y + 1), (x + 2, y + 1),
            (x - 1, y + 2), (x + 1, y + 2),
        ]

        for move in possible_moves:
            moves, stop = self.add_square(move[0], move[1], board)
            final_moves += moves

        return final_moves
