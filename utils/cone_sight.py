import math
from config import Config


def cone_sight(positions, agent):
    ''' Computes the sight input for the agent '''

    cones_min_dist = [float("inf") for _ in Config.agent_sight_cones]

    for [x, y] in positions:
        # Computes the angle and distance between the agent and the current position
        angle = math.degrees(math.atan2(
            - agent.y + y, - agent.x + x)) - agent.angle
        distance = math.sqrt((agent.x - x)**2 + (agent.y - y)**2)

        # Checks if the position is in the agent's sight
        for i, [start_angle, end_angle] in enumerate(Config.agent_sight_cones):
            if start_angle <= angle <= end_angle and distance < cones_min_dist[i]:
                cones_min_dist[i] = distance

    # Returns the sight input, normalized between 0 and 1, 0 being the farthest
    return [0 if dist > Config.agent_sight_range else 1 - dist / Config.agent_sight_range for dist in cones_min_dist]
