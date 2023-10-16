from furgoneta_bicing import Furgoneta
from parameters_bicing import params
from functions_bicing import distancia_manhattan
from typing import Generator
from operators_bicing import BicingOperator, CambiarEstacionCarga, CambiarEstacionDescarga, IntercambiarEstacionDescarga, CambiarNumeroBicisCarga, IntercambiarEstacionCarga

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

    def realizar_ruta_furgoneta(self, id_furgoneta: int):
        furgoneta: Furgoneta = self.lista_furgonetas[id_furgoneta]
        furgoneta.realizar_ruta()
        cambios: list[dict] = [furgoneta.info_est_origen] + furgoneta.info_est_destino
        for est in cambios:
            self.info_estaciones[est['index']] = {key: value for key, value in est.items()}


    def heuristic(self) -> float:
        return self.calcular_balance()
        
    def generate_actions(self) -> Generator:
        # Generate all the possible actions for the current state of the problem:
        estaciones_origen = set()
        for furgoneta in self.lista_furgonetas:
            estaciones_origen.add(furgoneta.info_est_origen['index'])

        for furgoneta in self.lista_furgonetas:
              # CambiarEsigetacionCarga
            for est in self.info_estaciones:
                if est['index'] not in estaciones_origen:
                    yield CambiarEstacionCarga(furgoneta, est)
            
            """# IntercambiarEstacionCarga
            for furgoneta2 in self.lista_furgonetas:
                if furgoneta != furgoneta2:
                    yield IntercambiarEstacionCarga(furgoneta1=furgoneta, furgoneta2=furgoneta2)

            # CambiarEstacionDescarga
            for est in self.info_estaciones:
                for pos_est in {0, 1}:
                    # No hacemos comprobación de que la nueva estación de descarga sea distinta a la anterior porque consideramos 
                    # que se puede hacer un movimiento a la misma estación de descarga (como quedarse quieto)
                    yield CambiarEstacionDescarga(furgoneta, est, pos_est)
            
            # IntercambiarEstacionDescarga
            for furgoneta2 in self.lista_furgonetas:
                if furgoneta != furgoneta2:
                    for pos_estacion1 in {0, 1}:
                        for pos_estacion2 in {0, 1}:
                            if furgoneta.coord_destinos[pos_estacion1] != furgoneta2.coord_destinos[pos_estacion2]:
                                yield IntercambiarEstacionDescarga(furgoneta, furgoneta2, pos_estacion1, pos_estacion2)"""

            """# CambiarNumeroBicisCarga
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
                        
                    for num_bicicletas_carga in range(0, num_max + 1):
                        yield CambiarNumeroBicisCarga(furgoneta, furgoneta.info_est_origen, num_bicicletas_carga=0)

                # Caso 2 movimientos "reales"
                else:
                    dif_destino1 = furgoneta.info_est_destino[0]['dif']
                    dif_destino2 = furgoneta.info_est_destino[1]['dif']
                    num_max = min(30, \
                                    furgoneta.info_est_origen['disp'] if furgoneta.info_est_origen['disp'] > 0 else 0, \
                                        abs(dif_destino1) if dif_destino1 < 0 else 0 + abs(dif_destino2) if dif_destino2 < 0 else 0)

                    for num_bicicletas_carga in range(0, num_max + 1):
                        yield CambiarNumeroBicisCarga(furgoneta, furgoneta.info_est_origen, num_bicicletas_carga)"""
    
    def apply_action(self, action: BicingOperator) -> 'EstadoBicing':
        new_state: EstadoBicing = self.copy()
        if isinstance(action, CambiarEstacionCarga):
            furgoneta = new_state.lista_furgonetas[action.id_furgoneta]
            new_estacion = new_state.info_estaciones[action.id_est]
            furgoneta.set_estacion_origen(new_estacion)
            num_bicicletas_cargadas = min(30, furgoneta.info_est_origen['disp'] if furgoneta.info_est_origen['disp'] > 0 else 0, \
                                           abs(furgoneta.info_est_destino[0]['dif']) if furgoneta.info_est_destino[0]['dif'] < 0 else 0 \
                                            + abs(furgoneta.info_est_destino[1]['dif']) if furgoneta.info_est_destino[1]['dif'] < 0 else 0)
            furgoneta.set_num_bicicletas_cargadas(num_bicicletas_cargadas)
            
            self.realizar_ruta_furgoneta(action.id_furgoneta)
        
        elif isinstance(action, IntercambiarEstacionCarga):
            furgoneta1 = new_state.lista_furgonetas[action.id_furgoneta1]
            furgoneta2 = new_state.lista_furgonetas[action.id_furgoneta2]
            copia_estacion_origen1 = {key: value for key, value in furgoneta1.info_est_origen.items()}
            copia_estacion_origen2 = {key: value for key, value in furgoneta2.info_est_origen.items()}
            furgoneta1.set_estacion_origen(copia_estacion_origen2)
            furgoneta2.set_estacion_origen(copia_estacion_origen1)
            num_bicicletas_cargadas1 = furgoneta1.calcular_bicicletas_carga()
            num_bicicletas_cargadas2 = furgoneta2.calcular_bicicletas_carga()

            furgoneta1.set_num_bicicletas_cargadas(num_bicicletas_cargadas1)
            furgoneta2.set_num_bicicletas_cargadas(num_bicicletas_cargadas2)
            
            self.realizar_ruta_furgoneta(furgoneta1.id)
            self.realizar_ruta_furgoneta(furgoneta2.id)
        
        elif isinstance(action, CambiarEstacionDescarga):
            furgoneta = new_state.lista_furgonetas[action.id_furgoneta]
            new_estacion = new_state.info_estaciones[action.id_est]
            if action.pos_est == 0:
                furgoneta.set_estaciones_destinos(new_estacion, furgoneta.info_est_destino[1])
            else:
                furgoneta.set_estaciones_destinos(furgoneta.info_est_destino[0], new_estacion)
            
            self.realizar_ruta_furgoneta(furgoneta.id)
    
        if isinstance(action, IntercambiarEstacionDescarga):
            furgoneta1 = new_state.lista_furgonetas[action.id_furgoneta1]
            furgoneta2 = new_state.lista_furgonetas[action.id_furgoneta2]
            copia_estacion_destino1 = new_state.info_estaciones[action.id_furgoneta1]
            copia_estacion_destino2 = new_state.info_estaciones[action.id_furgoneta2]   

            if action.pos_est1 == 0:
                if action.pos_est2 == 0:
                    furgoneta1.set_estaciones_destinos(copia_estacion_destino2, furgoneta1.info_est_destino[1])
                    furgoneta2.set_estaciones_destinos(copia_estacion_destino1, furgoneta2.info_est_destino[1])
                else:
                    furgoneta1.set_estaciones_destinos(copia_estacion_destino2, furgoneta1.info_est_destino[1])
                    furgoneta2.set_estaciones_destinos(furgoneta2.info_est_destino[0], copia_estacion_destino1)
            else:
                if action.pos_est2 == 0:
                    furgoneta1.set_estaciones_destinos(furgoneta1.info_est_destino[0], copia_estacion_destino2)
                    furgoneta2.set_estaciones_destinos(copia_estacion_destino1, furgoneta2.info_est_destino[1])
                else:
                    furgoneta1.set_estaciones_destinos(furgoneta1.info_est_destino[0], copia_estacion_destino2)
                    furgoneta2.set_estaciones_destinos(furgoneta2.info_est_destino[0], copia_estacion_destino1)

            self.realizar_ruta_furgoneta(furgoneta1.id)
            self.realizar_ruta_furgoneta(furgoneta2.id)

        """elif isinstance(action, CambiarNumeroBicisCarga):
            furgoneta = new_state.lista_furgonetas[action.id_furgoneta]
            furgoneta.set_num_bicicletas_cargadas(action.num_bicicletas_carga)"""

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