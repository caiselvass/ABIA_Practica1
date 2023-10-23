from state_bicing import EstadoBicing
from generate_initial_state_bicing import generate_initial_state
from parameters_bicing import params
from problem_bicing import ProblemaBicing
from aima.search import hill_climbing, simulated_annealing
import random
from typing import Union
from timeit import timeit
import time
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# Declaración de funciones
def comparar_resultados(opt: int = 0, iteraciones: int = 10, semilla: Union[int, None] = None, operadores_activos: dict = {operator: True for operator in {'CambiarEstacionCarga', \
                                                               'CambiarEstacionCarga', \
                                                                'IntercambiarEstacionCarga', \
                                                                    'CambiarOrdenDescarga', \
                                                                        'CambiarEstacionDescarga', \
                                                                            'IntercambiarEstacionDescarga', \
                                                                                'QuitarEstacionDescarga', \
                                                                                    'ReasignarFurgoneta', \
                                                                                        'ReducirNumeroBicicletasCarga'}}) -> None:

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

def comparar_operadores(opt: int = 0, iteraciones: int = 10, semilla: Union[int, None] = None, operadores: dict = {operator: True for operator in {'CambiarEstacionCarga', \
                                                            'IntercambiarEstacionCarga', \
                                                                'CambiarOrdenDescarga', \
                                                                    'CambiarEstacionDescarga', \
                                                                        'IntercambiarEstacionDescarga', \
                                                                            'QuitarEstacionDescarga', \
                                                                                'ReasignarFurgoneta', \
                                                                                    'ReducirNumeroBicicletasCarga'}}) -> None:

    progreso = 0
    media_beneficios = []

    for val8 in [True, False]:
        operadores['ReducirNumeroBicicletasCarga'] = val8
        for val7 in range(2):
            operadores['CambiarEstacionCarga'] = val7
            for val6 in range(2):
                operadores['IntercambiarEstacionCarga'] = val6
                for val5 in range(2):
                    operadores['CambiarOrdenDescarga'] = val5
                    for val4 in range(2):
                        operadores['CambiarEstacionDescarga'] = val4
                        for val3 in range(2):
                            operadores['IntercambiarEstacionDescarga'] = val3
                            for val2 in range(2):
                                operadores['QuitarEstacionDescarga'] = val2
                                for val1 in range(2):
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

##############################################################################################################################

# Programa principal
if __name__ == "__main__":

# Experimento
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
    operadores_experimento = {'CambiarEstacionCarga': True, \
                                    'IntercambiarEstacionCarga': True, \
                                        'CambiarOrdenDescarga': True, \
                                            'CambiarEstacionDescarga': True, \
                                                'IntercambiarEstacionDescarga': True, \
                                                    'QuitarEstacionDescarga': True, \
                                                        'ReasignarFurgoneta': True, \
                                                            'ReducirNumeroBicicletasCarga': True}
    
    #comparar_resultados(opt=1, iteraciones=100, operadores_activos=operadores_experimento)
    #comparar_operadores(opt=1, semilla=random.randint(0, 1_000_000), iteraciones=100)
    #mejor_initial_state(iteraciones=100)

# Obtener estadísticas y generar un box plot
    iterations_plot = 100
    times_HC, benefits_HC, distances_HC = [], [], []
    times_SA, benefits_SA, distances_SA = [], [], []
    for i in range(iterations_plot):
        print(f"PROGRESO: {(i/iterations_plot)*100}%", end='\r')
        initial_state = generate_initial_state(opt=2)
        initial_state.heuristic(coste_transporte=params.coste_transporte)
        problema_bicing = ProblemaBicing(initial_state)

        
        inicio = time.time()
        resultado_HC = hill_climbing(problema_bicing)
        times_HC.append((time.time() - inicio)*1000)
        benefits_HC.append(resultado_HC.heuristic(coste_transporte=params.coste_transporte))
        distances_HC.append(sum([resultado_HC.get_distancias_furgoneta(id_f)[2] for id_f in range(params.n_furgonetas)]))

        #inicio = time.time()
        #resultado_SA = simulated_annealing(problema_bicing)
        #times_SA.append(time.time() - inicio)
        #benefits_SA.append(resultado_SA.heuristic(coste_transporte=params.coste_transporte))
        #distances_SA.append(sum([resultado_SA.get_distancias_furgoneta(id_f)[2] for id_f in range(params.n_furgonetas)]))

    # Gráfico para beneficios
    plt.boxplot(benefits_HC)
    plt.title(f"Boxplot de los beneficios con Hill Climbing ({iterations_plot} iteraciones)")
    plt.ylabel("Beneficio (€)")
    plt.savefig("beneficios.png")
    plt.close()  # Cierra la figura para que podamos crear la siguiente

    # Gráfico para tiempos
    plt.boxplot(times_HC)
    plt.title(f"Boxplot de los tiempos con Hill Climbing ({iterations_plot} iteraciones)")
    plt.ylabel("Tiempo (ms)")
    plt.savefig("tiempos.png")
    plt.close()  # Cierra la figura para que podamos crear la siguiente

    # Gráfico para distancias
    plt.boxplot(distances_HC)
    plt.title(f"Boxplot de las distancias totales con Hill Climbing ({iterations_plot} iteraciones)")
    plt.ylabel("Distancia (km)")
    plt.savefig("distancias.png")
    plt.close()  # Cierra la figura para que podamos crear la siguiente


# Obtener estadísticas y generar un line plot
    """hill_climbing_value = None # HEM DE FER QUE HILL CLIMBING VALUE --> returns a list of objective function values over iterations:
    
    plt.figure(figsize=(10, 6))  # Tamaño de la figura
    plt.plot(hill_climbing_value, marker='o', linestyle='-')  # Creamos el gráfico
    plt.title("Progreso de Hill Climbing") 
    plt.xlabel("Iteraciones")  
    plt.ylabel("Coste")  
    plt.grid(True)  # Añadimos grid para una mejor ínterpretación"""