import pygame as pg
import random
from flappy.bird import Bird


class App:
    def __init__(self) -> None:
        self.W, self.H = 350, 480

        self.SCREEN = None
        self.bird = Bird()
        self.score = 0

        self.background = None
        self.pipe = None
        self.pipes = []

    def load_animations(self) -> None:
        for i in range(1, 4):
            self.bird.animations.append(pg.image.load(f"flappy/sprites/redbird-{i}.png"))

        self.background = pg.transform.scale(pg.image.load(f"flappy/sprites/background-day.png"), (self.W, self.H))
        self.pipe = pg.image.load(f"flappy/sprites/pipe-green.png")

    def generate_pipe(self) -> None:  # pipe height 320 / 80 = 3.0
        random_num, value = random.randint(1, 3), 100
        h1 = random_num * value
        h2 = self.H - h1 - value

        self.pipes.append([h1, h2, self.W + self.pipe.get_width()])

    def draw_pipe(self, pipe: tuple) -> None:
        h1, h2, x = pipe
        w, h = self.pipe.get_size()

        y1 = 0 - h + h1
        y2 = self.H - h2

        self.SCREEN.blit(pg.transform.rotate(self.pipe, 180), (x, y1))
        self.SCREEN.blit(self.pipe, (x, y2))

        bw, bh = self.bird.animation.get_size()
        bird = pg.Rect(self.bird.x, self.bird.y, bw, bh)
        pipe1, pipe2 = pg.Rect(x, y1, w, h), pg.Rect(x, y2, w, h)

        if bird.colliderect(pipe1) or bird.colliderect(pipe2):
            self.bird.ALIVE = False

    def draw_pipes(self) -> None:
        for pipe in self.pipes:
            self.draw_pipe(pipe)
            pipe[2] -= self.bird.speed

            if pipe[2] < -self.pipe.get_width():
                self.pipes.remove(pipe)

    def draw_end(self) -> None:
        img = pg.image.load(f"flappy/sprites/gameover.png")

        x = (self.W - img.get_width()) // 2
        y = (self.H - img.get_height()) // 2

        self.SCREEN.blit(img, (x, y))

    def run(self) -> None:
        self.SCREEN = pg.display.set_mode([self.W, self.H])

        pg.display.set_caption("Flappy Bird")

        self.load_animations()

        counter = 0
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                    if event.key == pg.K_SPACE:
                        self.bird.up = True

                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        self.bird.up = False

            if self.bird.ALIVE:
                self.bird.update_animation()

                self.SCREEN.blit(self.background, (0, 0))
                self.SCREEN.blit(pg.transform.rotate(self.bird.animation, self.bird.rotation), (self.bird.x, self.bird.y))
                self.draw_pipes()

                self.bird.fly()
            else:
                self.draw_end()

            if self.bird.y < 0 or self.bird.y > self.H:
                self.bird.ALIVE = False

            if counter == 650:
                self.generate_pipe()
                counter = 0
            else:
                counter += 1

            pg.display.update()

        pg.quit()
