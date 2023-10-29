from abia_bicing import Estaciones, Estacion

class Parameters:
	def __init__(self, n_estaciones: int, n_bicicletas: int, n_furgonetas: int, seed: int, coste_transporte: bool = True, operadores_modificables: set = {}) -> None:
		assert n_estaciones > n_furgonetas, "El número de estaciones debe ser mayor que el número de furgonetas"
		self.coste_transporte = coste_transporte
		self.operadores_modificables = operadores_modificables
		self.seed = seed
		self.n_estaciones = n_estaciones
		self.n_furgonetas = n_furgonetas
		self.n_bicicletas = n_bicicletas
		
		self.actualizar_estaciones(n_estaciones=n_estaciones, n_furgonetas=n_furgonetas, n_bicicletas=n_bicicletas)

	def actualizar_estaciones(self, \
								n_estaciones: int, \
									n_furgonetas: int, \
										 n_bicicletas: int) -> None:
		self.n_estaciones = n_estaciones
		self.n_furgonetas = n_furgonetas
		self.n_bicicletas = n_bicicletas
		self.estaciones = Estaciones(num_estaciones=n_estaciones, num_bicicletas=n_bicicletas, semilla=self.seed).lista_estaciones

	def actualizar_semilla(self, semilla: int) -> None:
		self.seed = semilla
		self.actualizar_estaciones(n_estaciones=self.n_estaciones, n_furgonetas=self.n_furgonetas, n_bicicletas=self.n_bicicletas)

params = Parameters(n_estaciones=25, \
					n_bicicletas=1250, \
						n_furgonetas=5, \
							seed=42, \
								coste_transporte=False, \
									operadores_modificables={'CambiarOrdenDescarga', \
								  'IntercambiarEstacionDescarga', \
									'IntercambiarEstacionCarga', \
										'ReasignarFurgonetaInformado'})


