class Config:
    # Network parameters
    network_dimensions = [9, 4, 1]
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
    agent_wall_sight_angles = [-15, 15]
    agent_wall_sight_range = 100

    # Reproduction parameters
    reproduction_cost = 20
    reproduction_min_health = 50

    # Display parameters
    display_dimensions = (800, 800)
    display_agent_size = 10.3
    display_agent_outline = 3.0
    display_food_size = 3.3
    display_cone_colors = ["#0c0c22", "#0f0f25", "#0c0c22"]
    display_bg_color = "#0a0a1f"
    display_bg_color_ = (10, 10, 31)
    display_outline_color = "#ffffff"
    display_tail_length = 50
    display_tail_alpha = 0.7

    # Food parameters
    food_recompense = 30
    food_spawn_prob = 0.1

    # Initial population parameters
    initial_number_agents = 2
    initial_number_food = 100
