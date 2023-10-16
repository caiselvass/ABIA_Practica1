class BicingOperator(object):
    pass


class CambiarEstacionCarga(BicingOperator):
    def __init__(self, id_furgoneta: int, id_est: int) -> None:
        self.id_furgoneta = id_furgoneta
        self.id_est = id_est


class CambiarOrdenDescarga(BicingOperator):
    def __init__(self, id_furgoneta: int) -> None:
        self.id_furgoneta = id_furgoneta


class IntercambiarEstacionCarga(BicingOperator):
    def __init__(self, id_furgoneta1: int, id_furgoneta2: int) -> None:
        self.id_furgoneta1 = id_furgoneta1
        self.id_furgoneta2 = id_furgoneta2


class CambiarEstacionDescarga(BicingOperator):
    def __init__(self, id_furgoneta: int, id_est: dict, pos_est: int) -> None:
        assert pos_est in {0,1}, "pos_est debe ser 0 o 1"
        self.id_furgoneta = id_furgoneta
        self.id_est = id_est
        self.pos_est = pos_est


class IntercambiarEstacionDescarga(BicingOperator):
    def __init__(self, id_furgoneta1: int, id_furgoneta2: int, id_est1: int, id_est2: int, pos_est1: int, pos_est2: int) -> None:
        assert pos_est1 in {0, 1} and pos_est2 in {0, 1}, "pos_est1 y pos_est2 deben ser 0 o 1"
        self.id_furgoneta1 = id_furgoneta1
        self.id_furgoneta2 = id_furgoneta2
        self.id_est1 = id_est1
        self.id_est2 = id_est2
        self.pos_est1 = pos_est1
        self.pos_est2 = pos_est2

"""
class CambiarNumeroBicisCarga(BicingOperator):
    def __init__(self, id_furgoneta: int, id_est: int, bicicletas_carga: int) -> None:
        self.id_furgoneta = id_furgoneta
        self.id_est = id_est
        self.bicicletas_carga = bicicletas_carga
"""
