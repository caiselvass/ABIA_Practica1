from functions_bicing import comparar_all_operadores, mejor_initial_state, encontrar_parametros_SA ,comparar_resultados_HC_SA, tiempos_experimento_con_aumento
from math import exp
import random
from generate_initial_state_bicing import *
from problem_bicing import ProblemaBicing
from parameters_bicing import params
from aima.search import hill_climbing, simulated_annealing
from time import time

# Función de ejecución de experimentos
def experimento1(opt: int, lista_semillas: list, iteraciones_por_semilla: int) -> None:
    # Experimento 1: Comparación de operadores
    comparar_all_operadores(opt=opt, \
                            lista_semillas=lista_semillas, \
                                iteraciones_por_semilla=iteraciones_por_semilla)

def experimento2(operadores_resultado_exp1: dict, lista_semillas: list, iteraciones_estrategias_aleatorias: int) -> None:
    # Experimento 2: Comparación de initial_state
    mejor_initial_state(iteraciones_estrategias_aleatorias=iteraciones_estrategias_aleatorias, \
                        lista_semillas=lista_semillas, \
                            operadores_activos=operadores_resultado_exp1)

def experimento3(iteraciones_por_semilla: int, lista_semillas: list, operadores_resultado_exp1: dict, opt_resultado_exp2: int, valores_k: list, valores_lam: list, limite: int) -> None:
    # Experimento 3: Comparación de SA
    encontrar_parametros_SA(lista_semillas=lista_semillas, \
                            opt=opt_resultado_exp2, \
                                operadores_activos=operadores_resultado_exp1, \
                                    valores_k=valores_k, \
                                        valores_lam=valores_lam, \
                                            limit=limite, \
                                                iteraciones_por_semilla=iteraciones_por_semilla)

def experimento4(operadores_resultado_exp1: dict, \
                 opt_resultado_exp2: int, \
                    incremento_estaciones: int, \
                        incremento_furgonetas: int, \
                            incremento_bicicletas: int, \
                                iteraciones_por_tanda: int, \
                                    n_incrementos: int) -> None:
    # Experimento 4: Comparación de HC
    tiempos_experimento_con_aumento(opt=opt_resultado_exp2, \
                                        operadores_activos=operadores_resultado_exp1, \
                                            incremento_estaciones=incremento_estaciones, \
                                                incremento_furgonetas=incremento_furgonetas, \
                                                    incremento_bicicletas=incremento_bicicletas, \
                                                        iteraciones_por_tanda=iteraciones_por_tanda,
                                                            n_incrementos=n_incrementos)

def experimento5(operadores_resultado_exp1: dict, opt_resultado_exp2: int, exp_schedule) -> None:
    # Experimento 5: Comparación de HC y SA
    comparar_resultados_HC_SA(opt=2, \
                              HC=True, \
                                SA=True, \
                                    iterations=50, \
                                        schedule_sa=exp_schedule())

def experimento6(operadores_resultado_exp1: dict, opt_resultado_exp2: int, exp_schedule) -> None:
    # Experimento 6: Comparación de HC y SA
    comparar_resultados_HC_SA(opt=2, \
                              HC=True, \
                                SA=True, \
                                    iterations=50, \
                                        schedule_sa=exp_schedule())

#######################################################################################################################

# Programa principal
if __name__ == "__main__":
    # Creación de la lista de semillas
    rng = random.Random(1234)
    n_semillas: int = 10
    lista_semillas: list = [42] + [rng.randint(0, 1000) for _ in range(n_semillas - 1)]
    print(f"Lista de {n_semillas} semillas para los experimentos: {lista_semillas}")

    # Generación del estado inicial
    initial_state = generate_initial_state(opt=2)
    initial_state.heuristic()
    problema_bicing = ProblemaBicing(initial_state)
    problema_bicing.mode_simulated_annealing = True
    def exp_schedule2(k: float=0.1, lam: float=0.1, limit: int=50000): # Función con los parámetros de Simulated Anealing obtenidos como resultado del experimento 3
        return lambda t: (k * exp(-lam * t)) if t < limit else 0
    schedule_sa = exp_schedule2()
    SA = simulated_annealing(problema_bicing, schedule=schedule_sa)
    print(SA.heuristic())
    
    # ----- Experimento 1 -----
    #experimento1(opt=1, lista_semillas=lista_semillas, iteraciones_por_semilla=10)

    operadores_exp1: dict = {'CambiarOrdenDescarga': True, \
                'IntercambiarEstacionDescarga': False, \
                'IntercambiarEstacionCarga': True, \
                    'ReasignarFurgonetaInformado': True}

    # ----- Experimento 2 -----    
    #experimento2(operadores_resultado_exp1=operadores_exp1, lista_semillas=lista_semillas, iteraciones_estrategias_aleatorias=5)
    
    opt_exp2: int = 2

    # ----- Experimento 3 -----
    valores_k: list = [0.001, 0.01, 0.1, 1, 10, 100]
    valores_lam: list = [0.0001, 0.001, 0.01, 0.1, 0.99]
    limite: int = 1

    #experimento3(iteraciones_por_semilla=5, lista_semillas=lista_semillas, operadores_resultado_exp1=operadores_exp1, opt_resultado_exp2=opt_exp2, valores_k=valores_k, valores_lam=valores_lam, limite=limite)

    def exp_schedule(k: float=0.1, lam: float=0.1, limit: int=15000): # Función con los parámetros de Simulated Anealing obtenidos como resultado del experimento 3
        return lambda t: (k * exp(-lam * t)) if t < limit else 0

    # ----- Experimento 4 -----
    #experimento4(operadores_resultado_exp1=operadores_exp1, opt_resultado_exp2=opt_exp2, incremento_estaciones=25, incremento_furgonetas=5, incremento_bicicletas=1250, iteraciones_por_tanda=10, n_incrementos=10)

    # ----- Experimento 5 -----
    #experimento5(operadores_resultado_exp1=operadores_exp1, opt_resultado_exp2=opt_exp2)

    # ----- Experimento 6 -----
    #experimento6(operadores_resultado_exp1=operadores_exp1, opt_resultado_exp2=opt_exp2)