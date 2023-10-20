from estaciones_bicing import Estaciones
from state_bicing import EstadoBicing
from furgoneta_bicing import Furgoneta
from parameters_bicing import params
from problem_bicing import ProblemaBicing
from aima.search import hill_climbing, simulated_annealing
import random
from typing import Union
from timeit import timeit
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


# Declaración de funciones
def generate_initial_state(opt: int = 0, semilla: Union[int, None] = None, operadores_activos: dict = {operator: True for operator in {'CambiarEstacionCarga', \
                                                               'CambiarEstacionCarga', \
                                                                'IntercambiarEstacionCarga', \
                                                                    'CambiarOrdenDescarga', \
                                                                        'CambiarEstacionDescarga', \
                                                                            'IntercambiarEstacionDescarga', \
                                                                                'QuitarEstacionDescarga', \
                                                                                    'ReasignarFurgoneta', \
                                                                                        'ReordenarFurgonetas'}}) -> EstadoBicing:
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
    if opt == 0:        
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
    
    # NIVEL DE OPTIMIZACIÓN 1: ORIGEN DE FURGONETAS A ESTACIONES CON DIFERENCIA POSITIVA, DESTINO A ESTACIONES CON DIFERENCIA NEGATIVA
    elif opt == 1:
        # Creamos una lista con los índices de las estaciones con diferencia positiva y otra con los de diferencia negativa    
        lista_est_excedente: list = []
        lista_est_faltante: list = []
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

            furgoneta.id_est_origen = lista_est_excedente[id_est_o]
        
            # Asignamos las estaciones de destino a la furgoneta
            id_est_d1 = rng.randint(0, n_estaciones_destino - 1)
            id_est_d2 = rng.randint(0, n_estaciones_destino - 1)

            furgoneta.id_est_dest1 = lista_est_faltante[id_est_d1]
            furgoneta.id_est_dest2 = lista_est_faltante[id_est_d2]

    # NIVEL DE OPTIMIZACIÓN 2: ORIGEN DE FURGONETAS A LAS ESTACIONES CON MAYOR DIFERENCIA POSITIVA, DESTINO A LAS ESTACIONES CON MAYOR DIFERENCIA NEGATIVA
    elif opt == 2:
         # Creamos una lista con los índices de las estaciones con diferencia positiva y otra con los de diferencia negativa    
        lista_est_excedente: list = []
        lista_est_faltante: list = []
        for est in info_estaciones:
            if est['dif'] < 0:
                lista_est_faltante.append((est['dif'], est['index']))
            elif est['dif'] > 0 and est['disp'] > 0:
                lista_est_excedente.append((est['dif'], est['index']))
        
        lista_est_excedente.sort(reverse=True)
        lista_est_faltante.sort()

        j = 0
        for i, furgoneta in enumerate(lista_furgonetas):
            furgoneta.id_est_origen = lista_est_excedente[i][1]
            furgoneta.id_est_dest1 = lista_est_faltante[j][1]
            furgoneta.id_est_dest2 = lista_est_faltante[j+1][1]
            j += 2
                
    state = EstadoBicing(lista_furgonetas=lista_furgonetas, operadores_activos=operadores_activos)
    return state
    
def comparar_resultados_operadores(iteraciones: int = 10, operadores_activos: dict = {operator: True for operator in {'CambiarEstacionCarga', \
                                                               'CambiarEstacionCarga', \
                                                                'IntercambiarEstacionCarga', \
                                                                    'CambiarOrdenDescarga', \
                                                                        'CambiarEstacionDescarga', \
                                                                            'IntercambiarEstacionDescarga', \
                                                                                'QuitarEstacionDescarga', \
                                                                                    'ReasignarFurgoneta', \
                                                                                        'ReordenarFurgonetas'}}):
    
    for _ in range(iteraciones):
        semilla = random.randint(0, 1_000_000)
        state1 = generate_initial_state(semilla=semilla)
        state2 = generate_initial_state(semilla=semilla, operadores_activos=operadores_activos)
        hill_climbing_1 = hill_climbing(ProblemaBicing(initial_state=state1))
        hill_climbing_2 = hill_climbing(ProblemaBicing(initial_state=state2))
        print(hill_climbing_1.heuristic(coste_transporte=params.coste_transporte), hill_climbing_2.heuristic(coste_transporte=params.coste_transporte))

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
    
##############################################################################################################################################

    # Experimento
    initial_state: EstadoBicing = generate_initial_state(opt = 0)
    initial_state.heuristic(coste_transporte=params.coste_transporte)
    initial_state.print_state(inicial=True)
    initial_state.visualize_state(manhattan = True)

    problema_bicing = ProblemaBicing(initial_state)
    final_solution_HC = hill_climbing(problema_bicing)
    final_solution_HC.print_state()
    print("SOLUCIONES COMPROBADAS:", problema_bicing.solutions_checked, "\n")
    final_solution_HC.visualize_state(manhattan = True)

    # Experimentos desactivando operadores:
    operadores_experimento = {'CambiarEstacionCarga': True, \
                                    'CambiarEstacionCarga': True, \
                                        'IntercambiarEstacionCarga': True, \
                                            'CambiarOrdenDescarga': True, \
                                                'CambiarEstacionDescarga': True, \
                                                    'IntercambiarEstacionDescarga': True, \
                                                        'QuitarEstacionDescarga': True, \
                                                            'ReasignarFurgoneta': True, \
                                                                'ReordenarFurgonetas': False}
    
    #comparar_resultados_operadores(iteraciones=10, operadores_activos=operadores_experimento)

    # Obtener estadísticas y generar un box plot
    """times_hill_climbing = [timeit(lambda: hill_climbing(problema_bicing), number=1) for _ in range(15)]
    times_simulated_annealing = [timeit(lambda: simulated_annealing(problema_bicing), number=1) for _ in range(15)]
    
    data_to_plot = [times_hill_climbing, times_simulated_annealing]
    labels=['hill_climbing', 'simulated_annealing']
        
    plt.boxplot(data_to_plot, labels=labels)
    plt.ylabel('Tiempo de ejecución (s)')
    plt.title('Comparativa de Hill Climning y Simulated Annealing con Boxplots')
    plt.savefig('test.png')"""



    """# Obtener estadísticas y generar un line plot
    hill_climbing_value = None # HEM DE FER QUE HILL CLIMBING VALUE --> returns a list of objective function values over iterations:
    
    plt.figure(figsize=(10, 6))  # Tamaño de la figura
    plt.plot(hill_climbing_value, marker='o', linestyle='-')  # Creamos el gráfico
    plt.title("Progreso de Hill Climbing") 
    plt.xlabel("Iteraciones")  
    plt.ylabel("Coste")  
    plt.grid(True)  # Añadimos grid para una mejor ínterpretación"""

