def cos_rad(x):
    return math.cos(math.radians(x))


def sin_rad(x):
    return math.sin(math.radians(x))


def create_arrow(canvas, x, y, angle, size, color):
    canvas.create_polygon(x + cos_rad(angle) * size,
                          y + sin_rad(angle) * size,
                          x + cos_rad(angle + 120) * size,
                          y + sin_rad(angle + 120) * size,
                          x, y,
                          x + cos_rad(angle - 120) * size,
                          y + sin_rad(angle - 120) * size,
                          fill=color, outline='')
