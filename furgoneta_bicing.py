from typing import Union
class Furgoneta(object):
    def __init__(self, x: int, y: int, num_bicicletas: Union[int, None] = None):
        self.coordX = x
        self.coordY = y
        self.km = 0
        self.num_bicicletas = num_bicicletas
        

    def __eq__(self, other):
        return isinstance(other, Furgoneta) and \
            self.coordX == other.coordX and \
                self.coordY == other.coordY and \
                    self.num_bicicletas == other.num_bicicletas