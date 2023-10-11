from estaciones_bicing import Estacion
from furgoneta_bicing import Furgoneta

class BicingOperator(object):
    pass
class MoveFurgoneta(BicingOperator):
    def __init__(self, furgoneta: Furgoneta, estacion_carga: Estacion, estaciones_destino: list[Estacion] = []):
        self.furgoneta = furgoneta
        self.estacion_carga = estacion_carga
        self.estaciones_destino = estaciones_destino

    def __repr__(self) -> str:
        return f"Move furgoneta {self.furgoneta} from {self.estacion_carga} to {self.estaciones_destino}"

class CargarBicicletas(BicingOperator):
    def __init__(self, furgoneta: Furgoneta):

        
class DescargarBicicletas(BicingOperator):
    def __init__(self, furgoneta: Furgoneta, estacion: Estacion, n_bicicletas_descarga):


class Distribute_Bicicletas(BicingOperator):
    pass

class Swap_Movement(BicingOperator):
    pass


    
    # def __repr__(self):
    #     str_estaciones_destino = ""
    #     for estacion in self.estaciones_destino:
    #         str_estaciones_destino += f"{estacion.__repr__()}"
    #     return f"Move furgoneta: {self.furgoneta.__repr__()}:\nEstacion carga: \nTo estaciones: {s"