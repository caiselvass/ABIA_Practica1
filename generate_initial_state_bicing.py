import random
from parameters_bicing import params
from typing import Union
from state_bicing import EstadoBicing
from furgoneta_bicing import Furgoneta

# Declaración de funciones
def generate_initial_state(opt: int = 0, \
                           semilla_rng: Union[int, None] = None, \
                            operadores_activos: dict = {operator: True for operator in params.operadores_modificables}) -> EstadoBicing:
    rng = random.Random(semilla_rng)

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

        # Para evitar que el código se rompa si no hay suficientes estaciones con diferencia positiva o negativa
        while len(lista_est_excedente) < n_furgonetas:
            nueva_estacion = rng.randint(0, n_estaciones - 1)
            if nueva_estacion not in lista_est_excedente:
                lista_est_excedente.append(nueva_estacion)
                lista_est_faltante.pop(lista_est_faltante.index(nueva_estacion))
        
        while len(lista_est_faltante) < 1:
            nueva_estacion = rng.randint(0, n_estaciones -1)
            if nueva_estacion not in lista_est_excedente:
                lista_est_faltante.append(nueva_estacion)

        
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
        
        n_estaciones_origen = len(lista_est_excedente)
        n_estaciones_destino = len(lista_est_faltante)
                
        lista_est_excedente.sort(reverse=True)
        lista_est_faltante.sort()

        # Para evitar que el código se rompa si no hay suficientes estaciones con diferencia positiva o negativa
        while len(lista_est_excedente) < n_furgonetas:
            nueva_estacion = rng.randint(0, n_estaciones - 1)
            if nueva_estacion not in lista_est_excedente:
                lista_est_excedente.append((None, nueva_estacion))
                for i, est in enumerate(lista_est_faltante):
                    if est[1] == nueva_estacion:
                        lista_est_faltante.pop(i)
                        break
        
        while len(lista_est_faltante) < 2*n_furgonetas:
            nueva_estacion = rng.randint(0, n_estaciones -1)
            if nueva_estacion not in lista_est_excedente and nueva_estacion not in lista_est_faltante:
                lista_est_faltante.append((None, nueva_estacion))
        
        # Asignación tipo 1
        j = 0
        for i, furgoneta in enumerate(lista_furgonetas):
            furgoneta.id_est_origen = lista_est_excedente[i][1]
            furgoneta.id_est_dest1 = lista_est_faltante[j][1]
            furgoneta.id_est_dest2 = lista_est_faltante[j+1][1]
            j += 2
    
    state = EstadoBicing(lista_furgonetas=lista_furgonetas, operadores_activos=operadores_activos)
    return state