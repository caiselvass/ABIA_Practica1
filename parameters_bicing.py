class Parameters:
	def __init__(self, n_estaciones: int, n_bicicletas: int, n_furgonetas: int, seed: int):
		assert n_estaciones > n_furgonetas, "El número de estaciones debe ser mayor que el número de furgonetas"
		self.n_estaciones = n_estaciones
		self.n_bicicletas = n_bicicletas
		self.n_furgonetas = n_furgonetas
		self.seed = seed

	def __repr__(self) -> str:
		return f"Params(n_estaciones={self.n_estaciones}, n_bicicletas={self.n_bicicletas}, n_furgonetas={self.n_furgonetas}, seed={self.seed})"
