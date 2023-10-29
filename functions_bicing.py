from aima.search import hill_climbing, simulated_annealing
from generate_initial_state_bicing import generate_initial_state
from parameters_bicing import params
from problem_bicing import ProblemaBicing
from state_bicing import EstadoBicing

import random
import time
import numpy as np
from typing import Union
from math import exp
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

def ejecucion_individual_HC(opt: int = 2, \
                            semilla: int = 42, \
                                operadores_activos: dict = {operator: True for operator in params.operadores_modificables}) -> None:
    params.actualizar_semilla(semilla=semilla)
    
    initial_state: EstadoBicing = generate_initial_state(opt=opt, operadores_activos=operadores_activos)
    initial_state.heuristic()
    problema_bicing = ProblemaBicing(initial_state)
    tiempo_inicio = time.time()
    final_solution_HC = hill_climbing(problema_bicing)
    tiempo_final = time.time()

    initial_state.print_state(inicial=True)
    initial_state.visualize_state(manhattan = True)
    final_solution_HC.print_state()
    print(f"SOLUCIONES COMPROBADAS: {problema_bicing.solutions_checked}")
    print(f"TIEMPO DE EJECUCIÓN: {1000*(tiempo_final - tiempo_inicio)} ms\n")
    final_solution_HC.visualize_state(manhattan = True)

def comparar_operadores_default(opt: int = 0, \
                                iteraciones: int = 15, \
                                    semilla: Union[int, None] = None, \
                                        operadores_activos: dict = {operator: True for operator in params.operadores_modificables}) -> None:
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
        state1 = generate_initial_state(opt=opt, semilla_rng=seed)
        state2 = generate_initial_state(opt=opt, semilla_rng=seed, operadores_activos=operadores_activos)
        
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
                            iteraciones_por_semilla: int = 15, \
                                lista_semillas: list = [42]) -> None:
    """
    Comprueba todas las posibles combinaciones de operadores y escribe en pantalla los resultados ordenados de mayor a menor beneficio medio.
    """
    # Los únicos operadores que podemos activar/desactivar son CambiarOrdenDescarga, IntercambiarEstacionDescarga, IntercambiarEstacionCarga, ReasignarFurgonetaRandom y ReasignarFurgonetaInformado
    progreso = 0
    media_beneficios = []
    operadores: dict = {operator: True for operator in params.operadores_modificables}

    # Fijamos las semillas para que los resultados sean comparables
    semillas_initial_state = [random.randint(0, 1000) for _ in range(iteraciones_por_semilla)]

    for val4 in [True, False]:
        operadores['ReasignarFurgonetaInformado'] = val4
        for val3 in [True, False]:
            operadores['CambiarOrdenDescarga'] = val3
            for val2 in [True, False]:
                operadores['IntercambiarEstacionCarga'] = val2
                for val1 in [True, False]:
                    operadores['IntercambiarEstacionDescarga'] = val1
                    
                    progreso += 1
                    print(f"PROGRESO: {round((progreso/2**len(operadores))*100, 1)}%", end='\r')

                    benef_conjunto = 0
                    tiempo_conjunto = 0
                    
                    for semilla in lista_semillas:
                        params.actualizar_semilla(semilla=semilla)
                        
                        beneficios_semilla = 0
                        tiempo_semilla = 0
                        for i in range(iteraciones_por_semilla):
                            initial_state = generate_initial_state(opt=opt, semilla_rng=semillas_initial_state[i], operadores_activos=operadores)
                            initial_state.heuristic()
                            problema = ProblemaBicing(initial_state=initial_state)
    
                            inici = time.time()
                            hill_climbing_1 = hill_climbing(problema)
                            tiempo_semilla += time.time() - inici
                            beneficios_semilla += hill_climbing_1.heuristic()                          
    
                        benef_conjunto += beneficios_semilla/iteraciones_por_semilla
                        tiempo_conjunto += tiempo_semilla/iteraciones_por_semilla
                    
                    media_beneficios.append((benef_conjunto/len(lista_semillas), tiempo_conjunto/len(lista_semillas), {k: v for k, v in operadores.items()}))
    
    # Ordenamos los resultados por beneficio medio  
    media_beneficios.sort(key=lambda x: (x[0], -x[1]))
        
    for conjunto in media_beneficios:
        all_true = True
        for v in conjunto[2].values():
            if not v:
                all_true = False
                break

        if all_true:
            print(f"B: {conjunto[0]} | T: {conjunto[1]*1000} ms | OP: ALL TRUE\n")
        else:
            values = [f'{k}: T' if v else f'{k}: F' for k, v in conjunto[2].items()]
            print(f"B: {conjunto[0]} | T: {conjunto[1]*1000} ms | OP: {values}\n")

    print(f"OPT: {opt} | ITERACIONES POR CONJUNTO DE OPERADORES: {iteraciones_por_semilla} | HEURÍSTICO: {2 if params.coste_transporte else 1}\n")
    print(f"SEMILLAS USADAS: {lista_semillas}\n")

