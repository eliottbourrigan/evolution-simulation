import math
from network import *
import numpy as np
from config import Config
from utils.cone_sight import cone_sight
from utils.health_to_color import health_to_color
from utils.wall_sight import wall_sight
from utils.create_arrow import create_arrow


class Agent:
    def __init__(self, nw=None, x=None, y=None, angle=None):
        ''' Initializes an agent with a network, position and angle '''

        if nw == None:
            self.network = Network(Config.network_dimensions[0])
            for size in Config.network_dimensions[1:]:
                self.network.add_layer(size)
        else:
            self.network = nw
        self.x = x if x != None else np.random.randint(
            0, Config.display_dimensions[0])
        self.y = y if y != None else np.random.randint(
            0, Config.display_dimensions[1])
        self.angle = angle if angle != None else np.random.randint(0, 360)

        self.health = Config.agent_init_health
        self.selected = False
        self.tail = []

    def reproduce(self, other_agent):
        ''' Returns a new agent with a mutated mix of the 2 agents' networks '''

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
        ''' Draws the agent's sight cones '''

        for i, [start_angle, end_angle] in enumerate(Config.agent_sight_cones):
            cone_size = Config.agent_sight_range
            canvas.create_arc(self.x - cone_size, self.y - cone_size,
                              self.x + cone_size, self.y + cone_size,
                              start=start_angle - self.angle,
                              extent=end_angle - start_angle,
                              outline=Config.display_bg_color,
                              fill=Config.display_cone_colors[i],
                              width=2)

    def draw(self, canvas):
        ''' Draws the agent on the canvas '''

        if self.selected:
            # Draw agent's outline
            create_arrow(canvas, self.x, self.y, self.angle, Config.display_agent_size +
                         Config.display_agent_outline, Config.display_outline_color)

        # Draw agent
        create_arrow(canvas, self.x, self.y, self.angle,
                     Config.display_agent_size, health_to_color(self.health))

    def draw_tail(self, canvas):
        ''' Draw agent's tail '''

        if len(self.tail) == Config.display_tail_length:
            self.tail = self.tail[1:]
        self.tail.append([self.x, self.y, health_to_color(self.health)])

        current_tail = self.tail + \
            [[self.x, self.y, health_to_color(self.health)]]
        for i, [x, y, c] in enumerate(self.tail):
            [nx, ny, nc] = current_tail[i + 1]
            c = health_to_color(
                self.health, alpha=Config.display_tail_alpha * i / Config.display_tail_length)
            canvas.create_line(x, y, nx, ny, fill=c,
                               width=5 * i / Config.display_tail_length)

    def loop(self, game):
        ''' Main loop of the agent, called every frame '''

        # Compute neural network inputs
        agents_sight_input = cone_sight(
            [[agent.x, agent.y] for agent in game.agents], self)
        food_sight_input = cone_sight(
            [[food.x, food.y] for food in game.food], self)
        wall_sight_input = wall_sight(self)
        health_input = [self.health / Config.agent_max_health]

        # Feed inputs to the network
        inputs = np.concatenate(
            (agents_sight_input, food_sight_input, wall_sight_input, health_input))
        [angle_variation] = self.network.feedforward(inputs)

        # Update agent's position, angle and health
        self.angle += ((angle_variation - 0.5) * 40) % 360
        new_x = self.x + \
            math.cos(math.radians(self.angle)) * Config.agent_speed
        new_y = self.y + \
            math.sin(math.radians(self.angle)) * Config.agent_speed
        self.health -= Config.agent_hunger

        # If out of bounds in x, bounce on the wall
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

        # If out of bounds in y, bounce on the wall
        if new_y < 0:
            self.angle = - self.angle
            self.y = 1
        elif new_y > Config.display_dimensions[1]:
            self.angle = - self.angle
            self.y = Config.display_dimensions[1] - 1
        else:
            self.y = new_y

        # Eat food
        for food in game.food:
            distance = math.sqrt(
                (food.x - self.x)**2 + (food.y - self.y)**2)
            if distance < 10:
                self.health += Config.food_recompense
                self.health = min(self.health, Config.agent_max_health)
                game.food.remove(food)

        # Reproduce
        for agent in game.agents:
            distance = math.sqrt(
                (agent.x - self.x)**2 + (agent.y - self.y)**2)
            if distance < 10:
                if distance > 0.0:
                    if self.health > Config.reproduction_min_health and agent.health > Config.reproduction_min_health:
                        self.health -= Config.reproduction_cost
                        agent.health -= Config.reproduction_cost
                        game.agents.append(self.reproduce(agent))
