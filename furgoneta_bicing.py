from typing import Union


class Furgoneta(object):
    def __init__(self, id_furgoneta: int, \
                 id_estacion_origen: Union[int, None] = None, \
                    id_estacion_destino_1: Union[int, None] = None, \
                        id_estacion_destino_2: Union[int,None] = None, \
                            bicicletas_cargadas: int = 0, \
                                bicicletas_descargadas_1: int = 0, \
                                    bicicletas_descargadas_2: int = 0) -> None:
        self.id = id_furgoneta
        self.id_est_origen = id_estacion_origen
        self.id_est_dest1 = id_estacion_destino_1
        self.id_est_dest2 = id_estacion_destino_2
        self.bicicletas_cargadas = bicicletas_cargadas
        self.bicicletas_descargadas_1 = bicicletas_descargadas_1
        self.bicicletas_descargadas_2 = bicicletas_descargadas_2
    
    def __eq__(self, other: 'Furgoneta') -> bool:
        return self.id == other.id \
            and self.id_est_origen == other.id_est_origen \
                and self.id_est_dest1 == other.id_est_dest1 \
                    and self.id_est_dest2 == other.id_est_dest2 \
                        and self.bicicletas_cargadas == other.bicicletas_cargadas \
                            and self.bicicletas_descargadas_1 == other.bicicletas_descargadas_1 \
                                and self.bicicletas_descargadas_2 == other.bicicletas_descargadas_2

    def __repr__(self) -> str:
        return f"F[{self.id}]: C={self.id_est_origen} (num={self.bicicletas_cargadas}) | D1={self.id_est_dest1} (num={self.bicicletas_descargadas_1}) | D2={self.id_est_dest2} (num={self.bicicletas_descargadas_2})"

    def copy(self) -> 'Furgoneta':
        return Furgoneta(self.id, \
                         self.id_est_origen, \
                            self.id_est_dest1, \
                                self.id_est_dest2, \
                                    self.bicicletas_cargadas, \
                                        self.bicicletas_descargadas_1, \
                                            self.bicicletas_descargadas_2)


    """
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
        new_furgoneta = Furgoneta(estacion_origen=self.info_est_origen, id=self.id)
        new_furgoneta.info_est_destino = [{key: value for key, value in estacion.items()} for estacion in self.info_est_destino]
        new_furgoneta.origenX = self.origenX
        new_furgoneta.origenY = self.origenY
        new_furgoneta.num_bicicletas_cargadas = self.num_bicicletas_cargadas
        new_furgoneta.coord_destinos = [(coord[0], coord[1]) for coord in self.coord_destinos]
        new_furgoneta.num_bicicletas_descargadas_destino1 = self.num_bicicletas_descargadas_destino1
        new_furgoneta.num_bicicletas_descargadas_destino2 = self.num_bicicletas_descargadas_destino2

        return new_furgoneta

    def set_estaciones_destinos(self, destino1: dict, destino2: dict) -> None:
        if distancia_manhattan((self.origenX, self.origenY), (params.estaciones[destino1['index']].coordX , params.estaciones[destino1['index']].coordY)) \
            < distancia_manhattan((self.origenX, self.origenY), (params.estaciones[destino2['index']].coordX , params.estaciones[destino2['index']].coordY)):
            self.info_est_destino = [destino1, destino2]
            self.coord_destinos = [(params.estaciones[destino1['index']].coordX , params.estaciones[destino1['index']].coordY), \
                                    (params.estaciones[destino2['index']].coordX , params.estaciones[destino2['index']].coordY)]
        else:
            self.info_est_destino = [destino2, destino1]
            self.coord_destinos = [(params.estaciones[destino2['index']].coordX , params.estaciones[destino2['index']].coordY), \
                                    (params.estaciones[destino1['index']].coordX , params.estaciones[destino1['index']].coordY)]
    
    def set_estacion_origen(self, estacion_origen: dict) -> None:
        self.info_est_origen = estacion_origen
        self.origenX = params.estaciones[estacion_origen['index']].coordX
        self.origenY = params.estaciones[estacion_origen['index']].coordY        

    def set_num_bicicletas_cargadas(self, num_bicicletas: int):
        self.num_bicicletas_cargadas = num_bicicletas

    def calcular_bicicletas_carga(self) -> int:
            num_bicicletas_cargadas = min(30, self.info_est_origen['disp'] if self.info_est_origen['disp'] > 0 else 0, \
                        abs(self.info_est_destino[0]['dif']) if self.info_est_destino[0]['dif'] < 0 else 0 \
                        + abs(self.info_est_destino[1]['dif']) if self.info_est_destino[1]['dif'] < 0 else 0)
            
            return num_bicicletas_cargadas

    def realizar_ruta(self) -> None:
        self.__cargar_bicicletas(self.num_bicicletas_cargadas)
        self.__descargar_bicicletas(estacion_descarga1=self.info_est_destino[0], estacion_descarga2=self.info_est_destino[1])
    
    def __cargar_bicicletas(self, num_bicicletas_carga: Union[int, None] = None) -> None:
        self.num_bicicletas_cargadas = num_bicicletas_carga
        self.info_est_origen['disp'] -= num_bicicletas_carga
        self.info_est_origen['dif'] -= num_bicicletas_carga

    def __descargar_bicicletas(self, estacion_descarga1: dict, estacion_descarga2: dict) -> None:
        self.num_bicicletas_descargadas_destino1 = min(self.num_bicicletas_cargadas, abs(estacion_descarga1['dif']) if estacion_descarga1['dif'] < 0 else 0)
        self.num_bicicletas_descargadas_destino2 = self.num_bicicletas_cargadas - self.num_bicicletas_descargadas_destino1
        estacion_descarga1['disp'] += self.num_bicicletas_descargadas_destino1
        estacion_descarga2['disp'] += self.num_bicicletas_descargadas_destino2 
        estacion_descarga1['dif'] += self.num_bicicletas_descargadas_destino1
        estacion_descarga2['dif'] += self.num_bicicletas_descargadas_destino2
    
    def calcular_coste_ruta(self) -> float:
        nb_trayecto1 = self.num_bicicletas_cargadas
        nb_trayecto2 = self.num_bicicletas_descargadas_destino2
        
        km_trayecto1 = distancia_manhattan((self.origenX, self.origenY), self.coord_destinos[0]) / 1000 # Redondeamos a 5 decimales para evitar problemas
        km_trayecto2 = distancia_manhattan(self.coord_destinos[0], self.coord_destinos[1]) / 1000 # Redondeamos a 5 decimales para evitar problemas
        
        coste_trayecto1 = ((nb_trayecto1 + 9) // 10) * km_trayecto1
        coste_trayecto2 = ((nb_trayecto2 + 9) // 10) * km_trayecto2
    
        return coste_trayecto1 + coste_trayecto2

    def __eq__(self, other: 'Furgoneta') -> bool:
        # Una furgoneta es igual a otra si tienen el mismo origen (ya que no puede haber dos furgonetas en la misma estación de carga inicial)
        return isinstance(other, Furgoneta) and \
            self.origenX == other.origenX and \
                self.origenY == other.origenY
    """