class MoveFurgoneta(object):
    def __init__(self, furgoneta: Furgoneta, estacion_carga: Estacion, estaciones_destino: list[Estacion] = []):
        self.furgoneta = furgoneta
        self.estacion_carga = estacion_carga
        self.estaciones_destino = estaciones_destino
    
    # def __repr__(self):
    #     str_estaciones_destino = ""
    #     for estacion in self.estaciones_destino:
    #         str_estaciones_destino += f"{estacion.__repr__()}"
    #     return f"Move furgoneta: {self.furgoneta.__repr__()}:\nEstacion carga: \nTo estaciones: {s"