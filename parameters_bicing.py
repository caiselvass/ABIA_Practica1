from abia_bicing import Estaciones, Estacion

class Parameters:
	def __init__(self, n_estaciones: int, n_bicicletas: int, n_furgonetas: int, seed: int, coste_transporte: bool = True, operadores_modificables: set = {}) -> None:
		assert n_estaciones > n_furgonetas, "El número de estaciones debe ser mayor que el número de furgonetas"
		self.n_estaciones = n_estaciones
		self.n_bicicletas = n_bicicletas
		self.n_furgonetas = n_furgonetas
		self.coste_transporte = coste_transporte
		self.seed = seed
		self.estaciones: list[Estacion] = Estaciones(num_estaciones=n_estaciones, num_bicicletas=n_bicicletas, semilla=seed).lista_estaciones
		self.operadores_modificables = operadores_modificables

	def __repr__(self) -> str:
		return f"Params(n_estaciones={self.n_estaciones}, n_bicicletas={self.n_bicicletas}, n_furgonetas={self.n_furgonetas}, seed={self.seed})"

params = Parameters(n_estaciones=25, \
					n_bicicletas=1250, \
						n_furgonetas=5, \
							seed=42, \
								coste_transporte=False, \
									operadores_modificables={'CambiarOrdenDescarga', \
								  'IntercambiarEstacionDescarga', \
									'IntercambiarEstacionCarga', \
										'ReasignarFurgonetaInformado'})


