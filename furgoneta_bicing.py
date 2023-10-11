from typing import Union
class Furgoneta(object):
    def __init__(self, x: Union[int, None] = None, y: Union[int, None] = None, num_bicicletas: int = 0):
        self.origenX = x
        self.origenY = y
        self.km = 0
        self.num_bicicletas = num_bicicletas
        self.coord_destinos = [(self.origenX, self.origenY), (self.origenX, self.origenY)]

    def __eq__(self, other: 'Furgoneta'):
        return isinstance(other, Furgoneta) and \
            self.origenX == other.origenX and \
                self.origenY == other.origenY and \
                    self.num_bicicletas == other.num_bicicletas
    
    def __repr__(self) -> str:
        return f"Furgoneta(coordX={self.origenX}, coordY={self.origenY}, num_bicicletas={self.num_bicicletas}, km={self.km}, coord_finales={self.coord_destinos})"