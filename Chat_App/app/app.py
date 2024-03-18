import pygame as pg
import threading
from client import Client


class App:
    def __init__(self) -> None:
        self.client = Client()

        self.W, self.H = 400, 600
        self.screen = pg.display.set_mode([self.W, self.H])
        self.info_bar_height = 50

        pg.font.init()
        pg.display.set_caption("Chat App")

        self.size = 17
        self.font = pg.font.Font("static/FiraMono-Bold.ttf", self.size)
        self.y = self.info_bar_height + self.size

        self.input_box = pg.Rect(0, self.H - 32, self.W, 32)
        self.input_text = ""
        self.last_message = None

    def display_info_bar(self) -> None:
        pg.draw.line(self.screen, "RED", (0, self.info_bar_height), (self.W, self.info_bar_height))

    def display_input_box(self, color: str) -> None:
        pg.draw.rect(self.screen, color, self.input_box)
        text_surface = self.font.render(self.input_text, True, "WHITE")

        self.screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))

    def display_messages(self) -> None:
        while True:
            message = self.client.receive_from_server()

            if message == self.last_message:
                self.last_message = None
                x = self.W - len(message) * 10 - 10 * 2
            else:
                x = 10

            data_surface = self.font.render(message, True, "WHITE")
            message_box = pg.Rect(x, self.y, len(message) * 10 + 10, 28)

            pg.draw.rect(self.screen, "GRAY", message_box)
            self.screen.blit(data_surface, (message_box.x + 5, message_box.y + 4))
            self.y += 28 + 5

    def run(self) -> None:
        running = True
        input_active = False

        self.client.connect()

        thread = threading.Thread(target=self.display_messages)
        thread.daemon = True
        thread.start()

        self.screen.fill("WHITE")
        while self.client and running:
            color = "LIGHT GRAY" if input_active else "GRAY"

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        input_active = True
                    else:
                        input_active = False

                if event.type == pg.KEYDOWN:
                    if input_active:
                        if event.key == pg.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        elif event.key == pg.K_RETURN:
                            self.client.send_to_server(self.input_text)
                            self.last_message = self.input_text
                            self.input_text = ""
                        else:
                            self.input_text += event.unicode

            pg.display.flip()

            self.display_info_bar()
            self.display_input_box(color)

        self.client.disconnect()
        pg.quit()


if __name__ == "__main__":
    app = App()
    app.run()