class BicingOperator(object):
    """
    Clase abstracta para representar los operadores que realizan una única acción.
    """
    pass


class CambiarEstacionCarga(BicingOperator):
    """
    Operador que cambia la estación de carga de una furgoneta.
    """
    def __init__(self, id_furgoneta: int, id_est: int) -> None:
        self.id_furgoneta = id_furgoneta
        self.id_est = id_est


class CambiarOrdenDescarga(BicingOperator):
    """
    Operador que cambia el orden de descarga de una furgoneta.
    """
    def __init__(self, id_furgoneta: int) -> None:
        self.id_furgoneta = id_furgoneta


class IntercambiarEstacionCarga(BicingOperator):
    """
    Operador que cambia la estación de carga de dos furgonetas distintas.
    """
    def __init__(self, id_furgoneta1: int, id_furgoneta2: int) -> None:
        self.id_furgoneta1 = id_furgoneta1
        self.id_furgoneta2 = id_furgoneta2


class CambiarEstacionDescarga(BicingOperator):
    """
    Operador que cambia una estación de descarga de una furgoneta.
    """
    def __init__(self, id_furgoneta: int, id_est: dict, pos_est: int) -> None:
        assert pos_est in {0,1}, "pos_est debe ser 0 o 1"
        self.id_furgoneta = id_furgoneta
        self.id_est = id_est
        self.pos_est = pos_est


class IntercambiarEstacionDescarga(BicingOperator):
    """
    Operador que Intercambia una estación de descarga de una furgoneta con el otra esta
    """
    def __init__(self, id_furgoneta1: int, id_furgoneta2: int, id_est1: int, id_est2: int, pos_est1: int, pos_est2: int) -> None:
        assert pos_est1 in {0, 1} and pos_est2 in {0, 1}, "pos_est1 y pos_est2 deben ser 0 o 1"
        self.id_furgoneta1 = id_furgoneta1
        self.id_furgoneta2 = id_furgoneta2
        self.id_est1 = id_est1
        self.id_est2 = id_est2
        self.pos_est1 = pos_est1
        self.pos_est2 = pos_est2



class ReasignarFurgonetaRandom(BicingOperator):
    """
    Operador que cambia todas las estaciones de carga y descarga de una furgoneta.
    """
    def __init__(self, id_furgoneta: int, id_est_origen: int, id_est_dest1: int, id_est_dest2) -> None:
        self.id_furgoneta = id_furgoneta
        self.id_est_origen = id_est_origen
        self.id_est_dest1 = id_est_dest1
        self.id_est_dest2 = id_est_dest2


class ReasignarFurgonetaInformado(BicingOperator):
    """
    Operador que cambia todas las estaciones de carga y descarga de una furgoneta.
    """
    def __init__(self, id_furgoneta: int, id_est_origen: int, id_est_dest1: int, id_est_dest2) -> None:
        self.id_furgoneta = id_furgoneta
        self.id_est_origen = id_est_origen
        self.id_est_dest1 = id_est_dest1
        self.id_est_dest2 = id_est_dest2


class ReducirNumeroBicicletasCarga(BicingOperator):
    """
    Operador que reduce el número de bicicletas de una estación de carga.
    """
    def __init__(self, id_furgoneta: int, reducir_bicicletas_carga: int) -> None:
        self.id_furgoneta = id_furgoneta
        self.reducir_bicicletas_carga = reducir_bicicletas_carga