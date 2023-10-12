from typing import Union
from functions_bicing import distancia_manhattan
from estaciones_bicing import Estacion

class Furgoneta(object):
    def __init__(self, estacion_origen: Union[None, Estacion] = None, id = None):
        self.id = id
        self.estacion_origen = estacion_origen
        self.estaciones_destino: list[Estacion] = []
        self.origenX = None
        self.origenY = None
        self.num_bicicletas_cargadas = 0
        self.coord_destinos: list[tuple] = [(self.origenX, self.origenY), (self.origenX, self.origenY)]
        self.num_bicicletas_descargadas_destino1: int = 0
        self.num_bicicletas_descargadas_destino2: int = 0

    def copy(self):
        new_furgoneta = Furgoneta(self.estacion_origen, self.id)
        new_furgoneta.estaciones_destino = [estacion.copy() for estacion in self.estaciones_destino]
        new_furgoneta.origenX = self.origenX
        new_furgoneta.origenY = self.origenY
        new_furgoneta.num_bicicletas_cargadas = self.num_bicicletas_cargadas
        new_furgoneta.coord_destinos = self.coord_destinos.copy()
        new_furgoneta.num_bicicletas_descargadas_destino1 = self.num_bicicletas_descargadas_destino1
        new_furgoneta.num_bicicletas_descargadas_destino2 = self.num_bicicletas_descargadas_destino2
        # Copia y asigna otros atributos si es necesario
        return new_furgoneta

    def set_estaciones_destinos(self, destino1: Estacion, destino2: Estacion):
        if distancia_manhattan((self.origenX, self.origenY), (destino1.coordX, destino1.coordY)) \
            < distancia_manhattan((self.origenX, self.origenY), (destino2.coordX, destino2.coordY)):
            self.coord_destinos = [(destino1.coordX, destino1.coordY), (destino2.coordX, destino2.coordY)]
            self.estaciones_destino = [destino1, destino2]
        else:
            self.coord_destinos = [(destino2.coordX, destino2.coordY), (destino1.coordX, destino1.coordY)]
            self.estaciones_destino = [destino2, destino1]
    
    def set_estacion_origen(self, estacion_origen: Estacion):
        self.estacion_origen = estacion_origen
        self.origenX = estacion_origen.coordX
        self.origenY = estacion_origen.coordY

    #def set_num_bicicletas_cargadas(self, num_bicicletas: int):
        #self.num_bicicletas_cargadas = num_bicicletas

    def realizar_ruta(self, estacion_descarga1: Estacion, estacion_descarga2: Estacion, num_bicicletas_carga: int):
        self.__cargar_bicicletas(num_bicicletas_carga)
        self.__descargar_bicicletas(estacion_descarga1, estacion_descarga2)
        self.beneficio_descargas = self.num_bicicletas_descargadas_destino1 + self.num_bicicletas_descargadas_destino2 - self.num_bicicletas_cargadas   
    
    def __cargar_bicicletas(self, num_bicicletas_carga: int):
        self.num_bicicletas_cargadas = num_bicicletas_carga
        self.estacion_origen.num_bicicletas_no_usadas -= num_bicicletas_carga
        self.estacion_origen.diferencia -= num_bicicletas_carga

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
        
        km_trayecto1 = round(distancia_manhattan((self.origenX, self.origenY), self.coord_destinos[0]) / 1000, 5)
        km_trayecto2 = round(distancia_manhattan(self.coord_destinos[0], self.coord_destinos[1]) / 1000, 5)
        
        coste_trayecto1 = ((nb_trayecto1 + 9) // 10) * km_trayecto1
        coste_trayecto2 = ((nb_trayecto2 + 9) // 10) * km_trayecto2

        return coste_trayecto1 + coste_trayecto2
    
    def __eq__(self, other: 'Furgoneta'):
        return isinstance(other, Furgoneta) and \
            self.origenX == other.origenX and \
                self.origenY == other.origenY

    def __repr__(self) -> str:
        return f"Furgoneta(coordX={self.origenX}, coordY={self.origenY}, num_bicicletas_cargadas={self.num_bicicletas_cargadas}, " \
             + f"num_bicicletas_descargadas_destino1={self.num_bicicletas_descargadas_destino1}, coste_ruta={self.calcular_coste_ruta()}, " \
                + f"coord_destinos={self.coord_destinos}, beneficio_descargas={self.beneficio_descargas})"