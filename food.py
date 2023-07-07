import numpy as np
from config import Config

class Food:
    def __init__(self):
        self.x = np.random.randint(0, Config.display_dimensions[0])
        self.y = np.random.randint(0, Config.display_dimensions[1])

    def draw(self, canvas):
        canvas.create_oval(self.x - 3, self.y - 3, self.x +
                           3, self.y + 3, fill="green")
