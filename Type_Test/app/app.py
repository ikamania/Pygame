import pygame as pg
import time
import random
from app import colors


def get_text() -> str:
    with open("app/assets/words.txt", "r") as file:
        raw_text = file.read()
        file.close()

    text = raw_text.split(" ")
    random.shuffle(text)

    return " ".join(text)


def get_pec(in_text, out_text):
    correct = 0
    for i, s in enumerate(in_text):
        if s == out_text[i]:
            correct += 1

    percentage = round(correct / len(in_text) * 100)

    return percentage


def get_wpm(x_text, x_time):
    x_time = x_time / 60
    wpm = round((len(x_text) / 5) / x_time)

    return wpm


class App:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 900, 400
        self.screen = pg.display.set_mode([self.WIDTH, self.HEIGHT])

        pg.display.set_caption('TYPE TEST')
        pg.init()

        self.f_size_default = 50
        self.f_size_stat = 64
        self.font_default = pg.font.Font("app/assets/fonts/FiraMono-Bold.ttf", self.f_size_default)
        self.font_stat = pg.font.Font("app/assets/fonts/FiraMono-Bold.ttf", self.f_size_stat)

        self.letters = "abcdefghijklmnopqrstuvwxyz,.!?'"

    def draw_letter(self, x_letter, x_color, x_font, xy_list):
        text_surface = x_font.render(x_letter, True, x_color)
        self.screen.blit(text_surface, (xy_list[0], xy_list[1]))

    def draw_time(self, x_time, x_font, window):
        text_surface = x_font.render(x_time, True, colors.STATS)
        self.screen.blit(text_surface, (window[0] - 100, 20))

    def draw_result(self, x_wpm, x_percentage, x_font):
        wpm_surface = x_font.render(str(x_wpm) + "wpm", True, colors.STATS)
        percentage_surface = x_font.render(str(x_percentage) + "%", True, colors.STATS)

        self.screen.blit(wpm_surface, (20, 20))
        self.screen.blit(percentage_surface, (300, 20))

    def run(self):
        start = False
        running = True
        on = True

        view = 0
        view_start = False

        user_text = ""
        text = get_text()

        start_time = None

        while running:
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    if event.unicode.lower() in list(self.letters) or event.key == pg.K_SPACE:
                        user_text += event.unicode
                        if view_start:
                            view -= 28
                    elif event.key == pg.K_BACKSPACE:
                        user_text = user_text[:-1]
                        if view_start and view < 0:
                            view += 28

            if len(user_text) > 0 and not start:
                start = True
                start_time = time.time() - 0.3

            if on:
                x = 28
                y = self.HEIGHT / 2 - self.f_size_default

                self.screen.fill(colors.BACKGROUND)

                for s in text:
                    self.draw_letter(s, colors.DEFAULT, self.font_default, [x + view, y])

                    x += 28
                x = 28

                for i, s in enumerate(user_text):
                    if s != text[i]:
                        pg.draw.rect(self.screen, colors.BACKGROUND, (x + view, y, 28, 50))
                        self.draw_letter(text[i], colors.WRONG, self.font_default, [x + view, y])
                    else:
                        self.draw_letter(s, colors.RIGHT, self.font_default, [x + view, y])

                    x += 28
                    if x > 200:
                        view_start = True

                if start:
                    loop_time = int(time.time() - start_time)

                    if (time.time() - start_time) > 30:
                        wpm, percentage = get_wpm(user_text, loop_time), get_pec(user_text, text)

                        self.draw_result(wpm, percentage, self.font_stat)
                        on = False
                    else:
                        self.draw_time(str(30 - round(loop_time)), self.font_stat, [self.WIDTH, self.HEIGHT])
                else:
                    self.draw_time("30", self.font_stat, [self.WIDTH, self.HEIGHT])

            pg.display.flip()
            pg.display.update()

        pg.quit()