def mejor_initial_state(iteraciones_estrategias_aleatorias: int = 5, \
                            lista_semillas: list = [42], \
                                operadores_activos: dict = {}) -> None:
        
    # Diccionario de resultados para cada estrategia (0, 1, y 2)
    results_accumulated = {0: [], 1: [], 2: []}
    progreso = 0  

    for semilla in lista_semillas:
        params.actualizar_semilla(semilla=semilla)
        
        # Realizamos 5 experimentos para las estrategias 0 y 1
        for strategy in [0, 1]:
            resultados_estrategias = []
            for _ in range(iteraciones_estrategias_aleatorias):
                progreso +=1
                print(f"PROGRESO: {progreso}/{len(lista_semillas) * iteraciones_estrategias_aleatorias * 2}", end='\r')
                initial_state = generate_initial_state(opt=strategy, operadores_activos=operadores_activos)
                initial_state.heuristic()
    
                problema_bicing = ProblemaBicing(initial_state)
                final_solution_HC = hill_climbing(problema_bicing)
                
                beneficio_obtenido = final_solution_HC.heuristic()
                resultados_estrategias.append(beneficio_obtenido)
            
            results_accumulated[strategy].append(np.mean(resultados_estrategias))  # Media de los 5 experimentos
        
        # Realizamos un experimento para la estrategia 2
        initial_state = generate_initial_state(opt=2, operadores_activos=operadores_activos)
        problema_bicing = ProblemaBicing(initial_state)
        final_solution_HC = hill_climbing(problema_bicing)
        beneficio_obtenido = final_solution_HC.heuristic()
        results_accumulated[2].append(beneficio_obtenido)

    # Calculamos las medias
    results_average = {strategy: np.mean(results) for strategy, results in results_accumulated.items()}

    print(f"\nHEURÍSTICO: {2 if params.coste_transporte else 1} |  ITERACIONES POR ESTRATEGIA: {iteraciones_estrategias_aleatorias}\n")
    for strategy, avg in results_average.items():
        print(f"   * OPT: {strategy} --> BENEFICIO MEDIO: {avg} {'[BEST]' if avg == max(results_average.values()) else ''}")
    
    print(f"\nSEMILLAS USADAS Y MEDIAS DE LAS ESTRATEGIAS:")
    for i, semilla in enumerate(lista_semillas):
        print(f"   * SEMILLA: {semilla}  ----->  EST. 0: {results_accumulated[0][i]} | EST. 1: {results_accumulated[1][i]} | EST. 2: {results_accumulated[2][i]}")

    # Crear la figura
    plt.figure(figsize=(10, 6))

    # Trazar los datos para cada estrategia
    for strategy, results in results_accumulated.items():
        plt.plot(results, label=f'Estrategia {strategy}')

    # Etiquetas y título
    plt.xlabel('Réplicas')
    plt.ylabel('Beneficio (€)')
    plt.title(f'Evolución del beneficio por estrategia ({len(lista_semillas)} réplicas)')
    plt.legend()
    plt.savefig("experimento2.png")

