from estaciones_bicing import Estaciones
from state_bicing import EstadoBicing
from furgoneta_bicing import Furgoneta
from parameters_bicing import params
from problem_bicing import ProblemaBicing
from aima.search import hill_climbing, simulated_annealing
import random
from typing import Union
from timeit import timeit

# Declaración de funciones
def generate_initial_state(greedy: bool = False, semilla: Union[int, None] = None) -> EstadoBicing:
    rng = random.Random(semilla)
    
    n_estaciones = params.n_estaciones
    n_furgonetas = params.n_furgonetas
    
    # Creamos una lista con la información que modificaremos de cada estación, para no tener que trabajar con objetos Estacion
    info_estaciones: list[dict] = [{'index': index, \
                                    'dif': est.num_bicicletas_next - est.demanda, \
                                    'disp': est.num_bicicletas_no_usadas} \
                                        for index, est in enumerate(params.estaciones)]
    
    # Creamos una lista con las furgonetas
    lista_furgonetas = [Furgoneta(id_furgoneta=i) for i in range(n_furgonetas)]
    
    # Creamos un set() con los id de las estaciones que ya tienen una furgoneta asignada 
    # para evitar asignar más de una furgoneta a la misma estación de carga
    est_con_furgoneta = set()
    
    # DISTRIBUCIÓN TOTALMENTE RANDOM
    if not greedy:        
        for furgoneta in lista_furgonetas:
            # Asignamos una estación de origen a la furgoneta
            id_est_o = rng.randint(0, n_estaciones - 1)
            while id_est_o in est_con_furgoneta:
                id_est_o = rng.randint(0, n_estaciones- 1)
            est_con_furgoneta.add(id_est_o)

            furgoneta.id_est_origen = id_est_o
        
            # Asignamos las estaciones de destino a la furgoneta
            id_est_d1 = rng.randint(0, n_estaciones - 1)
            id_est_d2 = rng.randint(0, n_estaciones - 1)

            furgoneta.id_est_dest1 = id_est_d1
            furgoneta.id_est_dest2 = id_est_d2
    
    # DISTRIBUCIÓN "AVARICIOSA" (TENIENDO EN CUENTA LA DIFERENCIA DE BICICLETAS DE CADA ESTACIÓN)
    else:
        # Creamos una lista con los índices de las estaciones con diferencia positiva y otra con los de diferencia negativa    
        lista_est_excedente: list[dict] = []
        lista_est_faltante: list[dict] = []
        for est in info_estaciones:
            if est['dif'] < 0:
                lista_est_faltante.append(est['index'])
            elif est['dif'] > 0 and est['disp'] > 0:
                lista_est_excedente.append(est['index'])
        
        n_estaciones_origen = len(lista_est_excedente)
        n_estaciones_destino = len(lista_est_faltante)
                
        for furgoneta in lista_furgonetas:
            # Asignamos una estación de origen a la furgoneta
            id_est_o = rng.randint(0, n_estaciones_origen - 1)
            while id_est_o in est_con_furgoneta:
                id_est_o = rng.randint(0, n_estaciones_origen - 1)
            est_con_furgoneta.add(id_est_o)

            furgoneta.id_est_origen = id_est_o
        
            # Asignamos las estaciones de destino a la furgoneta
            id_est_d1 = rng.randint(0, n_estaciones_destino - 1)
            id_est_d2 = rng.randint(0, n_estaciones_destino - 1)

            furgoneta.id_est_dest1 = id_est_d1
            furgoneta.id_est_dest2 = id_est_d2
                
    state = EstadoBicing(info_estaciones=info_estaciones, lista_furgonetas=lista_furgonetas)
    return state
    
# Programa principal
if __name__ == '__main__':
    """
    Prueba de funcionamiento:
    Creación de una instancia de estaciones y escritura a consola de:
    * Información de cada estacion
    * Datos por estacion de bicicletas presentes, demandadas, diferencia y excedente
    * Datos globales de bicicletas demandadas, disponibles para mover
      y bicicletas que es necesario mover
    """    
    estaciones = Estaciones(params.n_estaciones, params.n_bicicletas, params.seed)
    acum_bicicletas = 0
    acum_demanda = 0
    acum_disponibles = 0
    acum_necesarias = 0

    #print("Sta Cur Dem Dif Exc")

    for id_estacion, estacion in enumerate(estaciones.lista_estaciones):
        num_bicicletas_no_usadas = estacion.num_bicicletas_no_usadas
        num_bicicletas_next = estacion.num_bicicletas_next
        demanda = estacion.demanda
        acum_bicicletas = acum_bicicletas + num_bicicletas_next
        acum_demanda = acum_demanda + demanda
        diferencia = num_bicicletas_next - demanda
        if diferencia > 0:
            if diferencia > num_bicicletas_no_usadas:
                excedente = num_bicicletas_no_usadas
            else:
                excedente = diferencia
            acum_disponibles = acum_disponibles + excedente
        else:
            excedente = 0
            acum_necesarias = acum_necesarias - diferencia

        #print("est %2s = %2d %2d" % (id_estacion, estacion.coordX, estacion.coordY))
        #print("%3d %3d %3d %3d %3d" % (num_bicicletas_no_usadas, num_bicicletas_next, demanda, diferencia, excedente))

    #print("Bicis= %3d Demanda= %3d Disponibles= %3d Necesitan= %3d" %
          #(acum_bicicletas, acum_demanda, acum_disponibles, acum_necesarias))
    
    # Experimento
    initial_state: EstadoBicing = generate_initial_state(greedy=True)
    #initial_state.heuristic()
    initial_state.print_state(inicial=True)
    initial_state.visualize_state(manhattan = False)

    problema_bicing = ProblemaBicing(initial_state)
    final_solution = hill_climbing(problema_bicing)
    final_solution.print_state()
    final_solution.visualize_state(manhattan = False)
    print("SOLUCIONES COMPROBADAS:", problema_bicing.solutions_checked, "\n")

