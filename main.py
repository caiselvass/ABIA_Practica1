from state_bicing import EstadoBicing
from generate_initial_state_bicing import generate_initial_state
from parameters_bicing import params
from problem_bicing import ProblemaBicing
from aima.search import hill_climbing, simulated_annealing
import random
from math import exp
from typing import Union
import time
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# Declaración de funciones
def comparar_operadores_default(opt: int = 0, iteraciones: int = 10, semilla: Union[int, None] = None, operadores_activos: dict = {operator: True for operator in {'CambiarEstacionCarga', \
                                                               'CambiarEstacionCarga', \
                                                                'IntercambiarEstacionCarga', \
                                                                    'CambiarOrdenDescarga', \
                                                                        'CambiarEstacionDescarga', \
                                                                            'IntercambiarEstacionDescarga', \
                                                                                'QuitarEstacionDescarga', \
                                                                                    'ReasignarFurgoneta', \
                                                                                        'ReducirNumeroBicicletasCarga'}}) -> None:
    """
    Comparación de los resultados de Hill Climbing con los operadores por defecto y con los operadores modificados introducidos en el parámetro operadores_activos.
    """

    tiempo_default, tiempo_modificado, soluciones_expandidas_default, soluciones_expandidas_modificado = 0, 0, 0, 0
    beneficios_default, beneficios_modificado = [], []
    distancias_default, distancias_modificado = [], []
    rng = random.Random(semilla)

    for i in range(iteraciones):
        print(f"PROGRESO: {(i/iteraciones)*100}%", end='\r')
        seed = rng.randint(0, 1_000_000)
        state1 = generate_initial_state(opt=opt, semilla=seed)
        state2 = generate_initial_state(opt=opt, semilla=seed, operadores_activos=operadores_activos)
        
        problema1 = ProblemaBicing(initial_state=state1)
        inici1 = time.time()
        hill_climbing_1 = hill_climbing(problema1)
        tiempo_default += time.time() - inici1
        
        soluciones_expandidas_default += problema1.solutions_checked
        beneficios_default.append(hill_climbing_1.heuristic(coste_transporte=params.coste_transporte))
        distancia_total_default = sum([hill_climbing_1.get_distancias_furgoneta(id_f)[2] for id_f in range(params.n_furgonetas)])
        distancias_default.append(distancia_total_default)
        
        problema2 = ProblemaBicing(initial_state=state2)
        inici2 = time.time()
        hill_climbing_2 = hill_climbing(problema2)
        tiempo_modificado += time.time() - inici2
        
        soluciones_expandidas_modificado += problema2.solutions_checked
        beneficios_modificado.append(hill_climbing_2.heuristic(coste_transporte=params.coste_transporte))
        distancia_total_modificado = sum([hill_climbing_2.get_distancias_furgoneta(id_f)[2] for id_f in range(params.n_furgonetas)])
        distancias_modificado.append(distancia_total_modificado)

    print(f"\nHEURISTIC: {2 if params.coste_transporte else 1} | OPT: {opt} | ITERACIONES: {iteraciones}\n")
    print(f"MEDIA DEFECTO: {sum(beneficios_default)/iteraciones} | TIEMPO DEFAULT: {(tiempo_default/iteraciones)*1000} ms | Nº = {int(soluciones_expandidas_default/iteraciones)} | DISTANCIA DEFAULT: {sum(distancias_default)/iteraciones} | VARIANZA BENEF. DEFAULT: {sum([(beneficio - (sum(beneficios_default)/iteraciones))**2 for beneficio in beneficios_default])/iteraciones}")
    print(f"MEDIA MODIFICADO: {sum(beneficios_modificado)/iteraciones} | TIEMPO MODIFICADO: {(tiempo_modificado/iteraciones)*1000} ms) | Nº = {int(soluciones_expandidas_modificado/iteraciones)} | DISTANCIA MODIFICADO: {sum(distancias_modificado)/iteraciones} | VARIANZA BENEF.MODIFICADO: {sum([(beneficio - (sum(beneficios_modificado)/iteraciones))**2 for beneficio in beneficios_modificado])/iteraciones}\n")

