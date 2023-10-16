from furgoneta_bicing import Furgoneta
from parameters_bicing import params

class BicingOperator(object):
    pass


class CambiarEstacionCarga(BicingOperator):
    def __init__(self, furgoneta: Furgoneta, estacion: dict) -> None:
        self.id_furgoneta = furgoneta.id
        self.id_est = estacion['index']

    def __repr__(self) -> str:
        return f"CambiarEstacionCarga(furgoneta={self.id_furgoneta}, coord_estacion={(params.estaciones[self.info_est['index']].coordX, params.estaciones[self.info_est['index']].coordY)})"
  
class IntercambiarEstacionCarga(BicingOperator):
    def __init__(self, furgoneta1: Furgoneta, furgoneta2: Furgoneta) -> None:
        self.id_furgoneta1 = furgoneta1.id
        self.id_furgoneta2 = furgoneta2.id

    def __repr__(self) -> str:
        return f"IntercambiarEstacionCarga(furgoneta1={self.id_furgoneta1}, furgoneta2={self.id_furgoneta2})"


class CambiarEstacionDescarga(BicingOperator):
    def __init__(self, furgoneta: Furgoneta, estacion: dict, pos_est: int) -> None:
        assert pos_est in {0,1}, "n_estacion debe ser 0 o 1"
        self.id_est = estacion['index']
        self.id_furgoneta = furgoneta.id
        self.pos_est = pos_est

    def __repr__(self) -> str:
        return f"CambiarEstacionDescarga(furgoneta={self.furgoneta.id}, coord_estacion={(params.estaciones[self.info_est['index']].coordX, params.estaciones[self.info_est['index']].coordY)}, n_estacion={self.id_est})"


class IntercambiarEstacionDescarga(BicingOperator):
    def __init__(self, furgoneta1: Furgoneta, furgoneta2: Furgoneta, pos_est1: int, pos_est2: int) -> None:
        assert pos_est1 in {0, 1} and pos_est2 in {0, 1}, "n_estacion1 y n_estacion2 deben ser 0 o 1"
        self.id_furgoneta1 = furgoneta1.id
        self.id_furgoneta2 = furgoneta2.id
        self.pos_est1 = pos_est1
        self.pos_est2 = pos_est2

    def __repr__(self) -> str:
        return f"IntercambiarEstacionDescarga(furgoneta1={self.furgoneta1.id}, furgoneta2={self.furgoneta2.id}, id_est1={self.id_est1}, id_est2={self.id_est2})"


class CambiarNumeroBicisCarga(BicingOperator):
    def __init__(self, furgoneta: Furgoneta, estacion_carga: dict, num_bicicletas_carga: int) -> None:
        self.id_furgoneta = furgoneta.id
        self.id_est_carga = estacion_carga['index']
        self.num_bicicletas_carga = num_bicicletas_carga

    def __repr__(self) -> str:
        return f"CambiarNumeroBicisCarga(furgoneta={self.id_furgoneta}, coord_estacion_carga={(params.estaciones[self.id_est_carga['index']].coordX, params.estaciones[self.id_est_carga['index']].coordY)}, num_bicicletas_carga={self.num_bicicletas_carga})"

