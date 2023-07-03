from agent import *
from food import *
from network import *
import numpy as np
import tkinter as tk
import random
import time

WINDOW_SIZE = (800, 800)
FOOD_SPAWN_PROB = 0.1


class Game:
    def __init__(self, n_agents, n_food):
        self.agents = [Agent() for _ in range(n_agents)]
        self.food = [Food() for _ in range(n_food)]
        self.timer = 0
        self.display = True
        self.delay = 0

    def loop(self):
        self.timer += 1
        if np.random.rand() < FOOD_SPAWN_PROB:
            self.food.append(Food())
        for agent in self.agents:
            if agent.health <= 0:
                if len(self.agents) == 2:
                    agent.health = INITIAL_HEALTH
                else:
                    self.agents.remove(agent)
            else:
                agent.loop(self)
        if self.timer % 1000 == 0:
            print("Interation n°" + str(self.timer) +
                  " : Population = " + str(len(self.agents)))

    def draw(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(
            self.window, width=WINDOW_SIZE[0], height=WINDOW_SIZE[1])
        self.canvas.pack()
        self.window.tk.call('tk', 'scaling', 5.0)
        self.canvas.configure(bg="#0a0a1f")

        # Bind space key to game loop
        self.window.bind_all("<space>", lambda event: self.toggle_display())
        self.window.bind_all("<a>", lambda event: self.select_all())
        self.window.bind_all("<s>", lambda event: self.select_first())
        self.window.bind_all("<o>", lambda event: self.delay_up())
        self.window.bind_all("<i>", lambda event: self.delay_down())
        self.window.bind_all(
            "<Button-1>", lambda event: self.create_agent(event))
        self.window.after(1, self.loop_and_update)

        for agent in self.agents:
            agent.draw(self.canvas)
        for food in self.food:
            food.draw(self.canvas)

        self.window.mainloop()

    def select_all(self):
        print('Selecting all agents')
        for agent in self.agents:
            agent.selected = True

    def select_first(self):
        print('Selecting first agent')
        for agent in self.agents:
            agent.selected = False
        self.agents[0].selected = True

    def create_agent(self, event):
        x = event.x
        y = event.y
        agent = Agent(x=x, y=y)
        game.agents.append(agent)

    def toggle_display(self):
        self.display = not self.display

    def delay_up(self):
        print('Delay set to ', self.delay, 'ms')
        self.delay += 1

    def delay_down(self):
        print('Delay set to ', self.delay, 'ms')
        if self.delay > 0:
            self.delay -= 1

    def loop_and_update(self):
        self.loop()

        if self.display:
            # Clear canvas, then redraw
            self.canvas.delete("all")
            for agent in self.agents:
                agent.draw(self.canvas)
            for food in self.food:
                food.draw(self.canvas)
            if self.delay != 0:
                time.sleep(self.delay / 1000)

        self.window.after(1, self.loop_and_update)


if __name__ == "__main__":
    game = Game(20, 30)
    # Print all initial angles :
    for i, agent in enumerate(game.agents):
        print(i, ':', agent.angle)
    game.draw()