def comparar_all_operadores(opt: int = 0, iteraciones: int = 10, semilla: Union[int, None] = None, operadores: dict = {operator: True for operator in {'CambiarEstacionCarga', \
                                                            'IntercambiarEstacionCarga', \
                                                                'CambiarOrdenDescarga', \
                                                                    'CambiarEstacionDescarga', \
                                                                        'IntercambiarEstacionDescarga', \
                                                                            'QuitarEstacionDescarga', \
                                                                                'ReasignarFurgoneta', \
                                                                                    'ReducirNumeroBicicletasCarga'}}) -> None:
    """
    Comprueba todas las posibles combinaciones de operadores y escribe en pantalla los resultados ordenados de mayor a menor beneficio medio.
    """

    progreso = 0
    media_beneficios = []

    for val8 in [True, False]:
        operadores['ReducirNumeroBicicletasCarga'] = val8
        for val7 in [True, False]:
            operadores['CambiarEstacionCarga'] = val7
            for val6 in [True, False]:
                operadores['IntercambiarEstacionCarga'] = val6
                for val5 in [True, False]:
                    operadores['CambiarOrdenDescarga'] = val5
                    for val4 in [True, False]:
                        operadores['CambiarEstacionDescarga'] = val4
                        for val3 in [True, False]:
                            operadores['IntercambiarEstacionDescarga'] = val3
                            for val2 in [True, False]:
                                operadores['QuitarEstacionDescarga'] = val2
                                for val1 in [True, False]:
                                    operadores['ReasignarFurgoneta'] = val1
                                    
                                    progreso += 1
                                    print(f"PROGRESO: {(progreso/256)*100}%", end='\r')
                                    
                                    beneficios_tmp = []
                                    tiempo, soluciones_expandidas = 0, 0
                                    rng = random.Random(semilla)
                                    for _ in range(iteraciones):
                                        seed = rng.randint(0, 1_000_000)
                                        
                                        state = generate_initial_state(opt=opt, semilla=seed, operadores_activos=operadores)
                                        
                                        problema = ProblemaBicing(initial_state=state)
                                        inici = time.time()
                                        hill_climbing_1 = hill_climbing(problema)
                                        tiempo += time.time() - inici
                                        soluciones_expandidas += problema.solutions_checked
                                        beneficios_tmp.append(hill_climbing_1.heuristic(coste_transporte=params.coste_transporte))
                                    
                                    media_beneficios.append((sum(beneficios_tmp)/iteraciones, tiempo/iteraciones, int(soluciones_expandidas/iteraciones), {k: v for k, v in operadores.items()}))

    media_beneficios.sort(key=lambda x: x[0])
        
    for exp in media_beneficios:
        all_true = True
        for v in exp[3].values():
            if not v:
                all_true = False
                break
        
        if all_true:
            print(f"B: {exp[0]} | T: {exp[1]*1000} ms | Nº: {exp[2]} | OP: ALL TRUE\n")
        else:
            values = ['T' if v else 'F' for v in exp[3].values()]
            print(f"B: {exp[0]} | T: {exp[1]*1000} ms | Nº: {exp[2]} | OP: {values}\n")

    print(f"OPT: {opt} | ITERACIONES: {iteraciones} | HEURÍSTICO: {2 if params.coste_transporte else 1} | SEMILLA: {semilla}\n")

def mejor_initial_state(initial_strategies: list = [0, 1, 2], iteraciones: int = 10) -> None:
    """
    Compara los resultados de los tres métodos de generación de estados iniciales y escribe en pantalla los resultados indicando el mejor de ellos.
    """
    results_accumulated = {strategy: 0 for strategy in initial_strategies}

    for i in range(iteraciones):
        print(f"PROGRESO: {(i/iteraciones)*100}%")
        for strategy in initial_strategies:
            initial_state = generate_initial_state(opt=strategy)
            
            problema_bicing = ProblemaBicing(initial_state)
            final_solution_HC = hill_climbing(problema_bicing)
            
            heuristic_value = final_solution_HC.heuristic(coste_transporte=params.coste_transporte)
            
            results_accumulated[strategy] += heuristic_value

    results_average = {strategy: total/iteraciones for strategy, total in results_accumulated.items()}

    print(f"\nHEURÍSTICO {2 if params.coste_transporte else 1} | {iteraciones} ITERACIONES:")
    for strategy, avg in results_average.items():
        print(f"   * OPT: {strategy} --> BENEFICIO MEDIO: {avg} {'[BEST]' if avg == max(results_average.values()) else ''}")

