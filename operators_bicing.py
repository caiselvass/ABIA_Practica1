from furgoneta_bicing import Furgoneta
from parameters_bicing import params

class BicingOperator(object):
    pass


class CambiarEstacionCarga(BicingOperator):
    def __init__(self, furgoneta: Furgoneta, estacion: dict) -> None:
        self.furgoneta = furgoneta
        self.info_est = estacion

    def __repr__(self) -> str:
        return f"CambiarEstacionCarga(furgoneta={self.furgoneta.id}, coord_estacion={(params.estaciones[self.info_est['index']].coordX, params.estaciones[self.info_est['index']].coordY)})"
  

class CambiarEstacionDescarga(BicingOperator):
    def __init__(self, furgoneta: Furgoneta, estacion: dict, id_est: int) -> None:
        assert id_est in {0,1}, "n_estacion debe ser 0 o 1"
        self.info_est = estacion
        self.furgoneta = furgoneta
        self.id_est = id_est

    def __repr__(self) -> str:
        return f"CambiarEstacionDescarga(furgoneta={self.furgoneta.id}, coord_estacion={(params.estaciones[self.info_est['index']].coordX, params.estaciones[self.info_est['index']].coordY)}, n_estacion={self.id_est})"


class IntercambiarEstacionDescarga(BicingOperator):
    def __init__(self, furgoneta1: Furgoneta, furgoneta2: Furgoneta, id_est1: int, id_est2: int) -> None:
        assert id_est1 in {0, 1} and id_est2 in {0, 1}, "n_estacion1 y n_estacion2 deben ser 0 o 1"
        self.furgoneta1 = furgoneta1
        self.furgoneta2 = furgoneta2
        self.id_est1 = id_est1
        self.id_est2 = id_est2

    def __repr__(self) -> str:
        return f"IntercambiarEstacionDescarga(furgoneta1={self.furgoneta1.id}, furgoneta2={self.furgoneta2.id}, n_estacion1={self.id_est1}, n_estacion2={self.id_est2})"


class CambiarNumeroBicisCarga(BicingOperator):
    def __init__(self, furgoneta: Furgoneta, estacion_carga: dict, num_bicicletas_carga: int) -> None:
        self.furgoneta = furgoneta
        self.info_est_carga = estacion_carga
        self.num_bicicletas_carga = num_bicicletas_carga

    def __repr__(self) -> str:
        return f"CambiarNumeroBicisCarga(furgoneta={self.furgoneta.id}, coord_estacion_carga={(params.estaciones[self.info_est_carga['index']].coordX, params.estaciones[self.info_est_carga['index']].coordY)}, num_bicicletas_carga={self.num_bicicletas_carga})"

