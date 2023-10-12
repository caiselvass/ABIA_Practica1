from estaciones_bicing import Estacion
from furgoneta_bicing import Furgoneta

class BicingOperator(object):
    pass

class CargarBicicletas(BicingOperator):
    def __init__(self, furgoneta: 'Furgoneta', estacion: 'Estacion', n_bicicletas_carga: int):
        self.furgoneta = furgoneta
        self.estacion = estacion
        self.n_bicicletas_carga = n_bicicletas_carga
    
    def __repr__(self) -> str:
        return f"Cargar {self.n_bicicletas_carga} bicis a {self.furgoneta}"


class DescargarBicicletas(BicingOperator):
    def __init__(self, furgoneta: Furgoneta, estacion: Estacion, n_bicicletas_descarga: int):
        self.furgoneta = furgoneta
        self.estacion = estacion
        self.n_bicicletas_descarga = n_bicicletas_descarga
    
    def __repr__(self) -> str:
        return f"Descargar {self.n_bicicletas_descarga} bicicletas {self.furgoneta}"


class Distribute_Bicicletas(BicingOperator):
    def __init__(self, furgoneta: Furgoneta, estaciones: list[Estacion], bicicletas_por_estacion: list[int]):
        self.furgoneta = furgoneta
        self.estaciones = estaciones
        self.bicicletas_por_estacion = bicicletas_por_estacion
    
    def __repr__(self) -> str:
        return f"Distribuir bicicletas ({self.bicicletas_por_estacion}) de {self.furgoneta}"

class Swap_Movement(BicingOperator):
    def __init__(self, furgoneta1: Furgoneta, furgoneta2: Furgoneta, bicicletas_intercambio: int):
        self.furgoneta1 = furgoneta1
        self.furgoneta2 = furgoneta2
        self.bicicletas_intercambio = bicicletas_intercambio
    
    def __repr__(self) -> str:
        return f"Swap {self.bicicletas_intercambio} bicycles between van {self.furgoneta1} and van {self.furgoneta2}"
    
class CambiarEstacionCarga(BicingOperator):
    def __init__(self):
        pass