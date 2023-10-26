from state_bicing import EstadoBicing
from generate_initial_state_bicing import generate_initial_state
from parameters_bicing import params
from problem_bicing import ProblemaBicing
from aima.search import hill_climbing, simulated_annealing
import random
from math import exp
from typing import Union
import time
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from pdb import set_trace as bp

# Declaración de funciones
def comparar_operadores_default(opt: int = 0, iteraciones: int = 10, semilla: Union[int, None] = None, operadores_activos: dict = {operator: True for operator in params.operadores_modificables}) -> None:
    """
    Comparación de los resultados de Hill Climbing con los operadores por defecto y con los operadores modificados introducidos en el parámetro operadores_activos.
    """
    tiempo_default, tiempo_modificado, soluciones_expandidas_default, soluciones_expandidas_modificado = 0, 0, 0, 0
    beneficios_default, beneficios_modificado = [], []
    distancias_default, distancias_modificado = [], []
    rng = random.Random(semilla)

    for i in range(iteraciones):
        print(f"PROGRESO: {round((i/iteraciones)*100, 1)}%", end='\r')
        seed = rng.randint(0, 1_000_000)
        state1 = generate_initial_state(opt=opt, semilla=seed)
        state2 = generate_initial_state(opt=opt, semilla=seed, operadores_activos=operadores_activos)
        
        # Hill Climbing con operadores por defecto
        problema1 = ProblemaBicing(initial_state=state1)
        inici1 = time.time()
        hill_climbing_1 = hill_climbing(problema1)
        tiempo_default += time.time() - inici1
        
        soluciones_expandidas_default += problema1.solutions_checked
        beneficios_default.append(hill_climbing_1.heuristic())
        distancia_total_default = sum([hill_climbing_1.get_distancias_furgoneta(id_f)[2] for id_f in range(params.n_furgonetas)])
        distancias_default.append(distancia_total_default)
        
        # Hill Climbing con operadores modificados
        problema2 = ProblemaBicing(initial_state=state2)
        inici2 = time.time()
        hill_climbing_2 = hill_climbing(problema2)
        tiempo_modificado += time.time() - inici2
        
        soluciones_expandidas_modificado += problema2.solutions_checked
        beneficios_modificado.append(hill_climbing_2.heuristic())
        distancia_total_modificado = sum([hill_climbing_2.get_distancias_furgoneta(id_f)[2] for id_f in range(params.n_furgonetas)])
        distancias_modificado.append(distancia_total_modificado)

    print(f"\nHEURISTIC: {2 if params.coste_transporte else 1} | OPT: {opt} | ITERACIONES: {iteraciones}\n")
    print(f"MEDIA DEFECTO: {sum(beneficios_default)/iteraciones} | TIEMPO DEFAULT: {(tiempo_default/iteraciones)*1000} ms | Nº = {int(soluciones_expandidas_default/iteraciones)} | DISTANCIA DEFAULT: {sum(distancias_default)/iteraciones} | VARIANZA BENEF. DEFAULT: {sum([(beneficio - (sum(beneficios_default)/iteraciones))**2 for beneficio in beneficios_default])/iteraciones}")
    print(f"MEDIA MODIFICADO: {sum(beneficios_modificado)/iteraciones} | TIEMPO MODIFICADO: {(tiempo_modificado/iteraciones)*1000} ms) | Nº = {int(soluciones_expandidas_modificado/iteraciones)} | DISTANCIA MODIFICADO: {sum(distancias_modificado)/iteraciones} | VARIANZA BENEF.MODIFICADO: {sum([(beneficio - (sum(beneficios_modificado)/iteraciones))**2 for beneficio in beneficios_modificado])/iteraciones}\n")

