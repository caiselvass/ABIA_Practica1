from furgoneta_bicing import Furgoneta
from parameters_bicing import params
from functions_bicing import distancia_manhattan
from typing import Generator
from operators_bicing import BicingOperator, CambiarEstacionCarga, CambiarEstacionDescarga, IntercambiarEstacionDescarga, CambiarNumeroBicisCarga

class EstadoBicing(object):
    def __init__(self, info_estaciones: list[dict], lista_furgonetas: list[Furgoneta]) -> None:
        self.info_estaciones = info_estaciones
        self.lista_furgonetas = lista_furgonetas

    def copy(self) -> 'EstadoBicing':
        new_estado_bicing = EstadoBicing([], [])
        new_estado_bicing.info_estaciones = [estacion.copy() for estacion in self.info_estaciones]
        new_estado_bicing.lista_furgonetas = [furgoneta.copy() for furgoneta in self.lista_furgonetas]
        return new_estado_bicing
    """
    def copy(self) -> EstadoBicing:
        return EstadoBicing(self.params, self.v_p.copy(), self.free_spaces.copy())
    """

    def __eq__(self, other) -> bool:
        return isinstance(other, EstadoBicing) and self.info_estaciones == other.info_estaciones and self.lista_furgonetas == other.lista_furgonetas

    def __lt__(self, other) -> bool:
        return hash(self) < hash(other)
    
    def __hash__(self) -> int:
        return hash((self.info_estaciones, self.lista_furgonetas))
    
    def __str__(self) -> str:
        str_rutas = ""
        for furgoneta in self.lista_furgonetas:
            km_trayecto1 = distancia_manhattan((furgoneta.origenX, furgoneta.origenY), furgoneta.coord_destinos[0]) / 1000
            km_trayecto2 = distancia_manhattan(furgoneta.coord_destinos[0], furgoneta.coord_destinos[1]) / 1000
            str_rutas += f"   * Furgoneta {furgoneta.id}: Carga={(furgoneta.origenX, furgoneta.origenY)} | Descargas={[furgoneta.coord_destinos[0], furgoneta.coord_destinos[1]]} | KM={km_trayecto1 + km_trayecto2}\n"
        return f"\n\nRUTAS CALCULADAS:\n{str_rutas}"
    
    def calcular_balance_rutas(self) -> float:
        balance_rutas = 0
        for furgoneta in self.lista_furgonetas:
            balance_rutas -= furgoneta.calcular_coste_ruta()
        return balance_rutas

    def calcular_balance_estaciones(self) -> int:
        # estacion.diferencia = estacion.num_bicicletas_next - estacion.demanda
        balance_estaciones = 0
        for est in self.info_estaciones:
            diferencia_inicial = params.estaciones[est['index']].num_bicicletas_next - params.estaciones[est['index']].demanda      
            diferencia_final = est['dif']

            if diferencia_final >= 0 and diferencia_inicial <= 0:
                balance_estaciones += abs(diferencia_inicial)
            elif diferencia_final < 0:
                if diferencia_inicial >= 0:
                    balance_estaciones += diferencia_final
                else:
                    balance_estaciones += diferencia_final - diferencia_inicial
                
        return balance_estaciones
    
    def calcular_balance(self) -> float:
        return self.calcular_balance_estaciones() + self.calcular_balance_rutas()

    def heuristic(self) -> float:
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
            for est in self.info_estaciones:
                if params.estaciones[est['index']].coordX != furgoneta.origenX and params.estaciones[est['index']].coordY != furgoneta.origenY:
                    yield CambiarEstacionCarga(furgoneta, est)
            
            # CambiarEstacionDescarga
            for est in self.info_estaciones:
                for n_estacion in {0, 1}:
                    # No hacemos comprobación de que la nueva estación de descarga sea distinta a la anterior porque consideramos 
                    # que se puede hacer un movimiento a la misma estación de descarga (como quedarse quieto)
                    yield CambiarEstacionDescarga(furgoneta, est, n_estacion)
            
            # IntercambiarEstacionDescarga
            for furgoneta2 in self.lista_furgonetas:
                if furgoneta != furgoneta2:
                    for n_estacion1 in {0, 1}:
                        for n_estacion2 in {0, 1}:
                            if furgoneta.coord_destinos[n_estacion1] != furgoneta2.coord_destinos[n_estacion2]:
                                yield IntercambiarEstacionDescarga(furgoneta, furgoneta2, n_estacion1, n_estacion2)
            
            # CambiarNumeroBicisCarga
            if furgoneta.info_est_origen['disp'] > 0:
                # Comprobamos que no haya ningua estación destino igual a la de Origen, para evitar cargar bicicletas de más en ese caso
                if (furgoneta.origenX, furgoneta.origenY) == furgoneta.coord_destinos[0] == furgoneta.coord_destinos[1]:
                    yield CambiarNumeroBicisCarga(furgoneta, furgoneta.info_est_origen, num_bicicletas_carga=0)
                
                # Caso solo haremos 1 movimiento "real"
                elif (furgoneta.origenX, furgoneta.origenY) == furgoneta.coord_destinos[0]: 
                    dif_destino1 = furgoneta.info_est_destino[1]['dif']
                    num_max = min(30, \
                                  furgoneta.info_est_origen['dif'], \
                                    furgoneta.info_est_origen['disp'], \
                                        abs(dif_destino1) if dif_destino1 < 0 else 0)
                    
                    for num_bicicletas_carga in range(0, num_max + 1):
                        yield CambiarNumeroBicisCarga(furgoneta, furgoneta.info_est_origen, num_bicicletas_carga=0)

                # Caso 2 movimientos "reales"
                else:
                    dif_destino1 = furgoneta.info_est_destino[0]['dif']
                    dif_destino2 = furgoneta.info_est_destino[1]['dif']
                    num_max = min(30, \
                                  furgoneta.info_est_origen['dif'], \
                                    furgoneta.info_est_origen['disp'], \
                                        abs(dif_destino1) if dif_destino1 < 0 else 0 + abs(dif_destino2) if dif_destino2 < 0 else 0)
                    
                    for num_bicicletas_carga in range(0, num_max + 1):
                        yield CambiarNumeroBicisCarga(furgoneta, furgoneta.info_est_origen, num_bicicletas_carga)
    
    def apply_action(self, action: BicingOperator) -> 'EstadoBicing':
        new_state: EstadoBicing = self.copy()
        
        if isinstance(action, CambiarEstacionCarga):
            pass
        elif isinstance(action, CambiarEstacionDescarga):
            pass
        elif isinstance(action, IntercambiarEstacionDescarga):
            pass
        elif isinstance(action, CambiarNumeroBicisCarga):
            pass
        return new_state

    def print_state(self, inicial: bool = False) -> str:
        str_balances = ""
        if inicial:
            str_balances += f"\n{'*'*35 + ' [ ESTADO INICIAL ] ' + '*'*35}\n"
        else:
            str_balances += f"\n{'*'*35 + ' [ SOLUCIÓN FINAL ] ' + '*'*35}\n"
            
        str_balances += f"\nBALANCE RUTAS: {self.calcular_balance_rutas()}\n" + \
                    f"BALANCE ESTACIONES: {self.calcular_balance_estaciones()}\n" + \
                        f"BALANCE TOTAL: {self.calcular_balance()}"
        
        print(str_balances + self.__str__())