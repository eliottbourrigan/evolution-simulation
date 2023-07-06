import math
from network import *
import numpy as np
from config import Config


class Agent:
    def __init__(self, nw=None, x=None, y=None, angle=None):
        self.is_sprinting = False
        if nw == None:
            self.network = Network(Config.network_dimensions[0])
            for size in Config.network_dimensions[1:]:
                self.network.add_layer(size)
        else:
            self.network = nw
        if x == None:
            self.x = np.random.randint(0, Config.display_dimensions[0])
        else:
            self.x = x
        if y == None:
            self.y = np.random.randint(0, Config.display_dimensions[1])
        else:
            self.y = y
        if angle == None:
            self.angle = np.random.randint(0, 360)
        else:
            self.angle = angle
        self.health = Config.agent_init_health
        self.selected = False

    def reproduce(self, other_agent):
        new_nw = self.network.copy()
        other_nw = other_agent.network

        # mean of the 2 weights and biases vectors
        for k, layer in enumerate(new_nw.layers):
            new_nw.layers[k].weights = (
                layer.weights + other_nw.layers[k].weights) / 2
            new_nw.layers[k].biases = (
                layer.biases + other_nw.layers[k].biases) / 2

        new_nw.mutate(Config.network_evol_std, Config.network_mut_prob)
        return Agent(new_nw, self.x, self.y)

    def draw_cone(self, canvas):
        if self.selected:
            cone_color = "yellow"
            cone_size = 300
            cone_angles = [-45, -15, 15, 45]
            colors = ["#0c0c22", "#0f0f25", "#0c0c22"]
            for i in range(len(cone_angles) - 1):
                start_angle = - self.angle + cone_angles[i]
                end_angle = - self.angle + cone_angles[i + 1]
                canvas.create_arc(self.x - cone_size, self.y - cone_size,
                                  self.x + cone_size, self.y + cone_size,
                                  start=start_angle, extent=end_angle - start_angle,
                                  outline='#0a0a1f', fill=colors[i], width=2)

    def draw(self, canvas):
        # Draw cone of sight
        '''
        # Draw agent as a red circle
        health_color = health_to_color(self.health, self.selected)
        ag_rad = 5
        canvas.create_oval(self.x - ag_rad, self.y - ag_rad,
                           self.x + ag_rad, self.y + ag_rad,
                           fill=health_color, outline='', width=0)
        '''
        # Draw agent as triangle pointing in the direction of the agent
        if self.is_sprinting:
            ag_rad = 11
            health_color = health_to_color(self.health, True)
            if self.selected:
                outline = "white"
            else:
                outline = ""
            x, y = self.x, self.y
            next_x, next_y = x + math.cos(math.radians(self.angle)) * ag_rad, y + math.sin(
                math.radians(self.angle)) * ag_rad
            canvas.create_polygon(next_x, next_y,
                                  x +
                                  math.cos(math.radians(
                                      self.angle + 120)) * ag_rad,
                                  y +
                                  math.sin(math.radians(
                                      self.angle + 120)) * ag_rad,
                                  x +
                                  math.cos(math.radians(
                                      self.angle - 180)) * 3,
                                  y +
                                  math.sin(math.radians(
                                      self.angle - 180)) * 3,
                                  x +
                                  math.cos(math.radians(
                                      self.angle - 120)) * ag_rad,
                                  y +
                                  math.sin(math.radians(
                                      self.angle - 120)) * ag_rad,
                                  fill='white', outline='')

        if self.selected:
            ag_rad = 9
        else:
            ag_rad = 10
        health_color = health_to_color(self.health, True)
        if self.selected:
            outline = "white"
        else:
            outline = ""
        x, y = self.x, self.y
        next_x, next_y = x + math.cos(math.radians(self.angle)) * ag_rad, y + math.sin(
            math.radians(self.angle)) * ag_rad
        canvas.create_polygon(next_x, next_y,
                              x +
                              math.cos(math.radians(
                                  self.angle + 120)) * ag_rad,
                              y +
                              math.sin(math.radians(
                                  self.angle + 120)) * ag_rad,
                              x, y,
                              x +
                              math.cos(math.radians(
                                  self.angle - 120)) * ag_rad,
                              y +
                              math.sin(math.radians(
                                  self.angle - 120)) * ag_rad,
                              fill=health_color, outline='')

        '''
        # Draw point in the direction of the agent
        x, y = self.x, self.y
        next_x = self.x + \
            math.cos(math.radians(self.angle)) * ag_rad * 2.5
        next_y = self.y + \
            math.sin(math.radians(self.angle)) * ag_rad * 2.5
        x, y = next_x, next_y
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3,
                           fill=health_color, outline='', width=0)
        '''

    def loop(self, game):

        observed_agents = calculate_distances(game.agents, self)
        # print(observed_agents)
        observed_food = calculate_distances(game.food, self)
        # print(observed_food)
        right_wall_sight = distance_to_wall(
            self.x, self.y, (self.angle + 15) % 360, Config.display_dimensions[0], Config.display_dimensions[1])
        left_wall_sight = distance_to_wall(
            self.x, self.y, (self.angle - 15) % 360, Config.display_dimensions[0], Config.display_dimensions[1])
        inputs = np.array(observed_agents + observed_food +
                          [self.health / Config.agent_max_health, right_wall_sight, left_wall_sight])
        outputs = self.network.feedforward(inputs)

        sprint = outputs[1] * 3
        self.angle += (outputs[0] - 0.5) * 40 / (1 + 4 * sprint)

        self.is_sprinting = False
        self.angle %= 360

        new_x = self.x + math.cos(math.radians(self.angle)) * \
            (Config.agent_speed * (sprint * 2 + 1))
        self.health -= Config.agent_hunger
        # If out of bounds, bounce on the wall
        if new_x < 0:
            self.angle = 180 - self.angle
            self.x = 1
            self.health -= Config.agent_wall_damage
        elif new_x > Config.display_dimensions[0]:
            self.angle = 180 - self.angle
            self.x = Config.display_dimensions[0] - 1
            self.health -= Config.agent_wall_damage
        else:
            self.x = new_x

        new_y = self.y + math.sin(math.radians(self.angle)) * \
            (Config.agent_speed * (sprint * 2 + 1))
        # If out of bounds, bounce on the wall
        if new_y < 0:
            self.angle = - self.angle
            self.y = 1
        elif new_y > Config.display_dimensions[1]:
            self.angle = - self.angle
            self.y = Config.display_dimensions[1] - 1
        else:
            self.y = new_y

        for food in game.food:
            distance = math.sqrt(
                (food.x - self.x)**2 + (food.y - self.y)**2)
            if distance < 10:
                self.health += Config.food_recompense
                self.health = min(self.health, Config.agent_max_health)
                game.food.remove(food)

        for agent in game.agents:
            distance = math.sqrt(
                (agent.x - self.x)**2 + (agent.y - self.y)**2)
            if distance < 10:
                if distance > 0.0:
                    if self.health > Config.reproduction_min_health and agent.health > Config.reproduction_min_health:
                        self.health -= Config.reproduction_cost
                        agent.health -= Config.reproduction_cost
                        game.agents.append(self.reproduce(agent))