def comparar_resultados_HC_SA(HC: bool = True, \
                              SA: bool = True, \
                                lista_semillas: list = [42], \
                                    opt: int = 2, \
                                        operadores_activos: dict = {operator: True for operator in params.operadores_modificables}, \
                                            k: float = 1, \
                                                lam: float = 0.01, \
                                                    limit: int = 1000, \
                                                        beneficios_bool: bool = True, \
                                                            tiempos_bool: bool = True, \
                                                                distancias_bool: bool = True, \
                                                                    mostrar_progreso: bool = True, \
                                                                        iteraciones_por_replica: int = 10, \
                                                                            coste_transporte: bool = True) -> Union[None, list]:
    """
    Realiza los experimentos con Hill Climbing y Simulated Annealing y genera las gráficas de los resultados.
    Se pueden desactivar los experimentos que no se quieran realizar.
    """
    assert HC or SA, "Al menos uno de los dos experimentos debe estar activo"

    if coste_transporte:
        params.coste_transporte=True
    else:
        params.coste_transporte=False

    tiempos_HC, beneficios_HC, distancias_HC = [], [], []
    tiempos_SA, beneficios_SA, distancias_SA = [], [], []

    def exp_schedule(k=k, lam=lam, limit=limit):
        return lambda t: (k * exp(-lam * t)) if t < limit else 0

    for i, semilla in enumerate(lista_semillas):
        params.actualizar_semilla(semilla=semilla)
        
        if mostrar_progreso:
            print(f"PROGRESO: {round((i/len(lista_semillas))*100, 1)}%", end='\r')

        for _ in range(iteraciones_por_replica):    
            # Generación del estado inicial
            initial_state = generate_initial_state(opt=opt, operadores_activos=operadores_activos)
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
                resultado_SA = simulated_annealing(problema_bicing, schedule=exp_schedule())
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
        labels.append(f'Simulated Annealing\n(k={k}, λ={lam}, limit={limit})')
        beneficios.append(beneficios_SA)
        tiempos.append(tiempos_SA)
        distancias.append(distancias_SA)

    # Gráfico para los beneficios
    if beneficios_bool:
        plt.boxplot(beneficios, labels=labels)
        plt.title(f"Beneficios totales {'H2' if params.coste_transporte else 'H1'} ({len(lista_semillas)} réplicas)")
        plt.ylabel("Beneficio (€)")
        if params.coste_transporte:
            plt.savefig("beneficios_h2.png")
        else:
            plt.savefig("beneficios_h1.png")        
        plt.close()  # Cierra la figura para que podamos crear la siguiente

    # Gráfico para los tiempos
    if tiempos_bool:
        plt.boxplot(tiempos, labels=labels)
        plt.title(f"Tiempos de ejecución {'H2' if params.coste_transporte else 'H1'} ({len(lista_semillas)} réplicas)")
        plt.ylabel("Tiempo (ms)")
        if params.coste_transporte:
            plt.savefig("tiempos_h2.png")
        else:
            plt.savefig("tiempos_h1.png")        
        plt.close()  # Cierra la figura para que podamos crear la siguiente

    # Gráfico para las distancias
    if distancias_bool:
        plt.boxplot(distancias, labels=labels)
        plt.title(f"Distancias totales {'H2' if params.coste_transporte else 'H1'} ({len(lista_semillas)} réplicas)")
        plt.ylabel("Distancia (km)")
        if params.coste_transporte:
            plt.savefig("distancias_h2.png")
        else:
            plt.savefig("distancias_h1.png")
        plt.close()  # Cierra la figura para que podamos crear la siguiente

    # Devolvemos los beneficios de SA para el experimento 3 (Encontrar los mejores parámetros para Simulated Annealing)
    return beneficios_SA if SA and not HC else None