def comparar_resultados_HC_SA(HC: bool = True, SA: bool = True, iterations: int = 10, opt: int = 2, schedule_sa: Union[None, function] = None) -> None:
    """
    Realiza los experimentos con Hill Climbing y Simulated Annealing y genera las gráficas de los resultados.
    Se pueden desactivar los experimentos que no se quieran realizar.
    """
    assert HC or SA, "Al menos uno de los dos experimentos debe estar activo"
    assert callable(schedule_sa) if SA else True, "Se debe proporcionar una función de schedule para Simulated Annealing"

    tiempos_HC, beneficios_HC, distancias_HC = [], [], []
    tiempos_SA, beneficios_SA, distancias_SA = [], [], []

    for i in range(iterations):
        print(f"PROGRESO: {round((i/iterations)*100, 1)}%", end='\r')
        
        # Generación del estado inicial
        initial_state = generate_initial_state(opt=opt)
        initial_state.heuristic(coste_transporte=params.coste_transporte)
        problema_bicing = ProblemaBicing(initial_state)

        # Experimento con Hill Climbing
        if HC:
            inicio_HC = time.time()
            resultado_HC = hill_climbing(problema_bicing)
            tiempos_HC.append((time.time() - inicio_HC)*1000)
            beneficios_HC.append(resultado_HC.heuristic(coste_transporte=params.coste_transporte))
            distancias_HC.append(sum([resultado_HC.get_distancias_furgoneta(id_f)[2] for id_f in range(params.n_furgonetas)]))

        # Experimento con Simulated Annealing
        if SA:
            inicio_SA = time.time()
            resultado_SA = simulated_annealing(problema_bicing, schedule=schedule_sa)
            tiempos_SA.append((time.time() - inicio_SA)*1000)
            beneficios_SA.append(resultado_SA.heuristic(coste_transporte=params.coste_transporte))
            distancias_SA.append(sum([resultado_SA.get_distancias_furgoneta(id_f)[2] for id_f in range(params.n_furgonetas)]))

    # Generación de los box plots
    labels, beneficios, tiempos, distancias = [], [], [], []

    if HC:
        labels.append('Hill Climbing')
        beneficios.append(beneficios_HC)
        tiempos.append(tiempos_HC)
        distancias.append(distancias_HC)
    
    if SA:
        labels.append('Simulated Annealing')
        beneficios.append(beneficios_SA)
        tiempos.append(tiempos_SA)
        distancias.append(distancias_SA)

    # Gráfico para los beneficios
    plt.boxplot(beneficios, labels=labels)
    plt.title(f"Beneficios totales ({iterations} ejecuciones)")
    plt.ylabel("Beneficio (€)")
    plt.savefig("beneficios.png")
    plt.close()  # Cierra la figura para que podamos crear la siguiente

    # Gráfico para los tiempos
    plt.boxplot(tiempos, labels=labels)
    plt.title(f"Tiempos de ejecución ({iterations} ejecuciones)")
    plt.ylabel("Tiempo (ms)")
    plt.savefig("tiempos.png")
    plt.close()  # Cierra la figura para que podamos crear la siguiente

    # Gráfico para las distancias
    plt.boxplot(distancias, labels=labels)
    plt.title(f"Distancias totales ({iterations} ejecuciones)")
    plt.ylabel("Distancia (km)")
    plt.savefig("distancias.png")
    plt.close()  # Cierra la figura para que podamos crear la siguiente

def encontrar_parametros_SA():
    pass

##############################################################################################################################

# Programa principal
if __name__ == "__main__":

# Experimento individual
    """initial_state: EstadoBicing = generate_initial_state(opt=2)
    initial_state.heuristic(coste_transporte=params.coste_transporte)
    problema_bicing = ProblemaBicing(initial_state)
    tiempo_inicio = time.time()
    final_solution_HC = hill_climbing(problema_bicing)
    tiempo_final = time.time()
    
    initial_state.print_state(inicial=True)
    #initial_state.visualize_state(manhattan = True)
    final_solution_HC.print_state()
    print(f"SOLUCIONES COMPROBADAS: {problema_bicing.solutions_checked}")
    print(f"TIEMPO DE EJECUCIÓN: {1000*(tiempo_final - tiempo_inicio)} ms\n")
    #final_solution_HC.visualize_state(manhattan = True)"""

# Experimentos con operadores:
    """operadores_experimento = {'CambiarEstacionCarga': True, \
                                    'IntercambiarEstacionCarga': True, \
                                        'CambiarOrdenDescarga': True, \
                                            'CambiarEstacionDescarga': True, \
                                                'IntercambiarEstacionDescarga': True, \
                                                    'QuitarEstacionDescarga': True, \
                                                        'ReasignarFurgoneta': True, \
                                                            'ReducirNumeroBicicletasCarga': True}
    
    comparar_operadores_default(opt=1, iteraciones=100, operadores_activos=operadores_experimento)
    comparar_all_operadores(opt=1, semilla=random.randint(0, 1_000_000), iteraciones=100)
    mejor_initial_state(iteraciones=100)"""

# Experimentos de HC vs SA + Obtención de estadísticas y generación de gráficas
    # Schedule para Simulated Annealing
    lam: float = 0.001
    k : float = 25

    def exp_schedule(t, k: float=k, lam: float=lam):
        return k * exp(-lam * t)
    
    # Realizar experimento y generar gráficas
    comparar_resultados_HC_SA(opt=2, HC=True, SA=True, iterations=100, schedule_sa=exp_schedule)
