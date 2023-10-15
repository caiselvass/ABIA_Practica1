from typing import Union
from parameters_bicing import params
from functions_bicing import distancia_manhattan

class Furgoneta(object):
    def __init__(self, estacion_origen: dict = dict(), id: Union[int, None] = None) -> None:
        self.id = id
        self.info_est_origen = estacion_origen
        self.info_est_destino: list[dict] = []
        self.origenX = None
        self.origenY = None
        self.num_bicicletas_cargadas = 0
        self.coord_destinos: list[tuple] = [(self.origenX, self.origenY), (self.origenX, self.origenY)]
        self.num_bicicletas_descargadas_destino1: int = 0
        self.num_bicicletas_descargadas_destino2: int = 0

    def copy(self) -> 'Furgoneta':
        new_furgoneta = Furgoneta(self.info_est_origen, self.id)
        new_furgoneta.info_est_destino = [estacion.copy() for estacion in self.info_est_destino]
        new_furgoneta.origenX = self.origenX
        new_furgoneta.origenY = self.origenY
        new_furgoneta.num_bicicletas_cargadas = self.num_bicicletas_cargadas
        new_furgoneta.coord_destinos = self.coord_destinos.copy()
        new_furgoneta.num_bicicletas_descargadas_destino1 = self.num_bicicletas_descargadas_destino1
        new_furgoneta.num_bicicletas_descargadas_destino2 = self.num_bicicletas_descargadas_destino2
        # Copia y asigna otros atributos si es necesario
        return new_furgoneta

    def set_estaciones_destinos(self, destino1: dict, destino2: dict) -> None:
        if distancia_manhattan((self.origenX, self.origenY), (params.estaciones[destino1['index']].coordX , params.estaciones[destino1['index']].coordY)) \
            < distancia_manhattan((self.origenX, self.origenY), (params.estaciones[destino2['index']].coordX , params.estaciones[destino2['index']].coordY)):
            
            self.coord_destinos = [(params.estaciones[destino1['index']].coordX , params.estaciones[destino1['index']].coordY), \
                                   (params.estaciones[destino2['index']].coordX , params.estaciones[destino2['index']].coordY)]
            self.info_est_destino = [destino1, destino2]
        else:
            self.coord_destinos = [(params.estaciones[destino2['index']].coordX , params.estaciones[destino2['index']].coordY), \
                                   (params.estaciones[destino1['index']].coordX , params.estaciones[destino1['index']].coordY)]
            self.info_est_destino = [destino2, destino1]
    
    def set_estacion_origen(self, estacion_origen: dict) -> None:
        self.info_est_origen = estacion_origen
        self.origenX = params.estaciones[estacion_origen['index']].coordX
        self.origenY = params.estaciones[estacion_origen['index']].coordY

    #def set_num_bicicletas_cargadas(self, num_bicicletas: int):
        #self.num_bicicletas_cargadas = num_bicicletas

    def realizar_ruta(self, estacion_descarga1: dict, estacion_descarga2: dict, num_bicicletas_carga: int) -> None:
        self.__cargar_bicicletas(num_bicicletas_carga)
        self.__descargar_bicicletas(estacion_descarga1, estacion_descarga2)
    
    def __cargar_bicicletas(self, num_bicicletas_carga: int) -> None:
        self.num_bicicletas_cargadas = num_bicicletas_carga
        self.info_est_origen['disp'] -= num_bicicletas_carga
        self.info_est_origen['dif'] -= num_bicicletas_carga

    def __descargar_bicicletas(self, estacion_descarga1: dict, estacion_descarga2: dict) -> None:
        self.num_bicicletas_descargadas_destino1 = min(self.num_bicicletas_cargadas, abs(estacion_descarga1['dif']))
        self.num_bicicletas_descargadas_destino2 = self.num_bicicletas_cargadas - self.num_bicicletas_descargadas_destino1

        estacion_descarga1['disp'] += self.num_bicicletas_descargadas_destino1
        estacion_descarga2['disp'] += self.num_bicicletas_descargadas_destino2 
        estacion_descarga1['dif'] += self.num_bicicletas_descargadas_destino1
        estacion_descarga2['dif'] += self.num_bicicletas_descargadas_destino2
    
    def calcular_coste_ruta(self) -> float:
        # COSTE POR KM
        # nb es el número de bicicletas que transportamos en una furgoneta, el coste en euros por kilómetro recorrido es ((nb + 9) div 10), donde div es la división entera.
        
        nb_trayecto1 = self.num_bicicletas_cargadas
        nb_trayecto2 = self.num_bicicletas_descargadas_destino2
        
        km_trayecto1 = round(distancia_manhattan((self.origenX, self.origenY), self.coord_destinos[0]) / 1000, 5) # Redondeamos a 5 decimales para evitar problemas
        km_trayecto2 = round(distancia_manhattan(self.coord_destinos[0], self.coord_destinos[1]) / 1000, 5) # Redondeamos a 5 decimales para evitar problemas
        
        coste_trayecto1 = ((nb_trayecto1 + 9) // 10) * km_trayecto1
        coste_trayecto2 = ((nb_trayecto2 + 9) // 10) * km_trayecto2

        return coste_trayecto1 + coste_trayecto2

    def __eq__(self, other: 'Furgoneta') -> bool:
        # Una furgoneta es igual a otra si tienen el mismo origen (ya que no puede haber dos furgonetas en la misma estación de carga inicial)
        return isinstance(other, Furgoneta) and \
            self.origenX == other.origenX and \
                self.origenY == other.origenY
