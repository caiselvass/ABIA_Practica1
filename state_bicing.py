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
        # Reseteamos los valores para no arrastrar los cambios de los estados anteriores
        new_info_estaciones: list[dict] = [{'index': index, \
                                    'dif': est.num_bicicletas_next - est.demanda, \
                                    'disp': est.num_bicicletas_no_usadas} \
                                        for index, est in enumerate(params.estaciones)]
        new_lista_furgonetas: list = [furgoneta.copy() for furgoneta in self.lista_furgonetas]
            
        for furgoneta in new_lista_furgonetas:
            furgoneta.info_est_origen = new_info_estaciones[furgoneta.info_est_origen['index']]
            furgoneta.info_est_destino = [new_info_estaciones[est['index']] for est in furgoneta.info_est_destino]

        return EstadoBicing(info_estaciones=new_info_estaciones, lista_furgonetas=new_lista_furgonetas)


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
            str_rutas += f"   * F {furgoneta.id}: Carga=[Coord={(furgoneta.origenX, furgoneta.origenY)}, num={furgoneta.num_bicicletas_cargadas}] | Desc1=[Coords={furgoneta.coord_destinos[0]}, num={furgoneta.num_bicicletas_descargadas_destino1}] | Desc2=[Coord={furgoneta.coord_destinos[1]}, num={furgoneta.num_bicicletas_descargadas_destino2}] | KM=({km_trayecto1})+({km_trayecto2})={km_trayecto1+km_trayecto2} ({-furgoneta.calcular_coste_ruta()}€)\n"

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
        
    def generate_actions(self) -> Generator:
        # Generate all the possible actions for the current state of the problem:
        for furgoneta in self.lista_furgonetas:
            for est in self.info_estaciones:
                if params.estaciones[est['index']].coordX != furgoneta.origenX and params.estaciones[est['index']].coordY != furgoneta.origenY:
                    yield CambiarEstacionCarga(furgoneta, est)
            
            # CambiarEstacionDescarga
            for est in self.info_estaciones:
                for id_estacion in {0, 1}:
                    # No hacemos comprobación de que la nueva estación de descarga sea distinta a la anterior porque consideramos 
                    # que se puede hacer un movimiento a la misma estación de descarga (como quedarse quieto)
                    yield CambiarEstacionDescarga(furgoneta, est, id_estacion)
            
            # IntercambiarEstacionDescarga
            for furgoneta2 in self.lista_furgonetas:
                if furgoneta != furgoneta2:
                    for id_estacion1 in {0, 1}:
                        for id_estacion2 in {0, 1}:
                            if furgoneta.coord_destinos[id_estacion1] != furgoneta2.coord_destinos[id_estacion2]:
                                yield IntercambiarEstacionDescarga(furgoneta, furgoneta2, id_estacion1, id_estacion2)

            # CambiarNumeroBicisCarga
            if furgoneta.info_est_origen['disp'] > 0:
                # Comprobamos que no haya ningua estación destino igual a la de Origen, para evitar cargar bicicletas de más en ese caso
                if (furgoneta.origenX, furgoneta.origenY) == furgoneta.coord_destinos[0] == furgoneta.coord_destinos[1]:
                    yield CambiarNumeroBicisCarga(furgoneta, furgoneta.info_est_origen, num_bicicletas_carga=0)
                
                # Caso solo haremos 1 movimiento "real"
                elif (furgoneta.origenX, furgoneta.origenY) in {furgoneta.coord_destinos[0], furgoneta.coord_destinos[1]} and furgoneta.coord_destinos[0] != furgoneta.coord_destinos[1]: 
                    if (furgoneta.origenX, furgoneta.origenY) == furgoneta.coord_destinos[0]:
                        dif_destino1 = furgoneta.info_est_destino[1]['dif']
                    else:
                        dif_destino1 = furgoneta.info_est_destino[0]['dif']
                    
                    num_max = min(30, \
                                    furgoneta.info_est_origen['disp'] if furgoneta.info_est_origen['disp'] > 0 else 0, \
                                        abs(dif_destino1) if dif_destino1 < 0 else 0)
                    if num_max < 0:
                        num_max = 0
                        
                    for num_bicicletas_carga in range(0, num_max + 1):
                        yield CambiarNumeroBicisCarga(furgoneta, furgoneta.info_est_origen, num_bicicletas_carga=0)

                # Caso 2 movimientos "reales"
                else:
                    dif_destino1 = furgoneta.info_est_destino[0]['dif']
                    dif_destino2 = furgoneta.info_est_destino[1]['dif']
                    num_max = min(30, \
                                    furgoneta.info_est_origen['disp'] if furgoneta.info_est_origen['disp'] > 0 else 0, \
                                        abs(dif_destino1) if dif_destino1 < 0 else 0 + abs(dif_destino2) if dif_destino2 < 0 else 0)
                    if num_max < 0:
                        num_max = 0

                    for num_bicicletas_carga in range(0, num_max + 1):
                        yield CambiarNumeroBicisCarga(furgoneta, furgoneta.info_est_origen, num_bicicletas_carga)
    
    def apply_action(self, action: BicingOperator) -> 'EstadoBicing':
        new_state: EstadoBicing = self.copy()

        if isinstance(action, CambiarEstacionCarga):
            furgoneta = new_state.lista_furgonetas[action.furgoneta.id]
            new_estacion = {key: value for key, value in action.info_est.items()}
            furgoneta.set_estacion_origen(new_estacion)
            num_bicicletas_cargadas = min(30, furgoneta.info_est_origen['disp'], \
                                           abs(furgoneta.info_est_destino[0]['dif']) if furgoneta.info_est_destino[0]['dif'] < 0 else 0 \
                                            + abs(furgoneta.info_est_destino[1]['dif']) if furgoneta.info_est_destino[1]['dif'] < 0 else 0)
            if num_bicicletas_cargadas < 0:
                num_bicicletas_cargadas = 0

            furgoneta.set_num_bicicletas_cargadas(num_bicicletas_cargadas)
            furgoneta.realizar_ruta()
        
        elif isinstance(action, CambiarEstacionDescarga):
            furgoneta = new_state.lista_furgonetas[action.furgoneta.id]
            new_estacion = {key: value for key, value in action.info_est.items()}
            if action.id_est == 0:
                furgoneta.set_estaciones_destinos(new_estacion, furgoneta.info_est_destino[1])
            else:
                furgoneta.set_estaciones_destinos(furgoneta.info_est_destino[0], new_estacion)
            furgoneta.realizar_ruta()
    
        if isinstance(action, IntercambiarEstacionDescarga):
            furgoneta1 = new_state.lista_furgonetas[action.furgoneta1.id]
            furgoneta2 = new_state.lista_furgonetas[action.furgoneta2.id]
            copia_estacion_destino1 = {key: value for key, value in furgoneta1.info_est_destino[action.id_est1].items()}
            copia_estacion_destino2 = {key: value for key, value in furgoneta2.info_est_destino[action.id_est2].items()}

            if action.id_est1 == 0:
                if action.id_est2 == 0:
                    furgoneta1.set_estaciones_destinos(copia_estacion_destino2, furgoneta1.info_est_destino[1])
                    furgoneta2.set_estaciones_destinos(copia_estacion_destino1, furgoneta2.info_est_destino[1])
                else:
                    furgoneta1.set_estaciones_destinos(copia_estacion_destino2, furgoneta1.info_est_destino[1])
                    furgoneta2.set_estaciones_destinos(furgoneta2.info_est_destino[0], copia_estacion_destino1)
            else:
                if action.id_est2 == 0:
                    furgoneta1.set_estaciones_destinos(furgoneta1.info_est_destino[0], copia_estacion_destino2)
                    furgoneta2.set_estaciones_destinos(copia_estacion_destino1, furgoneta2.info_est_destino[1])
                else:
                    furgoneta1.set_estaciones_destinos(furgoneta1.info_est_destino[0], copia_estacion_destino2)
                    furgoneta2.set_estaciones_destinos(furgoneta2.info_est_destino[0], copia_estacion_destino1)

        elif isinstance(action, CambiarNumeroBicisCarga):
            furgoneta = new_state.lista_furgonetas[action.furgoneta.id]
            furgoneta.set_num_bicicletas_cargadas(action.num_bicicletas_carga)
            furgoneta.realizar_ruta()

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