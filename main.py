from estaciones_bicing import Estaciones, Estacion
from state_bicing import EstadoBicing
from furgoneta_bicing import Furgoneta
from parameters_bicing import Parameters
import random

# Declaración de funciones
def generate_initial_state(lista_estaciones: list[Estacion], n_furgonetas: int) -> EstadoBicing:
    # Creamos una lista con las estaciones con diferencia positiva y otra con las estaciones con diferencia negativa
    lista_est_excedente, lista_est_faltante = [], []
    for est in lista_estaciones:
        if est.diferencia < 0:
            lista_est_faltante.append(est)
        elif est.diferencia > 0 and est.num_bicicletas_no_usadas > 0:
            lista_est_excedente.append(est)
    
    n_estaciones_origen = len(lista_est_excedente)
    n_estaciones_destino = len(lista_est_faltante)
    
    lista_furgonetas = [Furgoneta() for _ in range(n_furgonetas)]
    
    est_con_furgoneta = set()
    for furgoneta in lista_furgonetas:
        # Asignamos una estación de origen a la furgoneta
        id_est_o = random.randint(0, n_estaciones_origen - 1)
        while id_est_o in est_con_furgoneta:
            id_est_o = random.randint(0, n_estaciones_origen - 1)
        est_con_furgoneta.add(id_est_o)
        estacion_origen = lista_est_excedente[id_est_o]

        # Asignamos las coorenadas de origen a la furgoneta
        furgoneta.set_coord_origen(estacion_origen.coordX, estacion_origen.coordY)
    
        # Creamos las rutas de las furgonetas
        id_est_d1 = random.randint(0, n_estaciones_destino - 1)
        id_est_d2 = random.randint(0, n_estaciones_destino - 1)
        estacion_destino1 = lista_est_faltante[id_est_d1]
        estacion_destino2 = lista_est_faltante[id_est_d2]

        coord_destino1: tuple[int, int] = (estacion_destino1.coordX, estacion_destino1.coordY)
        coord_destino2: tuple[int, int] = (estacion_destino2.coordX, estacion_destino2.coordY)
        furgoneta.set_coord_destinos(coord_destino1, coord_destino2)
        
        # Cargamos y descargamos las bicicletas en las estaciones correspondientes y actualizamos el balance de esas estaciones
        num_bicicletas_carga_inicial = min(30, estacion_origen.diferencia, estacion_origen.num_bicicletas_no_usadas, abs(estacion_destino1.diferencia) + abs(estacion_destino2.diferencia))
        
        furgoneta.realizar_ruta(estacion_carga=estacion_origen, estacion_descarga1=estacion_destino1, estacion_descarga2=estacion_destino2, num_bicicletas_carga=num_bicicletas_carga_inicial)
            
        print(furgoneta)

    return EstadoBicing(lista_estaciones, lista_furgonetas)

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
    parameters = Parameters(n_estaciones=25, n_bicicletas=1250, n_furgonetas=5, seed=42)
    
    estaciones = Estaciones(parameters.n_estaciones, parameters.n_bicicletas, parameters.seed)
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
        estacion.diferencia = diferencia
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
    
    test_state: EstadoBicing = generate_initial_state(estaciones.lista_estaciones, parameters.n_furgonetas)
    print(f"\n{'* '*20}\n\nBALANCE RUTAS: {test_state.calcular_balance_rutas()} \nBALANCE ESTACIONES: {test_state.calcular_balance_estaciones()} \nBALANCE TOTAL: {test_state.calcular_balance()}\n")