class Parameters:
	def __init__(self, n_estaciones: int, n_bicicletas: int, n_furgonetas: int, seed: int):
		self.n_estaciones = n_estaciones
		self.n_bicicletas = n_bicicletas
		self.n_furgonetas = n_furgonetas
		self.seed = seed

	def __repr__(self) -> str:
		return f"Params(n_estaciones={self.n_estaciones}, n_bicicletas={self.n_bicicletas}, n_furgonetas={self.n_furgonetas}, seed={self.seed})"
	

def distancia_manhattan(coord1: tuple, coord2: tuple):
    """
    Calcula la distancia de Manhattan entre dos puntos.
    """
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])