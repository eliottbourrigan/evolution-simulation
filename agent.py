import math
from network import *
import numpy as np

NW_SIZES = [7, 4, 2]
INITIAL_HEALTH = 30
HUNGER_RATE = 0.1
MAX_HEALTH = 100
EVOL_STD = 0.2
MUTATION_PROB = 5e-2
REPRODUCTION_COST = 30
REPRODUCTION_HEALTH = 50
WINDOW_SIZE = (800, 800)
SPEED = 5
FOOD_BONUS = 20


def calculate_distances(agents, observer):
    left_cone = (-45, -15)
    central_cone = (-15, 15)
    right_cone = (15, 45)

    # distances pour chaque cône (gauche, central, droit)
    distances = [0, 0, 0]

    for agent in agents:
        # Calculer l'angle entre l'agent observateur et l'agent actuel
        angle = math.degrees(math.atan2(
            - observer.y + agent.y, - observer.x + agent.x))

        # Soustraire l'angle de vision de l'agent observateur
        angle -= observer.angle

        # Calculer la distance entre l'agent observateur et l'agent actuel
        distance = math.sqrt(
            (agent.x - observer.x)**2 + (agent.y - observer.y)**2)

        # Vérifier dans quel cône se trouve l'agent actuel
        if left_cone[0] <= angle <= left_cone[1]:
            if distances[0] == 0 or distance < distances[0]:
                distances[0] = distance
        elif central_cone[0] <= angle <= central_cone[1]:
            if distances[1] == 0 or distance < distances[1]:
                distances[1] = distance
        elif right_cone[0] <= angle <= right_cone[1]:
            if distances[2] == 0 or distance < distances[2]:
                distances[2] = distance

    new_distances = []
    for distance in distances:
        if distance > 500 or distance == 0.0:
            new_distances.append(0)
        else:
            new_distances.append(1 - distance / 500)
    return new_distances


def health_to_color(value, is_selected):
    if not is_selected:
        return "#333333"

    # Vérification des limites
    if value < 0:
        value = 0
    elif value > 100:
        value = 100

    # Calcul de la composante rouge et bleue en fonction de la valeur
    red = int((100 - value) / 100 * 255)
    blue = int(value / 100 * 255)

    # Conversion en format hexadécimal
    color_hex = "#{:02x}{:02x}ff".format(red, blue)

    return color_hex


class Agent:
    def __init__(self, nw=None, x=None, y=None, angle=None):
        if nw == None:
            self.network = Network(NW_SIZES[0])
            for size in NW_SIZES[1:]:
                self.network.add_layer(size)
        else:
            self.network = nw
        if x == None:
            self.x = np.random.randint(0, WINDOW_SIZE[0])
        else:
            self.x = x
        if y == None:
            self.y = np.random.randint(0, WINDOW_SIZE[1])
        else:
            self.y = y
        if angle == None:
            self.angle = np.random.randint(0, 360)
        else:
            self.angle = angle
        self.health = INITIAL_HEALTH
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

        new_nw.mutate(EVOL_STD, MUTATION_PROB)
        print("Reproduced")
        return Agent(new_nw, self.x, self.y)

    def draw(self, canvas):
        # Draw cone of sight
        '''
        cone_color = "yellow"
        cone_size = 100
        cone_angle = 45
        start_angle = - self.angle - cone_angle
        end_angle = - self.angle + cone_angle
        canvas.create_arc(self.x - cone_size, self.y - cone_size,
                          self.x + cone_size, self.y + cone_size,
                          start=start_angle, extent=2 * cone_angle,
                          outline=cone_color)
        '''

        # Draw agent as a red circle
        health_color = health_to_color(self.health, self.selected)
        agent_radius = 5
        canvas.create_oval(self.x - agent_radius, self.y - agent_radius,
                           self.x + agent_radius, self.y + agent_radius,
                           fill=health_color, outline='', width=0)

        # Draw point in the direction of the agent
        x, y = self.x, self.y
        next_x = self.x + \
            math.cos(math.radians(self.angle)) * agent_radius * 2.5
        next_y = self.y + \
            math.sin(math.radians(self.angle)) * agent_radius * 2.5
        x, y = next_x, next_y
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3,
                           fill=health_color, outline='', width=0)

    def loop(self, game):
        self.health -= HUNGER_RATE
        observed_agents = calculate_distances(game.agents, self)
        # print(observed_agents)
        observed_food = calculate_distances(game.food, self)
        # print(observed_food)
        inputs = np.array(observed_agents + observed_food +
                          [self.health / MAX_HEALTH])
        outputs = self.network.feedforward(inputs)
        self.angle += outputs[0] * 10
        self.angle -= outputs[1] * 10
        self.angle %= 360
        self.x += math.cos(math.radians(self.angle)) * SPEED
        self.x %= WINDOW_SIZE[0]
        self.y += math.sin(math.radians(self.angle)) * SPEED
        self.y %= WINDOW_SIZE[1]

        for food in game.food:
            distance = math.sqrt(
                (food.x - self.x)**2 + (food.y - self.y)**2)
            if distance < 10:
                self.health += FOOD_BONUS
                self.health = min(self.health, MAX_HEALTH)
                game.food.remove(food)

        for agent in game.agents:
            distance = math.sqrt(
                (agent.x - self.x)**2 + (agent.y - self.y)**2)
            if distance < 10:
                if distance > 0.0:
                    if self.health > REPRODUCTION_HEALTH and agent.health > REPRODUCTION_HEALTH:
                        self.health -= REPRODUCTION_COST
                        agent.health -= REPRODUCTION_COST
                        game.agents.append(self.reproduce(agent))
