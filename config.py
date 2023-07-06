class Config:
    # Network parameters
    network_dimensions = [9, 4, 2]
    network_evol_std = 0.1
    network_mut_prob = 0.01

    # Agent parameters
    agent_init_health = 50
    agent_hunger = 0.1
    agent_max_health = 100
    agent_speed = 5
    agent_wall_damage = 10
    agent_sight_cones = [[-45, -15], [-15, 15], [15, 45]]
    agent_sight_range = 300

    # Reproduction parameters
    reproduction_cost = 20
    reproduction_min_health = 50

    # Display parameters
    display_dimensions = (800, 800)
    display_agent_size = 10
    display_agent_outline = 3
    display_food_size = 3

    # Food parameters
    food_recompense = 30
