from estaciones_bicing import Estaciones, Estacion
from furgoneta_bicing import Furgoneta

class EstadoBicing(object):
    def __init__(self, lista_estaciones: list[Estacion], lista_furgonetas: list[Furgoneta]):
        self.lista_estaciones = lista_estaciones
        self.lista_furgonetas = lista_furgonetas
        
    def __eq__(self, other):
        return isinstance(other, EstadoBicing) and self.lista_estaciones == other.lista_estaciones and self.lista_furgonetas == other.lista_furgonetas

    def __lt__(self, other):
        return hash(self) < hash(other)
    
    def __hash__(self):
        return hash((self.lista_estaciones, self.lista_furgonetas))
    
    def __repr__(self):
        str_furgonetas = ""
        count = 1
        for furgoneta in self.lista_furgonetas:
            str_furgonetas += f"Furgoneta {count}: {furgoneta.__repr__()}\n"
            count += 1
        
        f"{self.lista_estaciones.__repr__()}\n\n---------- FURGONETAS ----------\n{str_furgonetas}"
    
    def calcular_balance_rutas(self) -> int:
        coste_total = 0
        for furgoneta in self.lista_furgonetas:
            coste_total -= furgoneta.calcular_coste_ruta()
        
        return coste_total

    def calcular_beneficios_estaciones(self) -> int:
        beneficios_estaciones = 0
        for furgoneta in self.lista_furgonetas:
            beneficios_estaciones += furgoneta.beneficio_descargas
        
        return beneficios_estaciones
    
    def calcular_perdidas_estaciones(self) -> int:
        demanda_total = 0
        for estacion in self.lista_estaciones:
            demanda_total -= estacion.demanda
            
        return demanda_total
    
    def calcular_balance(self):
        return self.calcular_perdidas_estaciones() + self.calcular_beneficios_estaciones() - self.calcular_balance_rutas()

    def heuristic(self):
        # GANANCIAS
            #Nos paga un euro por cada bicicleta que transportemos que haga que el número de bicicletas de una estación se acerque a la demanda. 
            #Es decir, nos paga por las bicicletas adicionales que haya en una estación respecto a la previsión de cuantas bicicletas habrá en la estación en la
            #hora siguiente, siempre que no superen la demanda prevista."
        # PERDIDAS
            #nos cobrará un euro por cada bicicleta que transportemos que aleje a una estación de su previsión. 
            #Es decir, nos descontarán por las bicicletas que movamos que hagan que una estación quede por debajo de la demanda prevista.
        # COSTE POR KM
            # nb es el número de bicicletas que transportamos en una furgoneta, el coste en euros por kilómetro recorrido es ((nb + 9) div 10), donde div es la división entera.
        pass

    def generate_actions(self):
        pass

    def apply_action(self, action):
        pass