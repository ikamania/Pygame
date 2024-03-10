import random
import pygame as pg


class App:
    def __init__(self) -> None:
        self.W, self.H = 400, 600
        self.screen = pg.display.set_mode([self.W, self.H])
        self.info_bar_height = 50

        pg.font.init()

        self.size = 17
        self.font = pg.font.Font("app/static/FiraMono-Bold.ttf", self.size)

    def get_center(self, word: str) -> tuple:
        text_surface = self.font.render(word, True, "WHITE")
        width = text_surface.get_width()

        x, y = (self.W - width) / 2, self.H - self.size * 2

        return x, y

    def draw_word(self, word: str, color: str, position: tuple | list) -> None:
        text_surface = self.font.render(word, True, color)

        pg.draw.rect(self.screen, "WHITE", (position[0], position[1], text_surface.get_width(), self.size))
        self.screen.blit(text_surface, position)

    def draw_line(self, word: str, start: list, end: list) -> None:
        word = self.font.render(word, True, "WHITE")
        width = word.get_width() / 2

        start[0] += width
        end[0] += width
        start[1] -= 5
        end[1] += 25

        pg.draw.line(self.screen, "GREEN", start, end, 2)

    def gen_word(self) -> tuple:
        with open("app/static/words.txt", "r") as file:
            raw_text = file.read()
            file.close()

        text = raw_text.split(" ")
        word = random.choice(text)

        word_surface = self.font.render(word, True, "WHITE")
        width = word_surface.get_width()

        return word, [random.randint(0, 400 - width), -17]

    def game_over(self, word: tuple) -> bool:
        if word[1][1] > self.H - self.size:
            return True

        return False

    def run(self) -> None:
        pg.display.set_caption("Lase Word")

        running = True

        input_text = ""

        words = [("start", [100, -10])]
        target_word = words[0][0]

        word_timer = 0
        gravity_timer = 0

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pg.K_RETURN:
                        if input_text == target_word:
                            words.pop(0)
                            input_text = ""
                            if len(words) > 0:
                                target_word = words[0][0]
                    elif len(input_text) != len(target_word):
                        input_text += event.unicode

            self.screen.fill("WHITE")

            x, y = self.get_center(target_word)

            if input_text == target_word:
                color = "BLACK"
            else:
                color = "RED"

            self.draw_word(target_word, "GRAY", (x, y))
            self.draw_word(input_text, color, (x, y))

            if len(words) > 0:
                self.draw_line(target_word, [x, y], list(words[0][1]))

            if word_timer == 3000:
                words.append(self.gen_word())
                target_word = words[0][0]
                word_timer = 0

            if gravity_timer == 100:
                for word in words:
                    word[1][1] += 1
                    if self.game_over(words[0]):
                        running = False
                gravity_timer = 0

            for word in words:
                self.draw_word(word[0], "BLACK", word[1])

            word_timer += 1
            gravity_timer += 1

            pg.display.flip()

        pg.quit()