def comparar_all_operadores(opt: int = 0, \
                            iteraciones: int = 10, \
                                semilla: Union[int, None] = None, \
                                    operadores: dict = {operator: True for operator in params.operadores_modificables}) -> None:
    """
    Comprueba todas las posibles combinaciones de operadores y escribe en pantalla los resultados ordenados de mayor a menor beneficio medio.
    """
    # Los únicos operadores que podemos activar/desactivar son CambiarOrdenDescarga, IntercambiarEstacionDescarga, IntercambiarEstacionCarga, ReasignarFurgonetaRandom y ReasignarFurgonetaInformado
    progreso = 0
    media_beneficios = []
    for val4 in [True, False]:
        operadores['ReasignarFurgonetaRandom'] = val4
        for val3 in [True, False]:
            operadores['CambiarOrdenDescarga'] = val3
            for val2 in [True, False]:
                operadores['IntercambiarEstacionCarga'] = val2
                for val1 in [True, False]:
                    operadores['IntercambiarEstacionDescarga'] = val1
                    
                    progreso += 1
                    print(f"PROGRESO: {round((progreso/2**len(operadores))*100, 1)}%", end='\r')
                    
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
                        beneficios_tmp.append(hill_climbing_1.heuristic())
                    
                    media_beneficios.append((sum(beneficios_tmp)/iteraciones, tiempo/iteraciones, int(soluciones_expandidas/iteraciones), {k: v for k, v in operadores.items()}))

    media_beneficios.sort(key=lambda x: (x[0], -x[1]))
        
    for exp in media_beneficios:
        all_true = True
        for v in exp[3].values():
            if not v:
                all_true = False
                break

        if all_true:
            print(f"B: {exp[0]} | T: {exp[1]*1000} ms | Nº: {exp[2]} | OP: ALL TRUE\n")
        else:
            values = [f'{k}: T' if v else f'{k}: F' for k, v in exp[3].items()]
            print(f"B: {exp[0]} | T: {exp[1]*1000} ms | Nº: {exp[2]} | OP: {values}\n")

    print(f"OPT: {opt} | ITERACIONES: {iteraciones} | HEURÍSTICO: {2 if params.coste_transporte else 1}\n")
'''
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
            
            heuristic_value = final_solution_HC.heuristic()
            
            results_accumulated[strategy] += heuristic_value

    results_average = {strategy: total/iteraciones for strategy, total in results_accumulated.items()}

    print(f"\nHEURÍSTICO {2 if params.coste_transporte else 1} | {iteraciones} ITERACIONES:")
    for strategy, avg in results_average.items():
        print(f"   * OPT: {strategy} --> BENEFICIO MEDIO: {avg} {'[BEST]' if avg == max(results_average.values()) else ''}")
    
    # Creación del boxplot
    strategies_names = [str(s) for s in initial_strategies]
    data_to_plot = [results_accumulated[s] for s in initial_strategies]

    fig, ax = plt.subplots()
    ax.boxplot(data_to_plot)

    ax.set_xticklabels(strategies_names)
    ax.set_title('Comparación de Coste Heurístico por Estrategia de Solución Inicial')
    ax.set_xlabel('Estrategias de Solución Inicial')
    ax.set_ylabel('Coste Heurístico')

    plt.savefig('experimento2.png', format='png')  # Guardar gráfico como PNG
    plt.show()'''

def mejor_initial_state(iteraciones: int = 10, semilla_rng: int = random.randint(0, 1000), operadores_activos: dict = {}) -> None:
    # Diccionario de resultados para cada estrategia (0, 1, y 2)
    results_accumulated = {0: [], 1: [], 2: []}  

    for _ in range(iteraciones):
        # Realizamos 5 experimentos para las estrategias 0 y 1
        for strategy in [0, 1]:
            rng = random.Random(semilla_rng)

            resultados_estrategias = []
            for _ in range(5):
                semilla_initial_state = rng.randint(0, 1000)
                initial_state = generate_initial_state(opt=strategy, semilla=semilla_initial_state, operadores_activos=operadores_activos)
                initial_state.heuristic()
                problema_bicing = ProblemaBicing(initial_state)
                final_solution_HC = hill_climbing(problema_bicing)
                beneficio_obtenido = final_solution_HC.heuristic(coste_transporte=params.coste_transporte)
                resultados_estrategias.append(beneficio_obtenido)
            results_accumulated[strategy].append(np.mean(resultados_estrategias))  # Media de los 5 experimentos
        
        # Realizamos un experimento para la estrategia 2
        initial_state = generate_initial_state(opt=2, operadores_activos=operadores_activos)
        problema_bicing = ProblemaBicing(initial_state)
        final_solution_HC = hill_climbing(problema_bicing)
        beneficio_obtenido = final_solution_HC.heuristic(coste_transporte=params.coste_transporte)
        results_accumulated[2].append(beneficio_obtenido)  

    # Calculamos las medias
    results_average = {strategy: np.mean(results) for strategy, results in results_accumulated.items()}

    print(f"\nHEURÍSTICO {2 if params.coste_transporte else 1} | {iteraciones} ITERACIONES:")
    for strategy, avg in results_average.items():
        print(f"   * OPT: {strategy} --> BENEFICIO MEDIO: {avg} {'[BEST]' if avg == max(results_average.values()) else ''}")



