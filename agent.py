import math
from network import *
import numpy as np

NW_SIZES = [9, 2, 1]
INITIAL_HEALTH = 50
HUNGER_RATE = 0.08
MAX_HEALTH = 100
EVOL_STD = 0.1
MUTATION_PROB = 0.01
REPRODUCTION_COST = 20
REPRODUCTION_HEALTH = 50
WINDOW_SIZE = (800, 800)
SPEED = 5
FOOD_BONUS = 40
WALL_DAMAGE = 10


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
            new_distances.append((1 - distance / 500)**2)
    return new_distances


def distance_to_wall(agent_x, agent_y, angle, window_width, window_height):
    # Convertir l'angle en radians
    angle_rad = math.radians(angle)

    # Calculer les coordonnées du vecteur directeur
    dx = math.cos(angle_rad)
    dy = math.sin(angle_rad)

    # Initialiser la distance minimale à une valeur très élevée
    min_distance = float('inf')

    # Calculer la distance aux murs verticaux (x = 0 et x = window_width)
    if dx != 0:
        # Calculer la distance aux murs x = 0 et x = window_width
        distance_left = -agent_x / dx
        distance_right = (window_width - agent_x) / dx

        # Mettre à jour la distance minimale si nécessaire
        if distance_left > 0 and distance_left < min_distance:
            min_distance = distance_left
        if distance_right > 0 and distance_right < min_distance:
            min_distance = distance_right

    # Calculer la distance aux murs horizontaux (y = 0 et y = window_height)
    if dy != 0:
        # Calculer la distance aux murs y = 0 et y = window_height
        distance_top = -agent_y / dy
        distance_bottom = (window_height - agent_y) / dy

        # Mettre à jour la distance minimale si nécessaire
        if distance_top > 0 and distance_top < min_distance:
            min_distance = distance_top
        if distance_bottom > 0 and distance_bottom < min_distance:
            min_distance = distance_bottom

    if min_distance > 500:
        return 0
    else:
        return (1 - min_distance / 500) ** 2


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
    color_hex = "#{:02x}00{:02x}".format(red, blue)

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
        if self.selected:
            ag_rad = 13
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
        self.health -= HUNGER_RATE
        observed_agents = calculate_distances(game.agents, self)
        # print(observed_agents)
        observed_food = calculate_distances(game.food, self)
        # print(observed_food)
        right_wall_sight = distance_to_wall(
            self.x, self.y, (self.angle + 15) % 360, WINDOW_SIZE[0], WINDOW_SIZE[1])
        left_wall_sight = distance_to_wall(
            self.x, self.y, (self.angle - 15) % 360, WINDOW_SIZE[0], WINDOW_SIZE[1])
        inputs = np.array(observed_agents + observed_food +
                          [self.health / MAX_HEALTH, right_wall_sight, left_wall_sight])
        outputs = self.network.feedforward(inputs)
        self.angle += (outputs[0] - 0.5) * 40
        self.angle %= 360

        new_x = self.x + math.cos(math.radians(self.angle)) * SPEED
        # If out of bounds, bounce on the wall
        if new_x < 0:
            self.angle = 180 - self.angle
            self.x = 1
            self.health -= WALL_DAMAGE
        elif new_x > WINDOW_SIZE[0]:
            self.angle = 180 - self.angle
            self.x = WINDOW_SIZE[0] - 1
            self.health -= WALL_DAMAGE
        else:
            self.x = new_x

        new_y = self.y + math.sin(math.radians(self.angle)) * SPEED
        # If out of bounds, bounce on the wall
        if new_y < 0:
            self.angle = - self.angle
            self.y = 1
        elif new_y > WINDOW_SIZE[1]:
            self.angle = - self.angle
            self.y = WINDOW_SIZE[1] - 1
        else:
            self.y = new_y

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
