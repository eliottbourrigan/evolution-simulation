from utils.various import cos_rad, sin_rad


def create_arrow(canvas, x, y, angle, size, color) -> None:
    ''' Creates an arrow on the canvas based on the given position, angle, size and color '''
    return canvas.create_polygon(x + cos_rad(angle) * size,
                                 y + sin_rad(angle) * size,
                                 x + cos_rad(angle + 120) * size,
                                 y + sin_rad(angle + 120) * size,
                                 x, y,
                                 x + cos_rad(angle - 120) * size,
                                 y + sin_rad(angle - 120) * size,
                                 fill=color, outline='')
