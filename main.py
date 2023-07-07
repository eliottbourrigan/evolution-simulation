import numpy as np
import matplotlib.pyplot as plt

from config import Config
from game import Game
from network import Network
from agent import Agent
from food import Food

from utils.create_arrow import create_arrow
from utils.health_to_color import health_to_color
from utils.cone_sight import cone_sight

game = Game(Config.initial_number_agents, Config.initial_number_food)
game.first_draw()
