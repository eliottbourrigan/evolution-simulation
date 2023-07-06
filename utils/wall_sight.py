from config import Config


def wall_sight(agent: Agent):
    ''' Computes the sight input for the agent '''

    min_dists = []

    for angle in agent.wall_sight_angles:
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
            distance_left = - agent_x / dx
            distance_right = (window_width - agent_x) / dx
            distance_top = - agent_y / dy
            distance_bottom = (window_height - agent_y) / dy

            # Keep the minimum positive distance
            for distance in [distance_left, distance_right, distance_top, distance_bottom]:
                if distance > 0 and distance < min_distance:
                    min_dist = distance

        # Normalize the distance between 0 and 1, 0 being the farthest
        min_dists.append(
            0 if min_dist > Config.agent_wall_sight_range else 1 - min_dist / Config.agent_wall_sight_range)

    # Returns the sight input
    return min_dists
