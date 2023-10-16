from furgoneta_bicing import Furgoneta
from parameters_bicing import params
from functions_bicing import distancia_manhattan
from typing import Generator, Union
from operators_bicing import BicingOperator, \
    CambiarEstacionCarga, \
        IntercambiarEstacionCarga, \
            CambiarOrdenDescarga, \
                CambiarEstacionDescarga, \
                    IntercambiarEstacionDescarga


class EstadoBicing(object):
    def __init__(self, info_estaciones: list[dict], lista_furgonetas: list[Furgoneta]) -> None:
        self.info_estaciones = info_estaciones
        self.lista_furgonetas = lista_furgonetas
        self.balances_rutas: list[Union[float, None]] = [None for _ in range(params.n_furgonetas)]
        self.balance_estaciones: Union[float, None] = None
        self.balance_total: Union[float, None] = None
   
    def copy(self) -> 'EstadoBicing':
        # Restauramos los valores por defecto de las estacinones, ya que no queremos arrastrar los cambios del estado anterior
        new_info_estaciones: list[dict] = [{'index': index, \
                                    'dif': est.num_bicicletas_next - est.demanda, \
                                    'disp': est.num_bicicletas_no_usadas} \
                                        for index, est in enumerate(params.estaciones)]
        
        new_lista_furgonetas: list[Furgoneta] = [furgoneta.copy() for furgoneta in self.lista_furgonetas]

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
            km_trayecto1 = distancia_manhattan(self.get_coords_est(furgoneta.id_est_origen), self.get_coords_est(furgoneta.id_est_dest1)) / 1000
            km_trayecto2 = distancia_manhattan(self.get_coords_est(furgoneta.id_est_dest1), self.get_coords_est(furgoneta.id_est_dest2)) / 1000
            
            primera_parada = self.get_coords_est(furgoneta.id_est_dest1)
            segunda_parada = self.get_coords_est(furgoneta.id_est_dest2)
            num_primera_parada = furgoneta.bicicletas_descargadas_1
            num_segunda_parada = furgoneta.bicicletas_descargadas_2

            str_rutas += f"   * F[{furgoneta.id}]:"\
                  + f"  C=[Coord={self.get_coords_est(furgoneta.id_est_origen)}, num={furgoneta.bicicletas_cargadas}]"\
                      + f"  |  D1=[Coords={primera_parada}, num={num_primera_parada}]"\
                          + f"  |  D2=[Coord={segunda_parada}, num={num_segunda_parada}]"\
                              +f"  |  KM=({km_trayecto1})+({km_trayecto2})={km_trayecto1+km_trayecto2} [{self.balances_rutas[furgoneta.id]}€]\n"

        return f"\n\nRUTAS CALCULADAS:\n{str_rutas}"
    
    def get_coords_est(self, id_est) -> tuple:
        return (params.estaciones[id_est].coordX, params.estaciones[id_est].coordY)

    def realizar_ruta(self, id_furgoneta: int) -> float:
        furgoneta = self.lista_furgonetas[id_furgoneta]
        self.asignar_bicicletas_carga_descarga(id_furgoneta)
        
        carga = furgoneta.bicicletas_cargadas
        descarga1 = furgoneta.bicicletas_descargadas_1
        descarga2 = furgoneta.bicicletas_descargadas_2
        distancia_a_b = distancia_manhattan(self.get_coords_est(furgoneta.id_est_origen), self.get_coords_est(furgoneta.id_est_dest1)) / 1000
        distancia_b_c = distancia_manhattan(self.get_coords_est(furgoneta.id_est_dest1), self.get_coords_est(furgoneta.id_est_dest2)) / 1000

        # Acutalizamos los valores de diferencia y disponibilidad
        self.info_estaciones[furgoneta.id_est_origen]['dif'] -= carga
        self.info_estaciones[furgoneta.id_est_origen]['disp'] -= carga

        self.info_estaciones[furgoneta.id_est_dest1]['dif'] += descarga1
        self.info_estaciones[furgoneta.id_est_dest1]['disp'] += descarga1

        self.info_estaciones[furgoneta.id_est_dest2]['dif'] += descarga2
        self.info_estaciones[furgoneta.id_est_dest2]['disp'] += descarga2

        coste_a_b = ((carga + 9) // 10) * distancia_a_b
        coste_b_c = ((descarga2 + 9) // 10) * distancia_b_c
        
        self.balances_rutas[id_furgoneta] = -(coste_a_b + coste_b_c)

        return -(coste_a_b + coste_b_c)
    

    """def realizar_ruta2(self, id_furgoneta: int) -> float:
        furgoneta = self.lista_furgonetas[id_furgoneta]
        self.asignar_bicicletas_carga_descarga(id_furgoneta)
        
        carga = furgoneta.bicicletas_cargadas

        # Calcular costos y establecer el orden de las paradas
        descarga1 = furgoneta.bicicletas_descargadas_1
        descarga2 = furgoneta.bicicletas_descargadas_2
        distancia_a_b = distancia_manhattan(self.get_coords_est(furgoneta.id_est_origen), self.get_coords_est(furgoneta.id_est_dest1)) / 1000
        distancia_a_c = distancia_manhattan(self.get_coords_est(furgoneta.id_est_origen), self.get_coords_est(furgoneta.id_est_dest2)) / 1000 
        distancia_b_c = distancia_manhattan(self.get_coords_est(furgoneta.id_est_dest1), self.get_coords_est(furgoneta.id_est_dest2)) / 1000
        coste_a_b_c = ((carga + 9) // 10) * distancia_a_b + ((carga-descarga1 + 9) // 10) * distancia_b_c
        coste_a_c_b = ((carga + 9) // 10) * distancia_a_c + ((carga-descarga2 + 9) // 10) * distancia_b_c

        # Acutalizamos los valores de diferencia y disponibilidad
        self.info_estaciones[furgoneta.id_est_origen]['dif'] -= carga
        self.info_estaciones[furgoneta.id_est_origen]['disp'] -= carga

        self.info_estaciones[furgoneta.id_est_dest1]['dif'] += descarga1
        self.info_estaciones[furgoneta.id_est_dest1]['disp'] += descarga1

        self.info_estaciones[furgoneta.id_est_dest2]['dif'] += descarga2
        self.info_estaciones[furgoneta.id_est_dest2]['disp'] += descarga2

        return -min(coste_a_b_c, coste_a_c_b)
"""

    def asignar_bicicletas_carga_descarga(self, id_furgoneta: int) -> None:
        furgoneta = self.lista_furgonetas[id_furgoneta]
        est_origen = self.info_estaciones[furgoneta.id_est_origen]
        est_destino1 = self.info_estaciones[furgoneta.id_est_dest1]
        est_destino2 = self.info_estaciones[furgoneta.id_est_dest2]

        # Calculamos el número de bicicletas que se cargarán y descargarán
        bicicletas_carga = min(30, \
                               est_origen['disp'] if est_origen['disp'] > 0 else 0, \
                                abs(est_destino1['dif']) if est_destino1['dif'] < 0 else 0 \
                                    + abs(est_destino2['dif']) if est_destino2['dif'] < 0 else 0)
        bicicletas_descarga_1 = min(bicicletas_carga, abs(est_destino1['dif']) if est_destino1['dif'] < 0 else 0)
        bicicletas_descarga_2 = bicicletas_carga - bicicletas_descarga_1

        # Actualizamos los valores en la furgoneta
        furgoneta.bicicletas_cargadas = bicicletas_carga
        furgoneta.bicicletas_descargadas_1 = bicicletas_descarga_1
        furgoneta.bicicletas_descargadas_2 = bicicletas_descarga_2
    
    def calcular_balance_rutas(self) -> float:
        balance_rutas = 0
        #Calcular el balance de todas las rutas
        for furgoneta in self.lista_furgonetas:
            balance_rutas += self.realizar_ruta(furgoneta.id)
        return balance_rutas

    def calcular_balance_estaciones(self) -> int:
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
            
        self.balance_estaciones = balance_estaciones
                
        return balance_estaciones
    
    def calcular_balance_total(self) -> float:
        balance_rutas = self.calcular_balance_rutas()
        balance_estaciones = self.calcular_balance_estaciones()
        self.balance_total = balance_rutas + balance_estaciones
        return balance_rutas + balance_estaciones

    def heuristic(self) -> float:
        return self.calcular_balance_total()
        
    def generate_actions(self) -> Generator:
        # Creamos un set() para aseguramos de que dos furgonetas no carguen en la misma estación
        estaciones_carga: set[int] = set()
        for furgoneta in self.lista_furgonetas:
            estaciones_carga.add(furgoneta.id_est_origen)
        
        # Generate all the possible actions for the current state of the problem:
        for furgoneta in self.lista_furgonetas:
            
            # CambiarEstacionCarga ###############################################################################
            for est in self.info_estaciones:
                if est['index'] not in estaciones_carga:
                    yield CambiarEstacionCarga(id_furgoneta=furgoneta.id, \
                                               id_est=est['index'])
            
            # IntercambiarEstacionCarga ##########################################################################
            for furgoneta2 in self.lista_furgonetas:
                if furgoneta.id <= furgoneta2.id: # Para evitar que se repitan los intercambios
                        yield IntercambiarEstacionCarga(id_furgoneta1=furgoneta.id, id_furgoneta2=furgoneta2.id)
            
            # CambiarOrdenDescarga ###############################################################################
            yield CambiarOrdenDescarga(id_furgoneta=furgoneta.id)

            # CambiarEstacionDescarga ############################################################################
            for est in self.info_estaciones:
                for pos_est in {0, 1}:
                    # No hacemos comprobación de que la nueva estación de descarga sea distinta a la anterior porque este 
                    # caso ya se trata en el método asignar_bicicletas_carga_descarga()
                    yield CambiarEstacionDescarga(id_furgoneta=furgoneta.id, \
                                                  id_est=est['index'], \
                                                    pos_est=pos_est)
            
            # IntercambiarEstacionDescarga #######################################################################
            for furgoneta2 in self.lista_furgonetas:
                if furgoneta.id <= furgoneta2.id: # Para evitar que se repitan los intercambios
                    f_est_destinos = (furgoneta.id_est_dest1, furgoneta.id_est_dest2)
                    f2_est_destinos = (furgoneta2.id_est_dest1, furgoneta2.id_est_dest2)
                    for pos_est1 in {0, 1}:
                        for pos_est2 in {0, 1}:
                            if self.get_coords_est(f_est_destinos[pos_est1]) != self.get_coords_est(f2_est_destinos[pos_est2]):
                                id_estacion1 = f_est_destinos[pos_est1]
                                id_estacion2 = f2_est_destinos[pos_est2]
                                yield IntercambiarEstacionDescarga(id_furgoneta1=furgoneta.id, id_furgoneta2=furgoneta2.id, \
                                                                   id_est1=id_estacion1, id_est2=id_estacion2, \
                                                                    pos_est1=pos_est1, pos_est2=pos_est2)

            """
            # CambiarNumeroBicisCarga ############################################################################
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
                        yield CambiarNumeroBicisCarga(furgoneta, furgoneta.info_est_origen, num_bicicletas_carga)
            """
    
    def apply_action(self, action: BicingOperator) -> 'EstadoBicing':
        new_state: EstadoBicing = self.copy()
        
        if isinstance(action, CambiarEstacionCarga):
            furgoneta = new_state.lista_furgonetas[action.id_furgoneta]
            furgoneta.id_est_origen = action.id_est
   
        elif isinstance(action, IntercambiarEstacionCarga):
            furgoneta1 = new_state.lista_furgonetas[action.id_furgoneta1]
            furgoneta2 = new_state.lista_furgonetas[action.id_furgoneta2]
            furgoneta1.id_est_origen, furgoneta2.id_est_origen = furgoneta2.id_est_origen, furgoneta1.id_est_origen

        elif isinstance(action, CambiarOrdenDescarga):
            furgoneta = new_state.lista_furgonetas[action.id_furgoneta]
            furgoneta.id_est_dest1, furgoneta.id_est_dest2 = furgoneta.id_est_dest2, furgoneta.id_est_dest1

        elif isinstance(action, CambiarEstacionDescarga):
            furgoneta = new_state.lista_furgonetas[action.id_furgoneta]
            if action.pos_est == 0:
                furgoneta.id_est_dest1 = action.id_est
            else:
                furgoneta.id_est_dest2 = action.id_est
    
        elif isinstance(action, IntercambiarEstacionDescarga):
            furgoneta1 = new_state.lista_furgonetas[action.id_furgoneta1]
            furgoneta2 = new_state.lista_furgonetas[action.id_furgoneta2]

            if action.pos_est1 == 0:
                if action.pos_est2 == 0:
                    furgoneta1.id_est_dest1, furgoneta2.id_est_dest1 = furgoneta2.id_est_dest1, furgoneta1.id_est_dest1
                else:
                    furgoneta1.id_est_dest1, furgoneta2.id_est_dest2 = furgoneta2.id_est_dest2, furgoneta1.id_est_dest1                
            else:
                if action.pos_est2 == 0:
                    furgoneta1.id_est_dest2, furgoneta2.id_est_dest1 = furgoneta2.id_est_dest1, furgoneta1.id_est_dest2
                else:
                    furgoneta1.id_est_dest2, furgoneta2.id_est_dest2 = furgoneta2.id_est_dest2, furgoneta1.id_est_dest2

        """elif isinstance(action, CambiarNumeroBicisCarga):
            furgoneta = new_state.lista_furgonetas[action.id_furgoneta]
            furgoneta.set_num_bicicletas_cargadas(action.num_bicicletas_carga)"""

        return new_state

    def print_state(self, inicial: bool = False) -> None:
        str_balances = ""
        if inicial:
            str_balances += f"\n{'*'*35 + ' [ ESTADO INICIAL ] ' + '*'*35}\n"
        else:
            str_balances += f"\n{'*'*35 + ' [ SOLUCIÓN FINAL ] ' + '*'*35}\n"
        
        str_balances += f"\nBALANCE RUTAS: {sum(self.balances_rutas)}\n" + \
                    f"BALANCE ESTACIONES: {self.balance_estaciones}\n" + \
                        f"BALANCE TOTAL: {self.balance_total}"
        
        print(str_balances + self.__str__())