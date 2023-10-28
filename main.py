from functions_bicing import comparar_all_operadores, mejor_initial_state, encontrar_parametros_SA ,comparar_resultados_HC_SA
from math import exp

# Función de ejecución de experimentos
def experimento1(opt: int, semilla: int) -> None:
    # Experimento 1: Comparación de operadores
    comparar_all_operadores(opt=opt, \
                            semilla_rng=semilla, \
                                    iteraciones=15)


def experimento2(operadores_resultado_exp1: dict, semilla_rng) -> None:
    # Experimento 2: Comparación de initial_state
    mejor_initial_state(iteraciones=100, \
                        semilla_rng=semilla_rng, \
                            operadores_activos=operadores_resultado_exp1)

def experimento3(operadores_resultado_exp1: dict, opt_resultado_exp2: int, valores_k: list, valores_lam: list, limite: int) -> None:
    # Experimento 3: Comparación de SA
    encontrar_parametros_SA(opt=opt_resultado_exp2, \
                                operadores_activos=operadores_resultado_exp1, \
                                    valores_k=valores_k, \
                                        valores_lam=valores_lam, \
                                            limit=limite)

def experimento4() -> None:
    # Experimento 4: Comparación de HC
    comparar_resultados_HC_SA(opt=2, HC=True, SA=False, iterations=100)

def experimento5() -> None:
    # Experimento 5: Comparación de HC y SA
    k, lam, limit = encontrar_parametros_SA(opt=2, iteraciones_por_valor=1)

    def exp_schedule(k: float=k, lam: float=lam, limit: int=limit):
        return lambda t: (k * exp(-lam * t)) if t < limit else 0

    comparar_resultados_HC_SA(opt=2, HC=True, SA=True, iterations=50, schedule_sa=exp_schedule())

def experimento6() -> None:
    # Experimento 6: Comparación de HC y SA
    k, lam, limit = encontrar_parametros_SA(opt=2, iteraciones_por_valor=1)

    def exp_schedule(k: float=k, lam: float=lam, limit: int=limit):
        return lambda t: (k * exp(-lam * t)) if t < limit else 0

    comparar_resultados_HC_SA(opt=2, HC=True, SA=True, iterations=50, schedule_sa=exp_schedule())

#######################################################################################################################

# Programa principal
if __name__ == "__main__":

    # ----- Experimento 1 -----
    experimento1(opt=1, semilla=1234)
    
    operadores_exp1: dict = {'CambiarOrdenDescarga': True, \
                    'IntercambiarEstacionDescarga': True, \
                    'IntercambiarEstacionCarga': False, \
                        'ReasignarFurgonetaInformado': True}

    # ----- Experimento 2 -----    
    #experimento2(operadores_resultado_exp1=operadores_exp1, semilla_rng=1234)
    
    opt_exp2: int = 2

    # ----- Experimento 3 -----
    valores_k: list = [1, 5, 25, 50, 100, 150]
    valores_lam: list = [0.0001, 0.001, 0.01, 1]
    limite: int = 10_000

    #experimento3(operadores_resultado_exp1=operadores_exp1, opt_resultado_exp2=opt_exp2, valores_k=valores_k, valores_lam=valores_lam, limite=limite)

    k_exp3: int = 0
    lam_exp3: int = 0
    limite_exp3: int = 0

    # ----- Experimento 4 -----
    #experimento4(operadores_resultado_exp1=operadores_exp1, opt_resultado_exp2=opt_exp2)

    # ----- Experimento 5 -----
    #experimento5(operadores_resultado_exp1=operadores_exp1, opt_resultado_exp2=opt_exp2)

    # ----- Experimento 6 -----
    #experimento6(operadores_resultado_exp1=operadores_exp1, opt_resultado_exp2=opt_exp2)
