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
                                                                                    'ReasignarFurgoneta'}}) -> None:

    tiempo_default, tiempo_modificado = 0, 0
    beneficios_default, beneficios_modificado = [], []

    for _ in range(iteraciones):
        rng = random.Random(semilla)
        seed = rng.randint(0, 1_000_000)
        
        state1 = generate_initial_state(opt=opt, semilla=seed)
        state2 = generate_initial_state(opt=opt, semilla=seed, operadores_activos=operadores_activos)
        
        inici = time.time()
        hill_climbing_1 = hill_climbing(ProblemaBicing(initial_state=state1))
        tiempo_default += time.time() - inici
        beneficios_default.append(hill_climbing_1.heuristic(coste_transporte=params.coste_transporte))
        
        inici = time.time()
        hill_climbing_2 = hill_climbing(ProblemaBicing(initial_state=state2))
        tiempo_modificado += time.time() - inici
        beneficios_modificado.append(hill_climbing_2.heuristic(coste_transporte=params.coste_transporte))
        
    print(f"\nMEDIA DEFECTO: {sum(beneficios_default)/iteraciones} | TIEMPO DEFAULT: {tiempo_default/iteraciones} s | VARIANZA DEFAULT: {sum([(beneficio - (sum(beneficios_default)/iteraciones))**2 for beneficio in beneficios_default])/iteraciones}")
    print(f"MEDIA MODIFICADO: {sum(beneficios_modificado)/iteraciones} | TIEMPO MODIFICADO: {tiempo_modificado/iteraciones} s) | VARIANZA MODIFICADO: {sum([(beneficio - (sum(beneficios_modificado)/iteraciones))**2 for beneficio in beneficios_modificado])/iteraciones}\n")

def comparar_operadores(opt: int = 0, iteraciones: int = 10, semilla: Union[int, None] = None, operadores: dict = {operator: True for operator in {'CambiarEstacionCarga', \
                                                            'IntercambiarEstacionCarga', \
                                                                'CambiarOrdenDescarga', \
                                                                    'CambiarEstacionDescarga', \
                                                                        'IntercambiarEstacionDescarga', \
                                                                            'QuitarEstacionDescarga', \
                                                                                'ReasignarFurgoneta'}}) -> None:

    progreso = 0
    media_beneficios = []

    operadores['CambiarEstacionCarga'] = True
    for _ in range(2):
        operadores['IntercambiarEstacionCarga'] = True
        for _ in range(2):
            operadores['CambiarOrdenDescarga'] = True
            for _ in range(2):
                operadores['CambiarEstacionDescarga'] = True
                for _ in range(2):
                    operadores['IntercambiarEstacionDescarga'] = True
                    for _ in range(2):
                        operadores['QuitarEstacionDescarga'] = True
                        for _ in range(2):
                            operadores['ReasignarFurgoneta'] = True
                            for _ in range(2):
                                progreso += 1
                                print(f"PROGRESO: {(progreso/128)*100}%")
                                
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
                                
                                operadores['ReasignarFurgoneta'] = False
                            operadores['QuitarEstacionDescarga'] = False
                        operadores['IntercambiarEstacionDescarga'] = False
                    operadores['CambiarEstacionDescarga'] = False
                operadores['CambiarOrdenDescarga'] = False
            operadores['IntercambiarEstacionCarga'] = False
        operadores['CambiarEstacionCarga'] = False

    media_beneficios.sort(key=lambda x: x[0])
        
    for exp in media_beneficios:
        all_true = True
        for v in exp[3].values():
            if not v:
                all_true = False
                break
        
        if all_true:
            print(f"B: {exp[0]} | T: {exp[1]} | Nº: {exp[2]} | OP: ALL TRUE\n")
        else:
            values = ['T' if v else 'F' for v in exp[3].values()]
            print(f"B: {exp[0]} | T: {exp[1]} | Nº: {exp[2]} | OP: {values}\n")

    print(f"OPT: {opt} | ITERACIONES: {iteraciones} | HEURISTIC: {2 if params.coste_transporte else 1} | SEMILLA: {semilla}\n")

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
    tiempo_inicio = time.time()
    initial_state: EstadoBicing = generate_initial_state(opt = 2)
    problema_bicing = ProblemaBicing(initial_state)
    final_solution_HC = hill_climbing(problema_bicing)
    initial_state.heuristic(coste_transporte=params.coste_transporte)
    tiempo_final = time.time()
    
    initial_state.print_state(inicial=True)
    initial_state.visualize_state(manhattan = True)
    final_solution_HC.print_state()
    print(f"SOLUCIONES COMPROBADAS: {problema_bicing.solutions_checked}")
    print(f"TIEMPO DE EJECUCIÓN: {tiempo_final - tiempo_inicio} s\n")
    final_solution_HC.visualize_state(manhattan = True)"""

# Experimentos con operadores:
    """operadores_experimento = {'CambiarEstacionCarga': True, \
                                    'IntercambiarEstacionCarga': True, \
                                        'CambiarOrdenDescarga': True, \
                                            'CambiarEstacionDescarga': True, \
                                                'IntercambiarEstacionDescarga': True, \
                                                    'QuitarEstacionDescarga': True, \
                                                        'ReasignarFurgoneta': True}
    
    #comparar_resultados(opt=2, iteraciones=10, operadores_activos=operadores_experimento)
    #comparar_operadores(opt=1, semilla=random.randint(0, 1_000_000), iteraciones=100)
    #mejor_initial_state(iteraciones=100)"""

# Obtener estadísticas y generar un box plot
    """times_hill_climbing = [timeit(lambda: hill_climbing(problema_bicing), number=1) for _ in range(15)]
    times_simulated_annealing = [timeit(lambda: simulated_annealing(problema_bicing), number=1) for _ in range(15)]
    
    data_to_plot = [times_hill_climbing, times_simulated_annealing]
    labels=['hill_climbing', 'simulated_annealing']
        
    plt.boxplot(data_to_plot, labels=labels)
    plt.ylabel('Tiempo de ejecución (s)')
    plt.title('Comparativa de Hill Climning y Simulated Annealing con Boxplots')
    plt.savefig('test.png')"""

# Obtener estadísticas y generar un line plot
    """hill_climbing_value = None # HEM DE FER QUE HILL CLIMBING VALUE --> returns a list of objective function values over iterations:
    
    plt.figure(figsize=(10, 6))  # Tamaño de la figura
    plt.plot(hill_climbing_value, marker='o', linestyle='-')  # Creamos el gráfico
    plt.title("Progreso de Hill Climbing") 
    plt.xlabel("Iteraciones")  
    plt.ylabel("Coste")  
    plt.grid(True)  # Añadimos grid para una mejor ínterpretación"""

