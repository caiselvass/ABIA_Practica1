def distancia_manhattan(coord1: tuple, coord2: tuple):
    """
    Calcula la distancia de Manhattan entre dos puntos.
    """
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])