def comparar_resultados_HC_SA(HC: bool = True, SA: bool = True, iterations: int = 10, opt: int = 2, schedule_sa = None, beneficios_bool: bool = True, tiempos_bool: bool = True, distancias_bool: bool = True, ocultar_progreso: bool = False) -> Union[None, list]:
    """
    Realiza los experimentos con Hill Climbing y Simulated Annealing y genera las gráficas de los resultados.
    Se pueden desactivar los experimentos que no se quieran realizar.
    """
    assert HC or SA, "Al menos uno de los dos experimentos debe estar activo"
    assert callable(schedule_sa) if SA else True, "Se debe proporcionar una función de schedule para Simulated Annealing"

    tiempos_HC, beneficios_HC, distancias_HC = [], [], []
    tiempos_SA, beneficios_SA, distancias_SA = [], [], []

    for i in range(iterations):
        if not ocultar_progreso:
            print(f"PROGRESO: {round((i/iterations)*100, 1)}%", end='\r')
        
        # Generación del estado inicial
        initial_state = generate_initial_state(opt=opt)
        initial_state.heuristic()
        problema_bicing = ProblemaBicing(initial_state)

        # Experimento con Hill Climbing
        if HC:
            inicio_HC = time.time()
            resultado_HC = hill_climbing(problema_bicing)
            tiempos_HC.append((time.time() - inicio_HC)*1000)
            beneficios_HC.append(resultado_HC.heuristic())
            distancias_HC.append(sum([resultado_HC.get_distancias_furgoneta(id_f)[2] for id_f in range(params.n_furgonetas)]))

        # Experimento con Simulated Annealing
        if SA:
            problema_bicing.mode_simulated_annealing = True # Indicamos al problema que estamos en modo Simulated Annealing
            inicio_SA = time.time()
            resultado_SA = simulated_annealing(problema_bicing, schedule=schedule_sa)
            tiempos_SA.append((time.time() - inicio_SA)*1000)
            beneficios_SA.append(resultado_SA.heuristic())
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
    if beneficios_bool:
        plt.boxplot(beneficios, labels=labels)
        plt.title(f"Beneficios totales ({iterations} ejecuciones)")
        plt.ylabel("Beneficio (€)")
        plt.savefig("beneficios.png")
        plt.close()  # Cierra la figura para que podamos crear la siguiente

    # Gráfico para los tiempos
    if tiempos_bool:
        plt.boxplot(tiempos, labels=labels)
        plt.title(f"Tiempos de ejecución ({iterations} ejecuciones)")
        plt.ylabel("Tiempo (ms)")
        plt.savefig("tiempos.png")
        plt.close()  # Cierra la figura para que podamos crear la siguiente

    # Gráfico para las distancias
    if distancias_bool:
        plt.boxplot(distancias, labels=labels)
        plt.title(f"Distancias totales ({iterations} ejecuciones)")
        plt.ylabel("Distancia (km)")
        plt.savefig("distancias.png")
        plt.close()  # Cierra la figura para que podamos crear la siguiente

    # Devolvemos los beneficios de SA para el experimento 3 (Encontrar los mejores parámetros para Simulated Annealing)
    return beneficios_SA if SA else None

