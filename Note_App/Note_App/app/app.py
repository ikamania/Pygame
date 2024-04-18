import pygame as pg
import string
from app.static import *


class App:
    def __init__(self) -> None:
        self.W, self.H = 1200, 600
        self.SCREEN = None

        self.font = None
        self.font_size = None
        self.space_size = None
        self.tab_size = None
        self.letters_per_line = None

        self.path = "app/assets/files/text.txt"
        self.text = list(read_file(self.path))
        self.color = "BLACK"

        self.cursor_position = None
        self.scroll = 0
        self.scroll_draw = 0
        self.position = None
        self.end_point = None

    def draw_letter(self, letter: chr, position: tuple) -> None:
        text_surface = self.font.render(letter, True, self.color)
        self.SCREEN.blit(text_surface, position)
    
    def draw_text(self) -> None:
        x, y = self.font_size, self.font_size

        for i, letter in enumerate(self.text):  # add word splitting or y change
            if x > self.W - self.font_size * 1.5:
                y += self.tab_size
                x = self.font_size
            if y + self.scroll < -self.font_size:
                pass
            elif y + self.scroll > self.H:
                break
            else:
                self.draw_letter(letter, (x, y + self.scroll))

            x += self.space_size

    def draw_cursor(self) -> None:
        x, y = self.cursor_position
        length = self.font_size // 10

        x = round_to_value(x, self.space_size)
        y = round_to_value(y, self.tab_size)

        mouse_rect = (x + length * 3, y + self.font_size - self.tab_size + self.scroll_draw, length, self.font_size)
        pg.draw.rect(self.SCREEN, "RED", mouse_rect)

    def draw_saving_screen(self) -> None:
        text_surface = self.font.render("SAVING...", True, "GREEN")
        self.SCREEN.blit(text_surface, (self.space_size, self.tab_size))

    def draw(self) -> None:
        self.SCREEN.fill("WHITE")
        self.draw_text()
        self.draw_cursor()

    def move_cursor_horizontal(self, value: int) -> None:
        x, y = self.cursor_position

        if value == -1:
            x -= self.space_size

            if x < self.font_size:
                if y - self.tab_size < self.font_size:
                    return
                x = self.W - self.font_size
                y -= self.tab_size
        elif value == 1:
            x += self.space_size

            if self.W - x < self.font_size:
                x = self.font_size
                y += self.tab_size
        self.position += value
        self.cursor_position = x, y

    def move_cursor_vertical(self, value: int) -> None:
        x, y = self.cursor_position

        y += value * self.tab_size
        if y < self.font_size or y > self.end_point[1]:
            return

        self.position += int(value * self.letters_per_line)
        self.cursor_position = x, y

    def calculate_position(self) -> int:
        x, y = self.cursor_position

        w = round_to_value(x - self.font_size, self.space_size) // self.space_size
        h = round_to_value(y + abs(self.scroll), self.tab_size) // self.tab_size - 1

        return int(h * self.letters_per_line + w)

    def calculate_end_point(self) -> tuple:
        total_letters = len(self.text)

        y = (total_letters // self.letters_per_line) * self.tab_size + self.font_size
        x = (total_letters % self.letters_per_line - 1) * self.space_size + self.font_size

        return x, y

    def type(self, letter: chr) -> None:
        self.text.insert(self.position + 1, letter)
        self.move_cursor_horizontal(1)

    def delete(self) -> None:
        self.text.pop(self.position)
        self.move_cursor_horizontal(-1)

    def startup(self, font_size: int):
        self.font_size = font_size
        self.font = pg.font.Font("app/assets/font/FiraMono-Bold.ttf", self.font_size)
        self.space_size = self.font_size // 1.5
        self.tab_size = self.font_size * 1.5
        self.letters_per_line = int((self.W - self.font_size * 2) // self.space_size + 1)
        self.end_point = self.calculate_end_point()
        self.cursor_position = self.end_point
        self.position = self.calculate_position()

    def run(self) -> None:
        self.SCREEN = pg.display.set_mode([self.W, self.H])

        pg.display.set_caption("NOTE APP")
        pg.init()

        running = True
        letters = string.ascii_lowercase + string.punctuation + string.digits + " "

        self.startup(25)
        self.SCREEN.fill("WHITE")
        self.draw()
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.move_cursor_vertical(-1)
                        self.draw()
                    elif event.key == pg.K_DOWN:
                        self.move_cursor_vertical(1)
                        self.draw()
                    elif event.key == pg.K_RIGHT:
                        self.move_cursor_horizontal(1)
                        self.draw()
                    elif event.key == pg.K_LEFT:
                        self.move_cursor_horizontal(-1)
                        self.draw()
                    elif event.key == pg.K_F11:
                        self.draw_saving_screen()
                        text = "".join(self.text)
                        if save_file(self.path, text):
                            running = False
                    elif event.unicode.lower() in letters:
                        self.type(event.unicode)
                        self.draw()
                    elif event.key == pg.K_BACKSPACE:
                        self.delete()
                        self.draw()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pg.mouse.get_pos()
                        val = self.space_size * 2
                        if y > 0 and 0 + val < x < self.W - val:
                            self.cursor_position = x, y
                            self.scroll_draw = 0
                            self.position = self.calculate_position()
                            self.draw()
                    if event.button == 4:  # UP SCROLL
                        if self.scroll < 0:
                            self.scroll += self.tab_size
                            self.scroll_draw += self.tab_size
                            self.draw()
                    if event.button == 5:  # DOWN SCROLL
                        self.scroll -= self.tab_size
                        self.scroll_draw -= self.tab_size
                        self.draw()

            pg.display.flip()
            pg.display.update()

        pg.quit()
