from agent import *
from food import *
from network import *
import numpy as np
import tkinter as tk
import random
import time

try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


class Game:
    def __init__(self, n_agents, n_food):
        self.agents = [Agent() for _ in range(n_agents)]
        self.food = [Food() for _ in range(n_food)]
        self.timer = 0
        self.display = True
        self.delay = 0

    def loop(self):
        ''' Main loop of the game '''

        self.timer += 1
        if np.random.rand() < Config.food_spawn_prob:
            self.food.append(Food())

        # Delay
        for agent in self.agents:
            if agent.health <= 0:
                if len(self.agents) == 2:
                    agent.health = Config.agent_init_health
                    agent.loop(self)
                else:
                    self.agents.remove(agent)
            else:
                agent.loop(self)

        # Logging
        if self.timer % 1000 == 0:
            print("Interation n°" + str(self.timer) +
                  " : Population = " + str(len(self.agents)))

    def first_draw(self):
        ''' Initializes the window and draws the first frame '''

        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window,
                                width=Config.display_dimensions[0],
                                height=Config.display_dimensions[1])
        self.canvas.pack()
        self.canvas.configure(bg="#0a0a1f")

        # Bind keys to functions
        self.window.bind_all("<space>", lambda event: self.toggle_display())
        self.window.bind_all("<s>", lambda event: self.select_first())
        self.window.bind_all("<o>", lambda event: self.delay_up())
        self.window.bind_all("<i>", lambda event: self.delay_down())

        # Window mainloop
        self.window.after(1, self.loop_and_update)
        self.window.mainloop()

    def select_first(self):
        ''' Selects the first agent '''

        print('Selecting first agent')
        for agent in self.agents:
            agent.selected = False
        self.agents[0].selected = True

    def toggle_display(self):
        ''' Toggles the display '''
        self.display = not self.display

    def delay_up(self):
        ''' Increases the delay '''
        print('Delay set to ', self.delay, 'ms')
        self.delay += 1

    def delay_down(self):
        ''' Decreases the delay '''
        print('Delay set to ', self.delay, 'ms')
        if self.delay > 0:
            self.delay -= 1

    def loop_and_update(self):
        ''' Main loop of the game '''
        self.loop()
        if self.display:
            self.canvas.delete("all")
            for agent in self.agents:
                agent.draw_tail(self.canvas)
                if agent.selected:
                    agent.draw_cone(self.canvas)
            for agent in self.agents:
                agent.draw(self.canvas)
            for food in self.food:
                food.draw(self.canvas)
            if self.delay != 0:
                time.sleep(self.delay / 1000)

        self.window.after(1, self.loop_and_update)
