from game.pieces.piece import Piece


class King(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.name = "KING"
        self.location = f"game/static/{self.color.lower()}/king.png"
        self.castle = True

    def get_moves(self, board: list) -> list:
        x, y = self.position
        final_moves = []

        king_moves = [[x, y + 1], [x,  y - 1], [x + 1, y], [x - 1, y],
                      [x + 1, y + 1], [x + 1, y - 1], [x - 1, y + 1], [x - 1, y - 1]]

        for move in king_moves:
            moves, stop = self.add_square(move[0], move[1], board)
            final_moves += moves

        final_moves += self.get_castle_moves(board)

        return final_moves

    def get_castle_moves(self, board: list) -> list:
        if not self.castle:
            return []

        x, y = self.position
        final_moves = []

        for i in range(1, 5):
            left_rook = board[y][x - i]

            if i == 4 and left_rook != 0 and left_rook.name == "ROOK" and left_rook.castle:
                final_moves.append([x - 2, y])
            elif left_rook != 0:
                break

        for i in range(1, 4):
            right_rook = board[y][x + i]

            if i == 3 and right_rook != 0 and right_rook.name == "ROOK" and right_rook.castle:
                final_moves.append([x + 2, y])
            elif right_rook != 0:
                break

        return final_moves

    def get_check_status(self, board) -> bool:  # true if it's going to die
        x, y = self.position

        bishop_moves = self.diagonal_attack(x, y, board)
        rook_moves = self.horizontal_attack(x, y, board)
        knight_moves = self.knight_attack(x, y, board)
        pawn_moves = self.pawn_attack(x, y, board)

        for move in bishop_moves:
            x, y = move
            piece = board[y][x]

            if piece != 0:
                if piece.name in ["BISHOP", "QUEEN"] and piece.color == self.opponent:
                    return True

        for move in rook_moves:
            x, y = move
            piece = board[y][x]

            if piece != 0:
                if piece.name in ["ROOK", "QUEEN"] and piece.color == self.opponent:
                    return True

        for move in knight_moves:
            x, y = move
            piece = board[y][x]

            if piece != 0:
                if piece.name == "KNIGHT" and piece.color == self.opponent:
                    return True

        for move in pawn_moves:
            x, y = move
            piece = board[y][x]

            if piece != 0:
                if piece.name == "PAWN" and piece.color == self.opponent:
                    return True
        return False

    def get_checkmate_status(self, board: list) -> bool:  # True if checkmate
        for y, line in enumerate(board):
            for x, piece in enumerate(line):
                if piece != 0 and piece.color == self.color:
                    moves = piece.get_moves(board)

                    for move in moves:
                        a, b = move

                        square = board[b][a]
                        board[b][a] = piece
                        piece.position = (a, b)
                        board[y][x] = 0

                        answer = self.get_check_status(board)

                        board[y][x] = piece
                        piece.position = (x, y)
                        board[b][a] = square

                        if not answer:
                            return False
        return True
