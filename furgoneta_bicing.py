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

