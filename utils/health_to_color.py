from config import Config


def health_to_color(value, colored=True, alpha=None):
    ''' Returns the color corresponding to the health value '''

    # If the agent is not colored, returns a gray color
    if not colored or value < 0:
        return "#333333"

    # Calcul de la composante rouge et bleue en fonction de la valeur
    red = int((100 - value) / 100 * 255)
    blue = int(value / 100 * 255)
    if alpha != None:
        red = int(alpha * red + (1 - alpha) *
                  Config.display_bg_color_[0])
        blue = int(alpha * blue + (1 - alpha) *
                   Config.display_bg_color_[2])

    color_hex = "#{:02x}00{:02x}".format(red, blue)

    return color_hex
