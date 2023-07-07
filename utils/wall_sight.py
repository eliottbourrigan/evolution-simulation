import math
from config import Config


def wall_sight(agent):
    ''' Computes the sight input for the agent '''

    min_dists = []

    for angle in Config.agent_wall_sight_angles:
        # Compute dx and dy
        angle_rad = math.radians(angle)
        dx = math.cos(angle_rad)
        dy = math.sin(angle_rad)
        min_dist = float('inf')

        # Check division by 0
        if dx == 0 or dy == 0:
            min_dist = 0
        else:
            # Compute the distance to all 4 walls
            distance_left = - agent.x / dx
            distance_right = (Config.display_dimensions[0] - agent.x) / dx
            distance_top = - agent.y / dy
            distance_bottom = (Config.display_dimensions[1] - agent.y) / dy

            # Keep the minimum positive distance
            for distance in [distance_left, distance_right, distance_top, distance_bottom]:
                if distance > 0 and distance < min_dist:
                    min_dist = distance

        # Normalize the distance between 0 and 1, 0 being the farthest
        min_dists.append(
            0 if min_dist > Config.agent_wall_sight_range else 1 - min_dist / Config.agent_wall_sight_range)

    # Returns the sight input
    return min_dists
