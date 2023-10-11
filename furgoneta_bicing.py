from typing import Union
from parameters_bicing import distancia_manhattan
class Furgoneta(object):
    def __init__(self, x: Union[int, None] = None, y: Union[int, None] = None):
        self.origenX = x
        self.origenY = y
        self.num_bicicletas_cargadas = 0
        self.coord_destinos: list[tuple] = [(self.origenX, self.origenY), (self.origenX, self.origenY)]
        self.num_bicicletas_descargadas_destino1: int = 0
        self.beneficio_descargas: int = 0

    def set_coord_destinos(self, destino1: tuple[int, int], destino2: tuple[int, int]):
        if distancia_manhattan((self.origenX, self.origenY), destino1) < distancia_manhattan((self.origenX, self.origenY), destino2):
            self.coord_destinos = [destino1, destino2]
        else:
            self.coord_destinos = [destino2, destino1]

    def __eq__(self, other: 'Furgoneta'):
        return isinstance(other, Furgoneta) and \
            self.origenX == other.origenX and \
                self.origenY == other.origenY
    
    def calcular_coste_ruta(self):
        nb_trayecto1 = self.num_bicicletas_cargadas
        nb_trayecto2 = self.num_bicicletas_cargadas - self.num_bicicletas_descargadas_destino1
        
        km_trayecto1 = distancia_manhattan((self.origenX, self.origenY), self.coord_destinos[0]) / 1000
        km_trayecto2 = distancia_manhattan(self.coord_destinos[0], self.coord_destinos[1]) / 1000
        
        coste_trayecto1 = ((nb_trayecto1 + 9) // 10) * km_trayecto1
        coste_trayecto2 = ((nb_trayecto2 + 9) // 10) * km_trayecto2

        return coste_trayecto1 + coste_trayecto2
    
    def __repr__(self) -> str:
        return f"Furgoneta(coordX={self.origenX}, coordY={self.origenY}, num_bicicletas_cargadas={self.num_bicicletas_cargadas}," \
             + f"num_bicicletas_descargadas_destino1={self.num_bicicletas_descargadas_destino1}, coste_ruta={self.calcular_coste_ruta()}, coord_destinos={self.coord_destinos})"