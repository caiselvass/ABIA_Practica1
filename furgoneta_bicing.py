from typing import Union
from functions_bicing import distancia_manhattan
from estaciones_bicing import Estacion

class Furgoneta(object):
    def __init__(self, x: Union[int, None] = None, y: Union[int, None] = None):
        self.origenX = x
        self.origenY = y
        self.num_bicicletas_cargadas = 0
        self.coord_destinos: list[tuple] = [(self.origenX, self.origenY), (self.origenX, self.origenY)]
        self.num_bicicletas_descargadas_destino1: int = 0
        self.num_bicicletas_descargadas_destino2: int = 0

    def set_coord_destinos(self, destino1: tuple[int, int], destino2: tuple[int, int]):
        if distancia_manhattan((self.origenX, self.origenY), destino1) < distancia_manhattan((self.origenX, self.origenY), destino2):
            self.coord_destinos = [destino1, destino2]
        else:
            self.coord_destinos = [destino2, destino1]
    
    def set_coord_origen(self, new_x: int, new_y: int):
        self.origenX = new_x
        self.origenY = new_y

    #def set_num_bicicletas_cargadas(self, num_bicicletas: int):
        #self.num_bicicletas_cargadas = num_bicicletas

    def realizar_ruta(self, estacion_carga: Estacion, estacion_descarga1: Estacion, estacion_descarga2: Estacion, num_bicicletas_carga: int):
        self.__cargar_bicicletas(estacion_carga, num_bicicletas_carga)
        self.__descargar_bicicletas(estacion_descarga1, estacion_descarga2)
        self.beneficio_descargas = self.num_bicicletas_descargadas_destino1 + self.num_bicicletas_descargadas_destino2 - self.num_bicicletas_cargadas   

    def __cargar_bicicletas(self, estacion_carga: Estacion, num_bicicletas_carga: int):
        print(f"{estacion_carga} carreguem {num_bicicletas_carga} bicis")
        self.num_bicicletas_cargadas = num_bicicletas_carga
        estacion_carga.num_bicicletas_no_usadas -= num_bicicletas_carga
        estacion_carga.diferencia -= num_bicicletas_carga
        print(f"{estacion_carga}\n")

    def __descargar_bicicletas(self, estacion_descarga1: Estacion, estacion_descarga2: Estacion):
        self.num_bicicletas_descargadas_destino1 = min(self.num_bicicletas_cargadas, abs(estacion_descarga1.diferencia))
        self.num_bicicletas_descargadas_destino2 = self.num_bicicletas_cargadas - self.num_bicicletas_descargadas_destino1


        estacion_descarga1.num_bicicletas_no_usadas += self.num_bicicletas_descargadas_destino1
        estacion_descarga2.num_bicicletas_no_usadas += self.num_bicicletas_descargadas_destino2 
        estacion_descarga1.diferencia += self.num_bicicletas_descargadas_destino1
        estacion_descarga2.diferencia += self.num_bicicletas_descargadas_destino2
    
    def calcular_coste_ruta(self):
        nb_trayecto1 = self.num_bicicletas_cargadas
        nb_trayecto2 = self.num_bicicletas_descargadas_destino2
        
        km_trayecto1 = distancia_manhattan((self.origenX, self.origenY), self.coord_destinos[0]) / 1000
        km_trayecto2 = distancia_manhattan(self.coord_destinos[0], self.coord_destinos[1]) / 1000
        
        coste_trayecto1 = ((nb_trayecto1 + 9) // 10) * km_trayecto1
        coste_trayecto2 = ((nb_trayecto2 + 9) // 10) * km_trayecto2

        return coste_trayecto1 + coste_trayecto2
    
    def __eq__(self, other: 'Furgoneta'):
        return isinstance(other, Furgoneta) and \
            self.origenX == other.origenX and \
                self.origenY == other.origenY

    def __repr__(self) -> str:
        return f"Furgoneta(coordX={self.origenX}, coordY={self.origenY}, num_bicicletas_cargadas={self.num_bicicletas_cargadas}, " \
             + f"num_bicicletas_descargadas_destino1={self.num_bicicletas_descargadas_destino1}, coste_ruta={self.calcular_coste_ruta()}, coord_destinos={self.coord_destinos}, beneficio_descargas={self.beneficio_descargas})"