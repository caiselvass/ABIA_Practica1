from typing import Union
class Furgoneta(object):
    def __init__(self, x: Union[int, None] = None, y: Union[int, None] = None, num_bicicletas: int = 0):
        self.coordX = x
        self.coordY = y
        self.km = 0
        self.num_bicicletas = num_bicicletas

    def __eq__(self, other: 'Furgoneta'):
        return isinstance(other, Furgoneta) and \
            self.coordX == other.coordX and \
                self.coordY == other.coordY and \
                    self.num_bicicletas == other.num_bicicletas
    
    def __repr__(self) -> str:
        return f"Furgoneta(coordX={self.coordX}, coordY={self.coordY}, num_bicicletas={self.num_bicicletas}, km={self.km})"