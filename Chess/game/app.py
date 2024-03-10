import pygame as pg
from game.surface import surface


class App:
    def __init__(self) -> None:
        self.size = 64
        self.W, self.H = self.size * 8, self.size * 8
        self.screen = pg.display.set_mode([self.W, self.H])
        self.board = surface

    def draw_board(self) -> None:
        colors = ["#f0c380", "#6d3e17"]

        for col in range(8):
            for row in range(8):
                color = colors[(col + row) % 2]
                rect = (row * self.size, col * self.size, self.size, self.size)
                pg.draw.rect(self.screen, color, rect)

    def draw_pieces(self) -> None:
        for line in self.board.board:
            for piece in line:
                if piece != 0:
                    x, y = piece.position
                    x, y = x * self.size, y * self.size
                    self.screen.blit(piece.image, (x, y))

    def draw_promotion(self, position: tuple, board: list) -> None:
        x, y = position
        piece = board[y][x]

        a, b = self.W / 2 - self.size, self.H / 2 - self.size
        choices = ["QUEEN", "ROOK", "BISHOP", "KNIGHT"]

        for i, choice in enumerate(choices):
            image = pg.transform.scale(
                pg.image.load(f"game/static/{piece.color.lower()}/{choice.lower()}.png"),
                (self.size, self.size)
            )
            if i == 2:
                b += self.size
                a -= self.size * 2

            pg.draw.rect(self.screen, "LIGHT GREEN", (a + i * self.size, b, self.size, self.size))
            self.screen.blit(image, (a + i * self.size, b))

    def draw_end(self, word: str) -> None:
        pg.font.init()
        font = pg.font.Font("game/static/fonts/FiraMono-Bold.ttf", self.size // 4)

        end_text = font.render(word, True, "GREEN")
        width = end_text.get_width()
        height = end_text.get_height()

        x, y = (self.W - width) / 2, (self.H - height) / 2
        self.screen.blit(end_text, (x, y))

    def load_images(self) -> None:
        for height, line in enumerate(self.board.board):
            for width, piece in enumerate(line):
                if piece != 0:
                    piece.image = pg.transform.scale(
                        pg.image.load(piece.location), (self.size, self.size)
                    )

    def load_positions(self) -> None:
        for height, line in enumerate(self.board.board):
            for width, piece in enumerate(line):
                if piece != 0:
                    piece.position = (width, height)

    def mouse_pos(self) -> int:
        x, y = pg.mouse.get_pos()
        x, y = x // self.size, y // self.size

        return x, y

    def find_king(self, color: str) -> tuple:
        for y, line in enumerate(self.board.board):
            for x, piece in enumerate(line):
                if piece != 0:
                    if piece.name == "KING" and piece.color == color:
                        return x, y

    def run(self) -> None:
        pg.display.set_caption('Chess')

        running = True
        on = True
        promotion = (None, False)
        promotion_squares = [(3, 3), (4, 3), (3, 4), (4, 4)]
        promotion_choices = ["QUEEN", "ROOK", "BISHOP", "KNIGHT"]
        end = 0
        turn = "WHITE"
        winner = None
        selected = ()
        board = self.board.board

        self.load_positions()
        self.load_images()

        while running:
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.MOUSEBUTTONUP:
                    x, y = self.mouse_pos()

                    if promotion[1]:
                        if (x, y) in promotion_squares:
                            piece_changed = promotion_choices[promotion_squares.index((x, y))]
                            self.board.change_piece(promotion[0], piece_changed)
                            self.load_positions()
                            self.load_images()
                            promotion = (None, False)
                    elif event.button == 1 and on:
                        if selected == ():  # select piece if not selected
                            if board[y][x] != 0:
                                if board[y][x].color == turn:
                                    selected = (x, y)
                        else:
                            piece = board[selected[1]][selected[0]]
                            moves = piece.get_moves(board)

                            if [x, y] in moves:
                                old_piece = board[y][x]
                                piece.position = (x, y)
                                self.board.move_piece(selected, (x, y))

                                if piece.name == "KING":
                                    if x - selected[0] == -2:
                                        board[y][x + 1] = board[y][0]
                                        board[y][0] = 0
                                        board[y][x + 1].position = (x + 1, y)
                                    elif x - selected[0] == 2:
                                        board[y][x - 1] = board[y][7]
                                        board[y][7] = 0
                                        board[y][x - 1].position = (x - 1, y)

                                king_position = self.find_king(turn)
                                king = board[king_position[1]][king_position[0]]
                                if king.get_check_status(board):  # passed move
                                    # print("CANT MAKE THIS MOVE")
                                    piece.position = selected
                                    self.board.move_piece((x, y), selected)
                                    board[y][x] = old_piece
                                    if piece.name == "KING":
                                        if x - selected[0] == -2:
                                            board[y][0] = board[y][x + 1]
                                            board[y][x + 1] = 0
                                            board[y][0].position = (0, y)
                                        elif x - selected[0] == 2:
                                            board[y][7] = board[y][x - 1]
                                            board[y][x - 1] = 0
                                            board[y][7].position = (7, y)
                                else:  # made move
                                    if piece.name == "PAWN":
                                        if piece.get_promotion_status():
                                            promotion = ((x, y), True)  # promote here
                                    elif piece.name in ["ROOK", "KING"]:
                                        piece.castle = False

                                    turn = "WHITE" if turn == "BLACK" else "BLACK"

                                    king_position = self.find_king(turn)
                                    king = board[king_position[1]][king_position[0]]

                                    selected = ()
                                    if king.get_checkmate_status(board):
                                        winner = "WHITE" if turn == "BLACK" else "BLACK"
                                        on = False
                            else:
                                new_selected = board[y][x]

                                if new_selected == 0:
                                    selected = ()
                                elif new_selected.color == turn:
                                    selected = (x, y)

                self.draw_board()
                self.draw_pieces()

                if promotion[1]:
                    self.draw_promotion(promotion[0], board)

                if not on:
                    self.draw_end(f"GAME OVER. {winner} WON THE GAME !")
                    end += 1

                    if end > 100:
                        running = False

                pg.display.flip()
                pg.display.update()

        pg.quit()
