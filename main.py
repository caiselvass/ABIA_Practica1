from estaciones_bicing import Estaciones, Estacion
from state_bicing import EstadoBicing
from furgoneta_bicing import Furgoneta
from parameters_bicing import params
from problem_bicing import ProblemaBicing
from aima.search import hill_climbing, simulated_annealing
import random

# Declaración de funciones
def generate_initial_state(n_furgonetas: int, n_estaciones: int) -> EstadoBicing:
    # Creamos una lista con la información que modificaremos de cada estación, para no tener que trabajar con objetos Estacio
    info_estaciones: list[dict] = [{'index': index, \
                                    'dif': est.num_bicicletas_next - est.demanda, \
                                    'disp': est.num_bicicletas_no_usadas} \
                                        for index, est in enumerate(params.estaciones)]

    # Creamos una lista con las estaciones con diferencia positiva y otra con las estaciones con diferencia negativa    
    lista_est_excedente: list[dict] = []
    lista_est_faltante: list[dict] = []
    for est in info_estaciones:
        if est['dif'] < 0:
            lista_est_faltante.append(est)
        elif est['dif'] > 0 and est['disp'] > 0:
            lista_est_excedente.append(est)
    
    n_estaciones_origen = len(lista_est_excedente)
    n_estaciones_destino = len(lista_est_faltante)
    
    lista_furgonetas = [Furgoneta(id=i) for i in range(n_furgonetas)]
    
    est_con_furgoneta = set()
    for furgoneta in lista_furgonetas:
        # Asignamos una estación de origen a la furgoneta
        id_est_o = random.randint(0, n_estaciones_origen - 1)
        while id_est_o in est_con_furgoneta:
            id_est_o = random.randint(0, n_estaciones_origen - 1)
        est_con_furgoneta.add(id_est_o)
        info_est_origen = lista_est_excedente[id_est_o]

        # Asignamos las coorenadas de origen a la furgoneta
        furgoneta.set_estacion_origen(info_est_origen)
    
        # Creamos las rutas de las furgonetas
        id_est_d1 = random.randint(0, n_estaciones_destino - 1)
        id_est_d2 = random.randint(0, n_estaciones_destino - 1)
        info_est_destino1 = lista_est_faltante[id_est_d1]
        info_est_destino2 = lista_est_faltante[id_est_d2]

        furgoneta.set_estaciones_destinos(info_est_destino1, info_est_destino2)
        
        # Cargamos y descargamos las bicicletas en las estaciones correspondientes y actualizamos ciertos datos de esas estaciones
        num_bicicletas_carga_inicial = min(30, info_est_origen['dif'], info_est_origen['disp'], abs(info_est_destino1['dif']) + abs(info_est_destino2['dif']))
        
        furgoneta.realizar_ruta(estacion_descarga1=info_est_destino1, estacion_descarga2=info_est_destino2, num_bicicletas_carga=num_bicicletas_carga_inicial)
            
    return EstadoBicing(info_estaciones=info_estaciones, lista_furgonetas=lista_furgonetas)

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

    print("Sta Cur Dem Dif Exc")

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

        print("est %2s = %2d %2d" % (id_estacion, estacion.coordX, estacion.coordY))
        print("%3d %3d %3d %3d %3d" % (num_bicicletas_no_usadas, num_bicicletas_next, demanda, diferencia, excedente))

    print("Bicis= %3d Demanda= %3d Disponibles= %3d Necesitan= %3d" %
          (acum_bicicletas, acum_demanda, acum_disponibles, acum_necesarias))
    
    # Experimento
    initial_state: EstadoBicing = generate_initial_state(n_furgonetas=params.n_furgonetas, n_estaciones=params.n_estaciones)
    initial_state.print_state(inicial=True)

    problema_bicing = ProblemaBicing(initial_state)
    final_solution = hill_climbing(problema_bicing)
    final_solution.print_state()