def encontrar_parametros_SA(opt: int = 2, iteraciones_por_valor: int = 10, operadores_activos: dict = {operator: True for operator in params.operadores_modificables}) -> tuple:
    resultados_SA = []

    min_k, max_k, inc_k = 1, 50, 5
    min_lam, max_lam, inc_lam = 0, 0.5, 0.01
    limit = 100

    num_valores_comprobados = round(((max_k-min_k)/inc_k) * ((max_lam-min_lam)/inc_lam))
    num_valor = 0
    for k in np.arange(min_k, max_k, inc_k):
        for lam in np.arange(min_lam, max_lam, inc_lam):
            def exp_schedule(k: float=k, lam: float=lam, limit: int=limit):
                return lambda t: (k * exp(-lam * t)) if t < limit else 0
            
            num_valor += 1
            print(f"PROGRESO: [{num_valor}/{num_valores_comprobados}]", end='\r')
            resultados_iteraciones = comparar_resultados_HC_SA(HC=False, SA=True, iterations=iteraciones_por_valor, opt=opt, schedule_sa=exp_schedule(), beneficios_bool=False, tiempos_bool=False, distancias_bool=False, ocultar_progreso=True)
            promedio_iteraciones = sum(resultados_iteraciones)/iteraciones_por_valor
            resultados_SA.append((promedio_iteraciones, k, lam))

    print("TODOS LOS VALORES COMPORBADOS, GENERANDO GRÁFICOS...")
    
    # Nos quedamos con el mejor resultado
    mejor_resultado = max(resultados_SA, key=lambda x: x[0])
    best_k, best_lambda = mejor_resultado[1], mejor_resultado[2]

    # Generar el gráfico 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extract k, lambda and results from resultados_SA
    ks = [res[1] for res in resultados_SA]
    lambdas = [res[2] for res in resultados_SA]
    results = [res[0] for res in resultados_SA]

    # Assuming results are positive, you can set bottom to 0 for simplicity.
    bottom = np.zeros_like(results)

    # Define bar width and depth. You may need to adjust these depending on the granularity of your data.
    width = depth = 5

    ax.bar3d(ks, lambdas, bottom, width, depth, results)

    ax.set_xlabel('K')
    ax.set_ylabel('λ')
    ax.set_zlabel('Beneficio (€)')
    ax.set_title('Variación del beneficio para SA para varios valores de k y λ')
    plt.savefig("parametros_SA.png")
    plt.close()

    return best_k, best_lambda, limit


##############################################################################################################################

# Programa principal
if __name__ == "__main__":

# Pruebas individuales
    """initial_state: EstadoBicing = generate_initial_state(opt=2)
    initial_state.heuristic()
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

# Pruebas con operadores:
    """operadores_experimento = {'CambiarOrdenDescarga': True, \
                              'IntercambiarEstacionDescarga': True, \
                                'IntercambiarEstacionCarga': True, \
                                    'ReasignarFurgonetaInformado': False}
    
    comparar_operadores_default(opt=2, iteraciones=1, operadores_activos=operadores_experimento)"""
    

# Experimento 1 ----------------------------------------------------------------------------------
    #comparar_all_operadores(opt=0, semilla=random.randint(0, 1_000_000), iteraciones=10)

    operadores_exp1: dict = {}
# Experimento 2 ----------------------------------------------------------------------------------
    mejor_initial_state(iteraciones=50, semilla_rng=50, operadores_activos=operadores_exp1)

    opt_exp2: int = 

# Experimento 3 ----------------------------------------------------------------------------------
    k, lam, limit = encontrar_parametros_SA(opt=opt_exp2, iteraciones_por_valor=1)

    def exp_schedule(k: float=k, lam: float=lam, limit: int=limit):
        return lambda t: (k * exp(-lam * t)) if t < limit else 0
    
    comparar_resultados_HC_SA(opt=2, HC=True, SA=True, iterations=50, schedule_sa=exp_schedule())

# Experimento 4 ----------------------------------------------------------------------------------
    

# Experimento 5 ----------------------------------------------------------------------------------


# Experimento 6 ----------------------------------------------------------------------------------


# Experimento Especial ---------------------------------------------------------------------------
    #comparar_resultados_HC_SA(opt=2, HC=True, SA=False, iterations=100)