def encontrar_parametros_SA(opt: int = 2, \
                                iteraciones_por_semilla: int = 3, \
                                    valores_k: list = [1, 5, 25, 125], \
                                        valores_lam: list = [0.0001, 0.01, 1], \
                                            limit: int = 1000, \
                                                lista_semillas: list = [42], \
                                                    operadores_activos: dict = {operator: True for operator in params.operadores_modificables}) -> None:
    
    resultados_SA = []
    progreso = 0

    for k in valores_k:
        for lam in valores_lam:
            progreso += 1
            print(f"PROGRESO: {progreso}/{len(valores_k)*len(valores_lam)}", end='\r')
            
            def exp_schedule(k: float=k, lam: float=lam, limit: int=limit):
                return lambda t: (k * exp(-lam * t)) if t < limit else 0
            
            promedio_semillas = 0
            for semilla in lista_semillas:
                params.actualizar_semilla(semilla=semilla)
            
                resultados_iteraciones = comparar_resultados_HC_SA(HC=False, \
                                                                SA=True, \
                                                                    iterations=iteraciones_por_semilla, \
                                                                        opt=opt, \
                                                                            operadores_activos=operadores_activos, \
                                                                                schedule_sa=exp_schedule(), \
                                                                                    beneficios_bool=False, \
                                                                                        tiempos_bool=False, \
                                                                                            distancias_bool=False, \
                                                                                                mostrar_progreso=False)
                promedio_semillas += sum(resultados_iteraciones)/iteraciones_por_semilla
            resultados_SA.append((promedio_semillas/len(lista_semillas), k, lam))

    # Nos quedamos con el mejor resultado
    mejor_resultado = max(resultados_SA, key=lambda x: x[0])

    # Valores únicos de k y lambda
    k_values = sorted(set(k for _, k, _ in resultados_SA))
    lam_values = sorted(set(lam for _, _, lam in resultados_SA))

    # Inicializar matriz de ceros
    matrix = np.zeros((len(k_values), len(lam_values)))

    # Poblar la matriz con los datos
    for beneficio, k, lam in resultados_SA:
        i = k_values.index(k)
        j = lam_values.index(lam)
        matrix[i, j] = beneficio

    # Verificar la matriz
    for i, k in enumerate(k_values):
        for j, lam in enumerate(lam_values):
            print(f"k={k}, λ={lam} --> Beneficio: {matrix[i, j]}")

    # Crear la figura y los ejes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Generar coordenadas para cada barra
    _x = np.arange(len(k_values))
    _y = np.arange(len(lam_values))
    _xx, _yy = np.meshgrid(_x, _y)
    x, y = _xx.ravel(), _yy.ravel()

    # Valores de z (beneficio)
    z = matrix.T.ravel()

    # Definir el ancho, la profundidad y la altura de cada barra
    dx = dy = 0.45

    # Mapa de colores
    colors = ['r', 'g', 'b', 'y', 'c', 'm']
    num_lam_values = len(lam_values)
    colors = colors * (num_lam_values // len(colors) + 1)

    # Obtener los índices en orden descendente basado en z
    sorted_indices = np.argsort(z)[::-1]

    # Crear el gráfico de barras con colores distintos para cada fila de lambda usando los índices ordenados
    for idx in sorted_indices:
        color_idx = int(_yy.ravel()[idx])
        ax.bar3d(x[idx], y[idx], 0, dx, dy, z[idx] if z[idx] > 0 else 0, shade=True, color=colors[color_idx])

    # Etiquetas para los ejes
    ax.set_xticks(_x + dx/2)
    ax.set_yticks(_y + dy/2)
    ax.set_xticklabels(k_values)
    ax.set_yticklabels(lam_values)
    ax.set_xlabel('K')
    ax.set_ylabel('λ')
    ax.set_zlabel('Beneficio (€)')

    plt.savefig('parametros_SA.png')
    plt.close()

    print("\nMEJORES RESULTADOS:")
    for resultado in resultados_SA:
        if resultado[0] == mejor_resultado[0]:
            print(f"   * K={resultado[1]}, λ={resultado[2]} --> Beneficio: {resultado[0]}\n")

    print(f"SEMILLAS USADAS: {lista_semillas}\n")

def tiempos_experimento_con_aumento(opt: int = 2, \
                                    operadores_activos: dict = {operator: True for operator in params.operadores_modificables}, \
                                        incremento_estaciones: int = 25, \
                                            incremento_furgonetas: int = 5, \
                                                incremento_bicicletas: int = 1250, \
                                                    n_incrementos: int = 5,
                                                        lista_semillas: list = [42]) -> None:
    """
    Realiza múltiples ejecuciones de Hill Climbing con un incremento progresivo de estaciones, furgonetas y bicicletas.
    """
    tiempo_resultados = []
    progreso = 0

    for _ in range(n_incrementos):
        tiempos_tanda = []
        for semilla in lista_semillas:
            params.actualizar_semilla(semilla=semilla)

            progreso += 1
            print(f"PROGRESO: {progreso}/{n_incrementos*len(lista_semillas)}", end='\r')

            initial_state = generate_initial_state(opt=opt, operadores_activos=operadores_activos)
            initial_state.heuristic()
            problema_aumento = ProblemaBicing(initial_state=initial_state)

            tiempo_inicio = time.time()
            hill_climbing(problema_aumento)
            tiempo_final = time.time()

            tiempos_tanda.append(tiempo_final - tiempo_inicio)

        tiempo_resultados.append({'t': (sum(tiempos_tanda)/len(lista_semillas))*1000, 'e': params.n_estaciones, 'f': params.n_furgonetas, 'b': params.n_bicicletas})

        params.actualizar_estaciones(n_estaciones=params.n_estaciones + incremento_estaciones, \
                                        n_furgonetas=params.n_furgonetas + incremento_furgonetas, \
                                            n_bicicletas=params.n_bicicletas + incremento_bicicletas)
        
        
    print("\nRESULTADOS:")
    for resultado in tiempo_resultados:
        print(f"   * E: {resultado['e']} | F: {resultado['f']} | B: {resultado['b']} | T: {resultado['t']} ms")
    
    print(f"\nHEURÍSTICO: {2 if params.coste_transporte else 1} |  RÉPLICAS: {len(lista_semillas)} | OPT: {opt}\n")

    # Generamos el gráfico de la evolución de los tiempos
    plt.figure(figsize=(10, 7))
    plt.subplots_adjust(bottom=0.2)
    plt.plot([resultado['t'] for resultado in tiempo_resultados])
    plt.title(f"Evolución del tiempo de ejecución medio ({len(lista_semillas)} réplicas por incremento)")
    labels = [f"E = {resultado['e']}\nF = {resultado['f']}\nB = {resultado['b']}" for resultado in tiempo_resultados]
    plt.xticks(range(n_incrementos), labels)
    plt.xlabel("Número de estaciones (E), furgonetas (F) y bicicletas (B)")
    plt.ylabel("Tiempo (ms)")
    plt.savefig("evolucion_tiempos_aumento.png")
    plt.close()

def augmento_furgonetas(opt: int = 2, 
                                operadores_activos: dict = {operator: True for operator in params.operadores_modificables}, 
                                incremento_furgonetas: int = 5, 
                                n_incrementos: int = 5,
                                lista_semillas: list = [42]) -> None:
    """
    Realiza múltiples ejecuciones de Hill Climbing con un incremento progresivo de furgonetas.
    """
    beneficio_resultados = []
    progreso = 0

    for _ in range(n_incrementos):
        beneficios_tanda = []
        for semilla in lista_semillas:
            params.actualizar_semilla(semilla=semilla)
            progreso += 1
            print(f"PROGRESO: {progreso}/{n_incrementos*len(lista_semillas)}", end='\r')

            initial_state = generate_initial_state(opt=opt, operadores_activos=operadores_activos)
            initial_state.heuristic()
            problema_aumento = ProblemaBicing(initial_state=initial_state)

            HC = hill_climbing(problema_aumento)

            beneficios_tanda.append(HC.heuristic())

        beneficio_resultados.append({'b': (sum(beneficios_tanda)/len(lista_semillas)), 'f': params.n_furgonetas})
        params.actualizar_estaciones(n_estaciones=params.n_estaciones, \
                                                    n_furgonetas=params.n_furgonetas + incremento_furgonetas, \
                                                    n_bicicletas=params.n_bicicletas)
    print("\nRESULTADOS:")
    for resultado in beneficio_resultados:
        print(f"   * F: {resultado['f']} | B: {resultado['b']} euros")

    print(f"\nHEURÍSTICO: {2 if params.coste_transporte else 1} | OPT: {opt}\n")

    # Generamos el gráfico de la evolución de los tiempos
    plt.plot([resultado['b'] for resultado in beneficio_resultados])
    plt.title(f"Beneficio por número de furgonetas ({len(lista_semillas)} réplicas por incremento)")
    labels = [f"F = {resultado['f']}" for resultado in beneficio_resultados]
    plt.xticks(range(n_incrementos), labels)
    plt.xlabel("Número de furgonetas (F)")
    plt.ylabel("Beneficio (€)")
    plt.savefig("beneficio_respecto_furgonetas.png")
    plt.close()

