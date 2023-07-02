import numpy as np

WINDOW_SIZE = (800, 800)


class Food:
    def __init__(self):
        self.x = np.random.randint(0, WINDOW_SIZE[0])
        self.y = np.random.randint(0, WINDOW_SIZE[1])

    def draw(self, canvas):
        canvas.create_oval(self.x - 5, self.y - 5, self.x +
                           5, self.y + 5, fill="green")
