from estaciones_bicing import Estacion
from furgoneta_bicing import Furgoneta
from operators_bicing import BicingOperator

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
    
    def calcular_balance_rutas(self) -> int:
        balance_rutas = 0
        for furgoneta in self.lista_furgonetas:
            balance_rutas -= furgoneta.calcular_coste_ruta()
        return balance_rutas

    def calcular_balance_estaciones(self) -> int:
        # estacion.diferencia = estacion.num_bicicletas_next - estacion.demanda
        balance_estaciones = 0
        for estacion in self.lista_estaciones:
            diferencia_inicial = estacion.num_bicicletas_next - estacion.demanda      
            diferencia_final = estacion.diferencia

            if diferencia_final < 0 and diferencia_final < diferencia_inicial:
                print("\n\n", estacion)

            if diferencia_final >= 0 and diferencia_inicial <= 0:
                balance_estaciones += abs(diferencia_inicial)
            elif diferencia_final < 0:
                if diferencia_inicial >= 0:
                    balance_estaciones += diferencia_final
                else:
                    balance_estaciones += diferencia_final - diferencia_inicial
                

        return balance_estaciones
    
    def calcular_balance(self):
        return self.calcular_balance_estaciones() + self.calcular_balance_rutas()

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

    def apply_action(self, action: BicingOperator):
        pass