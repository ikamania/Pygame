import pygame as pg
import random
from GAME.snake import Snake

class App:
    def __init__(self) -> None:
        self.screen = pg.display.set_mode([500, 500])
        self.map = [[0] * 25 for _ in range(25)]
    
    def display_snake(self, snake: type[Snake]) -> None:
        s = snake.size

        for i in range(snake.length):
            pos = snake.possitions[i]
            pg.draw.rect(self.screen, snake.color, (pos[0] * s, pos[1] * s, s, s))

    def check_border(self, j: int) -> int:
        if j < 0: 
            return 24
        elif j > 24:
            return 0
        else:
            return j

    def run(self) -> None:
        running = True
        direction = 0
        delay = 0
        apple = 0

        snake = Snake()
        x, y = snake.possitions[-1]
        a, b = 0, 0

        pg.display.set_caption("Snake")

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN and (direction != 1 or snake.length == 1):
                        direction = 0
                    if event.key == pg.K_UP and (direction != 0 or snake.length == 1):
                        direction = 1
                    if event.key == pg.K_RIGHT and (direction != 3 or snake.length == 1):
                        direction = 2
                    if event.key == pg.K_LEFT and (direction != 2 or snake.length == 1):
                        direction = 3

            if delay == 100:
                if direction == 0:
                    y += 1
                elif direction == 1:
                    y -= 1
                elif direction == 2:    
                    x += 1
                elif direction == 3:
                    x -= 1
                
                for i in range(snake.length):
                    if snake.possitions[i] == [a, b]:
                        snake.eat()
                        apple = 0

                x, y = map(self.check_border, [x, y])

                if [x, y] not in snake.possitions:
                    snake.possitions.append([x, y])
                    if len(snake.possitions) > snake.length:
                        snake.possitions = snake.possitions[1:]
                    while len(snake.possitions) < snake.length:
                        snake.possitions.append([x, y])
                else:
                    running = False

                delay = 0
            
            self.screen.fill("BLACK")
            self.display_snake(snake)

            if apple < 1:
                a, b = random.randint(0, 24), random.randint(0, 24)       
                apple += 1
            else:
                s = snake.size
                pg.draw.rect(self.screen, "GREEN", (a * s, b * s, s, s))

            delay += 1

            pg.display.flip()
            pg.display.update()

        pg.quit()