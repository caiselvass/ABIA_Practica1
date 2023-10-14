from estaciones_bicing import Estacion
from furgoneta_bicing import Furgoneta

class BicingOperator(object):
    pass


class CambiarEstacionCarga(BicingOperator):
    def __init__(self, furgoneta: Furgoneta, estacion: Estacion) -> None:
        self.furgoneta = furgoneta
        self.estacion = estacion

    def __repr__(self) -> str:
        return f"CambiarEstacionCarga(furgoneta={self.furgoneta.id}, coord_estacion={(self.estacion.coordX, self.estacion.coordY)})"
  

class CambiarEstacionDescarga(BicingOperator):
    def __init__(self, furgoneta: Furgoneta, estacion: Estacion, n_estacion: int) -> None:
        assert n_estacion in {0,1}, "n_estacion debe ser 0 o 1"
        self.estacion = estacion
        self.furgoneta = furgoneta
        self.n_estacion = n_estacion

    def __repr__(self) -> str:
        return f"CambiarEstacionDescarga(furgoneta={self.furgoneta.id}, coord_estacion={(self.estacion.coordX, self.estacion.coordY)}, n_estacion={self.n_estacion})"


class IntercambiarEstacionDescarga(BicingOperator):
    def __init__(self, furgoneta1: Furgoneta, furgoneta2: Furgoneta, n_estacion1: int, n_estacion2: int) -> None:
        assert n_estacion1 in {0, 1} and n_estacion2 in {0, 1}, "n_estacion1 y n_estacion2 deben ser 0 o 1"
        self.furgoneta1 = furgoneta1
        self.furgoneta2 = furgoneta2
        self.n_estacion1 = n_estacion1
        self.n_estacion2 = n_estacion2

    def __repr__(self) -> str:
        return f"IntercambiarEstacionDescarga(furgoneta1={self.furgoneta1.id}, furgoneta2={self.furgoneta2.id}, n_estacion1={self.n_estacion1}, n_estacion2={self.n_estacion2})"


class CambiarNumeroBicisCarga(BicingOperator):
    def __init__(self, furgoneta: Furgoneta, estacion_carga: Estacion, num_bicicletas_carga: int) -> None:
        self.furgoneta = furgoneta
        self.estacion_carga = estacion_carga
        self.num_bicicletas_carga = num_bicicletas_carga

    def __repr__(self) -> str:
        return f"CambiarNumeroBicisCarga(furgoneta={self.furgoneta.id}, coord_estacion_carga={(self.estacion_carga.coordX, self.estacion_carga.coordY)}, num_bicicletas_carga={self.num_bicicletas_carga})"

