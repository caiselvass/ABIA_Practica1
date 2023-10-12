from estaciones_bicing import Estacion
from furgoneta_bicing import Furgoneta
from operators_bicing import BicingOperator, CambiarEstacionCarga, CambiarEstacionDescarga, IntercambiarEstacionDescarga, CambiarNumeroBicisCarga
from typing import Generator

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
        return self.calcular_balance()
        
        # GANANCIAS
            #Nos paga un euro por cada bicicleta que transportemos que haga que el número de bicicletas de una estación se acerque a la demanda. 
            #Es decir, nos paga por las bicicletas adicionales que haya en una estación respecto a la previsión de cuantas bicicletas habrá en la estación en la
            #hora siguiente, siempre que no superen la demanda prevista."
        # PERDIDAS
            #nos cobrará un euro por cada bicicleta que transportemos que aleje a una estación de su previsión.  
            #Es decir, nos descontarán por las bicicletas que movamos que hagan que una estación quede por debajo de la demanda prevista.
        # COSTE POR KM
            # nb es el número de bicicletas que transportamos en una furgoneta, el coste en euros por kilómetro recorrido es ((nb + 9) div 10), donde div es la división entera.


    def generate_actions(self) -> Generator:
        # Generate all the possible actions for the current state of the problem:
        for furgoneta in self.lista_furgonetas:
            # CambiarEstacionCarga
            for estacion in self.lista_estaciones:
                if estacion.coordX != furgoneta.origenX and estacion.coordY != furgoneta.origenY:
                    yield CambiarEstacionCarga(furgoneta, estacion)
            
            # CambiarEstacionDescarga
            for estacion in self.lista_estaciones:
                for n_estacion in {0, 1}:
                    # No hacemos comprobación de que la nueva estación de descarga sea distinta a la anterior porque consideramos 
                    # que se puede hacer un movimiento a la misma estación de descarga (como quedarse quieto)
                    yield CambiarEstacionDescarga(furgoneta, estacion, n_estacion)
            
            # IntercambiarEstacionDescarga
            for furgoneta2 in self.lista_furgonetas:
                if furgoneta != furgoneta2:
                    for n_estacion1 in {0, 1}:
                        for n_estacion2 in {0, 1}:
                            if furgoneta.coord_destinos[n_estacion1] != furgoneta2.coord_destinos[n_estacion2]:
                                yield IntercambiarEstacionDescarga(furgoneta, furgoneta2, n_estacion1, n_estacion2)
            
            # CambiarNumeroBicisCarga
            if furgoneta.estacion_origen.num_bicicletas_no_usadas > 0:
                # Comprobamos que no haya ningua estación destino igual a la de Origen, para evitar cargar bicicletas de más en ese caso
                if (furgoneta.origenX, furgoneta.origenY) == furgoneta.coord_destinos[0] == furgoneta.coord_destinos[1]:
                    yield CambiarNumeroBicisCarga(furgoneta, furgoneta.estacion_origen, num_bicicletas_carga=0)
                
                # Caso solo haremos 1 movimiento "real"
                elif (furgoneta.origenX, furgoneta.origenY) == furgoneta.coord_destinos[0]: 
                    dif_destino1 = furgoneta.estaciones_destino[1].diferencia
                    num_max = min(30, \
                                  furgoneta.estacion_origen.diferencia, \
                                    furgoneta.estacion_origen.num_bicicletas_no_usadas, \
                                        abs(dif_destino1) if dif_destino1 < 0 else 0)
                    
                    for num_bicicletas_carga in range(0, num_max + 1):
                        yield CambiarNumeroBicisCarga(furgoneta, furgoneta.estacion_origen, num_bicicletas_carga=0)

                # Caso 2 movimientos "reales"
                else:
                    dif_destino1 = furgoneta.estaciones_destino[0].diferencia
                    dif_destino2 = furgoneta.estaciones_destino[1].diferencia
                    num_max = min(30, \
                                  furgoneta.estacion_origen.diferencia, \
                                    furgoneta.estacion_origen.num_bicicletas_no_usadas, \
                                        abs(dif_destino1) if dif_destino1 < 0 else 0 + abs(dif_destino2) if dif_destino2 < 0 else 0)
                    
                    for num_bicicletas_carga in range(0, num_max + 1):
                        yield CambiarNumeroBicisCarga(furgoneta, furgoneta.estacion_origen, num_bicicletas_carga)

    def apply_action(self, action: BicingOperator) -> 'EstadoBicing':
        if isinstance(action, CambiarEstacionCarga):
            pass
        if isinstance(action, CambiarEstacionDescarga):
            pass
        if isinstance(action, IntercambiarEstacionDescarga):
            pass
        if isinstance(action, CambiarNumeroBicisCarga):
            pass