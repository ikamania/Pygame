class Snake:
    def __init__(self) -> None:
        self.length = 1
        self.size = 20
        self.color = "RED"
        self.possitions = [[0, 0]]

    def eat(self) -> None:
        self.length += 1