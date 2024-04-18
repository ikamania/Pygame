class Bird:
    def __init__(self) -> None:
        self.x, self.y = 50, 50

        self.speed = 0.7
        self.gravity = 1.5
        self.animation_speed = 25
        self.counter = 0
        self.up = 0

        self.animation = None
        self.animations = []
        self.rotation = 0

        self.ALIVE = True

    def update_animation(self) -> None:
        if self.animation is None:
            self.animation = self.animations[0]
            return
        if self.counter == self.animation_speed:
            if self.animation == self.animations[-1]:
                self.animation = self.animations[0]
            else:
                self.animation = self.animations[self.animations.index(self.animation) + 1]
            self.counter = 0
        else:
            self.counter += 1

    def fly(self) -> None:
        if self.up:
            self.y -= self.gravity
            self.rotation = 20
        else:
            self.y += self.gravity * 0.8
            self.rotation = 315
