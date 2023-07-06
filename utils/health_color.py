def health_color(value, colored):
    ''' Returns the color corresponding to the health value '''

    # If the agent is not colored, returns a gray color
    if not colored:
        return "#333333"

    # Calcul de la composante rouge et bleue en fonction de la valeur
    red = int((100 - value) / 100 * 255)
    blue = int(value / 100 * 255)
    color_hex = "#{:02x}00{:02x}".format(red, blue)

    return color_hex
