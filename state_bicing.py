from furgoneta_bicing import Furgoneta
from parameters_bicing import params
from functions_bicing import distancia_manhattan
from typing import Generator
import pygame
from operators_bicing import BicingOperator, \
    CambiarEstacionCarga, \
        IntercambiarEstacionCarga, \
            CambiarOrdenDescarga, \
                CambiarEstacionDescarga, \
                    IntercambiarEstacionDescarga, \
                        QuitarEstacionDescarga

from pdb import set_trace as bp

class EstadoBicing(object):
    def __init__(self, lista_furgonetas: list[Furgoneta]) -> None:
        self.info_estaciones: list[dict] = [{'index': index, \
                                    'dif': est.num_bicicletas_next - est.demanda, \
                                    'disp': est.num_bicicletas_no_usadas} \
                                        for index, est in enumerate(params.estaciones)]
        self.lista_furgonetas = lista_furgonetas

    def copy(self) -> 'EstadoBicing':
        new_lista_furgonetas: list[Furgoneta] = [furgoneta.copy() for furgoneta in self.lista_furgonetas]
        return EstadoBicing(lista_furgonetas=new_lista_furgonetas)

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
            total_km = km_trayecto1 + km_trayecto2

            primer_id = furgoneta.id_est_dest1
            segundo_id = furgoneta.id_est_dest2

            primera_parada = self.get_coords_est(furgoneta.id_est_dest1)
            segunda_parada = self.get_coords_est(furgoneta.id_est_dest2)
            num_primera_parada = furgoneta.bicicletas_descargadas_1
            num_segunda_parada = furgoneta.bicicletas_descargadas_2

            if primer_id == segundo_id:
                segundo_id = "NONE"
                segunda_parada = "(NONE, NONE)"
                num_segunda_parada = "NONE"
                km_trayecto2 = "NONE"

            str_rutas += f"   * F[{furgoneta.id}]:"\
                  + f"  C=[Est({furgoneta.id_est_origen})={self.get_coords_est(furgoneta.id_est_origen)}, num={furgoneta.bicicletas_cargadas}]"\
                      + f"  |  D1=[Est({primer_id})={primera_parada}, num={num_primera_parada}]"\
                          + f"  |  D2=[Est({segundo_id})={segunda_parada}, num={num_segunda_parada}]"\
                              +f"  |  KM=({km_trayecto1})+({km_trayecto2})={total_km} [{self.calcular_balance_ruta_furgoneta(furgoneta.id)}€]\n"

        return f"\n\nRUTAS CALCULADAS:\n{str_rutas}"
    
    def get_coords_est(self, id_est) -> tuple:
        return (params.estaciones[id_est].coordX, params.estaciones[id_est].coordY)
    
    def __restaurar_estaciones(self) -> None:
        self.info_estaciones: list[dict] = [{'index': index, \
                    'dif': est.num_bicicletas_next - est.demanda, \
                    'disp': est.num_bicicletas_no_usadas} \
                        for index, est in enumerate(params.estaciones)]

    def realizar_ruta(self, id_furgoneta: int) -> float:
        furgoneta = self.lista_furgonetas[id_furgoneta]
        
        # Calculamos el número de bicicletas que se cargarán y descargarán
        self.asignar_bicicletas_carga_descarga(id_furgoneta)

        # Actalizamos los valores de diferencia y disponibilidad
        self.info_estaciones[furgoneta.id_est_origen]['dif'] -= furgoneta.bicicletas_cargadas
        self.info_estaciones[furgoneta.id_est_origen]['disp'] -= furgoneta.bicicletas_cargadas

        self.info_estaciones[furgoneta.id_est_dest1]['dif'] += furgoneta.bicicletas_descargadas_1
        self.info_estaciones[furgoneta.id_est_dest1]['disp'] += furgoneta.bicicletas_descargadas_1

        self.info_estaciones[furgoneta.id_est_dest2]['dif'] += furgoneta.bicicletas_descargadas_2
        self.info_estaciones[furgoneta.id_est_dest2]['disp'] += furgoneta.bicicletas_descargadas_2

    def asignar_bicicletas_carga_descarga(self, id_furgoneta: int) -> None:
        furgoneta = self.lista_furgonetas[id_furgoneta]
        est_origen = self.info_estaciones[furgoneta.id_est_origen]
        est_destino1 = self.info_estaciones[furgoneta.id_est_dest1]
        est_destino2 = self.info_estaciones[furgoneta.id_est_dest2]

        # Calculamos el número de bicicletas que se cargarán y descargarán
        if furgoneta.id_est_dest1 != furgoneta.id_est_dest2:
            bicicletas_carga = min(30, \
                                    est_origen['disp'] if est_origen['disp'] > 0 else 0, \
                                        (abs(est_destino1['dif']) if (est_destino1['dif'] < 0) else 0) + \
                                            (abs(est_destino2['dif']) if (est_destino2['dif'] < 0) else 0))
            bicicletas_descarga_1 = min(bicicletas_carga, abs(est_destino1['dif']) if (est_destino1['dif'] < 0) else 0)
            bicicletas_descarga_2 = bicicletas_carga - bicicletas_descarga_1

        else: # Caso en que se hace un movimiento "nulo"
            bicicletas_carga = min(30, \
                                    est_origen['disp'] if est_origen['disp'] > 0 else 0, \
                                        abs(est_destino1['dif']) if (est_destino1['dif'] < 0) else 0)
            bicicletas_descarga_1 = bicicletas_carga
            bicicletas_descarga_2 = 0

        # Actualizamos los valores en la furgoneta
        furgoneta.bicicletas_cargadas = bicicletas_carga
        furgoneta.bicicletas_descargadas_1 = bicicletas_descarga_1
        furgoneta.bicicletas_descargadas_2 = bicicletas_descarga_2

    def calcular_balance_ruta_furgoneta(self, id_furgoneta: int) -> float:
        furgoneta = self.lista_furgonetas[id_furgoneta]
        
        carga = furgoneta.bicicletas_cargadas
        descarga1 = furgoneta.bicicletas_descargadas_1
        descarga2 = furgoneta.bicicletas_descargadas_2

        assert carga == descarga1 + descarga2, "El número de bicicletas cargadas no coincide con el número de bicicletas descargadas"

        distancia_a_b = distancia_manhattan(self.get_coords_est(furgoneta.id_est_origen), self.get_coords_est(furgoneta.id_est_dest1)) / 1000
        distancia_b_c = distancia_manhattan(self.get_coords_est(furgoneta.id_est_dest1), self.get_coords_est(furgoneta.id_est_dest2)) / 1000

        coste_a_b = ((carga + 9) // 10) * distancia_a_b
        coste_b_c = ((descarga2 + 9) // 10) * distancia_b_c
        
        return -(coste_a_b + coste_b_c)
    
    def calcular_balance_rutas(self) -> float:
        balance_rutas = 0
        #Calcular el balance de todas las rutas
        for furgoneta in self.lista_furgonetas:
            balance_rutas += self.calcular_balance_ruta_furgoneta(furgoneta.id)
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
            
        return balance_estaciones
    
    def calcular_balance_total(self) -> float:
        balance_rutas = self.calcular_balance_rutas()
        balance_estaciones = self.calcular_balance_estaciones()
        return balance_rutas + balance_estaciones

    def heuristic(self, coste_transporte: bool) -> float:
        self.__restaurar_estaciones()
        for furgoneta in self.lista_furgonetas:
            self.realizar_ruta(furgoneta.id)
        
        if coste_transporte:
            return self.calcular_balance_total()
        else:
            return self.calcular_balance_estaciones()
        
    def generate_actions(self) -> Generator:
        # Creamos un set() para aseguramos de que dos furgonetas no carguen en la misma estación
        estaciones_carga: set[int] = set()
        for furgoneta in self.lista_furgonetas:
            estaciones_carga.add(furgoneta.id_est_origen)
        
        # Generate all the possible actions for the current state of the problem:
        for furgoneta in self.lista_furgonetas:
            
            # CambiarEstacionCarga ###############################################################################
            for est in self.info_estaciones:
                if est['index'] not in estaciones_carga and est['index'] != furgoneta.id_est_dest1 and est['index'] != furgoneta.id_est_dest2:
                    yield CambiarEstacionCarga(id_furgoneta=furgoneta.id, \
                                               id_est=est['index'])
            
            # IntercambiarEstacionCarga ##########################################################################
            for furgoneta2 in self.lista_furgonetas:
                if furgoneta.id < furgoneta2.id: # Para evitar que se repitan los intercambios
                    if furgoneta2.id_est_origen != furgoneta.id_est_dest1 and furgoneta2.id_est_origen != furgoneta.id_est_dest2 \
                        and furgoneta.id_est_origen != furgoneta2.id_est_dest1 and furgoneta.id_est_origen != furgoneta2.id_est_dest2:
                            yield IntercambiarEstacionCarga(id_furgoneta1=furgoneta.id, id_furgoneta2=furgoneta2.id)
            
            # CambiarOrdenDescarga ###############################################################################
            yield CambiarOrdenDescarga(id_furgoneta=furgoneta.id)

            # CambiarEstacionDescarga ############################################################################
            for est in self.info_estaciones:
                if est['index'] != furgoneta.id_est_origen:
                    for pos_est in {0, 1}:
                        # No hacemos comprobación de que la nueva estación de descarga sea distinta a la anterior porque este 
                        # caso ya se trata en el método asignar_bicicletas_carga_descarga()
                        yield CambiarEstacionDescarga(id_furgoneta=furgoneta.id, \
                                                    id_est=est['index'], \
                                                        pos_est=pos_est)
                
            # IntercambiarEstacionDescarga #######################################################################
            for furgoneta2 in self.lista_furgonetas:
                if furgoneta.id < furgoneta2.id: # Para evitar que se repitan los intercambios
                    f_est_destinos = (furgoneta.id_est_dest1, furgoneta.id_est_dest2)
                    f2_est_destinos = (furgoneta2.id_est_dest1, furgoneta2.id_est_dest2)
                    for pos_est1 in {0, 1}:
                        for pos_est2 in {0, 1}:
                            if self.get_coords_est(f_est_destinos[pos_est1]) != self.get_coords_est(f2_est_destinos[pos_est2]): # Para no intercambiar la misma estación
                                id_estacion1 = f_est_destinos[pos_est1]
                                id_estacion2 = f2_est_destinos[pos_est2]
                                if id_estacion2 != furgoneta.id_est_origen and id_estacion1 != furgoneta2.id_est_origen:
                                    yield IntercambiarEstacionDescarga(id_furgoneta1=furgoneta.id, id_furgoneta2=furgoneta2.id, \
                                                                    id_est1=id_estacion1, id_est2=id_estacion2, \
                                                                        pos_est1=pos_est1, pos_est2=pos_est2)
            
            # QuitarEstacionDescarga #############################################################################
            for pos_est in {0, 1}:
                yield QuitarEstacionDescarga(id_furgoneta=furgoneta.id, pos_est=pos_est)
    
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

        elif isinstance(action, QuitarEstacionDescarga):
            furgoneta = new_state.lista_furgonetas[action.id_furgoneta]
            if action.pos_est == 0: # Quitar la primera estación de descarga
                furgoneta.id_est_dest1 = furgoneta.id_est_dest2
            else: # Quitar la segunda estación de descarga
                furgoneta.id_est_dest2 = furgoneta.id_est_dest1

        return new_state

    def print_state(self, inicial: bool = False) -> None:
        str_balances = ""
        if inicial:
            str_balances += f"\n{'*'*35 + ' [ ESTADO INICIAL ] ' + '*'*35}\n"
        else:
            str_balances += f"\n{'*'*35 + ' [ SOLUCIÓN FINAL ] ' + '*'*35}\n"
        
        str_balances += f"\nBALANCE RUTAS: {self.calcular_balance_rutas() if params.coste_transporte else 'NONE'}\n" + \
                    f"BALANCE ESTACIONES: {self.calcular_balance_estaciones()}\n" + \
                        f"BALANCE TOTAL: {self.calcular_balance_total() if params.coste_transporte else self.calcular_balance_estaciones()}"
        
        print(str_balances + self.__str__())

    def visualize_state(self, manhattan: bool = True) -> None:
        # Inicializar pygame
        pygame.init()

        # Dimensiones de la ventana
        WIDTH, HEIGHT = 800, 800
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Ciudad con estaciones y furgonetas')

        # Colores
        WHITE = (255, 255, 255)
        GRAY = (230, 230, 230)
        BLACK = (0, 0, 0)
        CYAN = (0, 255, 255)
        BLUE = (50, 100, 255)
        PURPLE = (135, 0, 170)
        PINK = (255, 175, 240)

        LIST_COLORS = [BLACK, BLUE, PURPLE, PINK, CYAN]

        RED = (200, 0, 0)
        YELLOW = (255, 200, 0)
        GREEN = (0, 200, 0)

        # Tamaño de la ciudad en metros
        CITY_SIZE = 10000

        # Escalar coordenadas de metros a pixels
        def scale(coord):
            return int(coord * (WIDTH / CITY_SIZE))

        # Dibujar la ciudad
        def draw_city():
            # Dibujar las calles
            for i in range(0, CITY_SIZE, 100):
                pygame.draw.line(screen, GRAY, (scale(i), 0), (scale(i), HEIGHT))
                pygame.draw.line(screen, GRAY, (0, scale(i)), (WIDTH, scale(i)))

        # Dibujar estaciones de bicicletas
        def draw_stations(stations, vans):
            printed_origins = set()
            printed_destinations = set()

            for van in vans:
                est_origen = van[0]
                pygame.draw.circle(screen, GREEN, (scale(est_origen[0]), scale(est_origen[1])), 6)
                printed_origins.add(est_origen)
            
            for van in vans:
                est_destino1, est_destino2 = van[1], van[2]
                
                if est_destino1 not in printed_origins:
                    pygame.draw.circle(screen, RED, (scale(est_destino1[0]), scale(est_destino1[1])), 6)
                    printed_destinations.add(est_destino1)
                elif est_destino1 not in printed_destinations:
                    pygame.draw.circle(screen, YELLOW, (scale(est_destino1[0]), scale(est_destino1[1])), 6)
                    printed_destinations.add(est_destino1)
                
                if est_destino2 not in printed_origins:
                    pygame.draw.circle(screen, RED, (scale(est_destino2[0]), scale(est_destino2[1])), 6)
                    printed_destinations.add(est_destino2)
                elif est_destino2 not in printed_destinations:
                    pygame.draw.circle(screen, YELLOW, (scale(est_destino2[0]), scale(est_destino2[1])), 6)
                    printed_destinations.add(est_destino2)

            for id_est, station in enumerate(stations):
                if station not in printed_origins and station not in printed_destinations:            
                    pygame.draw.circle(screen, BLACK, (scale(station[0]), scale(station[1])), 4)

        # Dibujar números de estaciones
        def draw_texts(self):
            for id_est, station in enumerate(stations):
                # Diferencia de la estación
                number = str(f"E{id_est}(DF:{params.estaciones[id_est].num_bicicletas_next - params.estaciones[id_est].demanda}, DP:{params.estaciones[id_est].num_bicicletas_no_usadas})")

                # Crea una fuente
                font = pygame.font.Font(None, 15)
                
                # Renderiza el número
                text_surface = font.render(number, True, (0, 0, 0))
                
                # Dibuja el número debajo de la estación
                screen.blit(text_surface, (scale(station[0]) - 15, scale(station[1]) + 8))  # -10 y +8 son offsets para centrar y mover debajo del círculo

        def draw_manhattan_path(start, end, color):
            x1, y1 = start
            x2, y2 = end
            
            # Dibuja una línea horizontal desde el punto de inicio al punto final (pero manteniendo la coordenada y del inicio)
            pygame.draw.line(screen, color, (scale(x1), scale(y1)), (scale(x2), scale(y1)), 3)
            # Dibuja una línea vertical desde el final de la línea anterior hasta el punto final
            pygame.draw.line(screen, color, (scale(x2), scale(y1)), (scale(x2), scale(y2)), 3)

        def draw_euclidean_path(start, end, color):
            x1, y1 = start
            x2, y2 = end
            pygame.draw.line(screen, color, (scale(x1), scale(y1)), (scale(x2), scale(y2)), 3)

        def draw_vans(vans, manhattan):
            for i, van in enumerate(vans):
                COLOR = LIST_COLORS[i % len(LIST_COLORS)]
                start, stop1, stop2 = van
                if manhattan:
                    draw_manhattan_path(start, stop1, COLOR)
                    draw_manhattan_path(stop1, stop2, COLOR)
                else:
                    draw_euclidean_path(start, stop1, COLOR)
                    draw_euclidean_path(stop1, stop2, COLOR)


        # Crear estaciones y rutas de furgonetas aleatoriamente
        stations = [(est.coordX, est.coordY) for est in params.estaciones]

        vans = [(self.get_coords_est(furgoneta.id_est_origen),
                self.get_coords_est(furgoneta.id_est_dest1),
                self.get_coords_est(furgoneta.id_est_dest2)) for furgoneta in self.lista_furgonetas]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(WHITE)
            draw_city()
            draw_stations(stations, vans)
            draw_vans(vans, manhattan)
            draw_texts(self)
            pygame.display.flip()

        pygame.quit()