from estaciones_bicing import Estaciones, Estacion
from state_bicing import EstadoBicing
from furgoneta_bicing import Furgoneta
from parameters_bicing import Parameters, distancia_manhattan
import random

# Declaración de funciones
def generate_initial_state(lista_estaciones: list[Estacion], n_furgonetas: int) -> EstadoBicing:
    for est in lista_estaciones:
        est.bicicletas_sobrantes_next: int = est.num_bicicletas_next - est.demanda

    lista_sobrantes_next, lista_faltantes_next = [], []
    for est in lista_estaciones:
        if est.bicicletas_sobrantes_next < 0:
            lista_faltantes_next.append(est)
        elif est.bicicletas_sobrantes_next > 0 and est.num_bicicletas_no_usadas > 0:
            lista_sobrantes_next.append(est)
    
    n_estaciones_origen = len(lista_sobrantes_next)
    n_estaciones_destino = len(lista_faltantes_next)
    
    lista_furgonetas = [Furgoneta() for _ in range(n_furgonetas)]
    est_con_furgoneta = set()

    for furgoneta in lista_furgonetas:
        # Asignamos una estación de origen a la furgoneta
        id_est_o = random.randint(0, n_estaciones_origen - 1)
        while id_est_o in est_con_furgoneta:
            id_est_o = random.randint(0, n_estaciones_origen - 1)
        est_con_furgoneta.add(id_est_o)

        furgoneta.origenX = lista_sobrantes_next[id_est_o].coordX
        furgoneta.origenY = lista_sobrantes_next[id_est_o].coordY
        furgoneta.num_bicicletas_cargadas = lista_sobrantes_next[id_est_o].num_bicicletas_no_usadas \
            if lista_sobrantes_next[id_est_o].num_bicicletas_no_usadas <= 30 else 30

        # Creamos las rutas de las furgonetas
        id_est_d1 = random.randint(0, n_estaciones_destino - 1)
        id_est_d2 = random.randint(0, n_estaciones_destino - 1)

        destino1: tuple[int, int] = (lista_faltantes_next[id_est_d1].coordX, lista_faltantes_next[id_est_d1].coordY)
        destino2: tuple[int, int] = (lista_faltantes_next[id_est_d2].coordX, lista_faltantes_next[id_est_d2].coordY)
        furgoneta.set_coord_destinos(destino1, destino2)

        # Descargamos las bicicletas en la 1a estación de destino
        furgoneta.num_bicicletas_descargadas_destino1 = min(furgoneta.num_bicicletas_cargadas, \
                                                            abs(lista_faltantes_next[id_est_d1].bicicletas_sobrantes_next))
        

        furgoneta.beneficio_descargas += furgoneta.num_bicicletas_descargadas_destino1 * 2 # El euro que nos dan y el que ya no nos quitan
        furgoneta.beneficio_descargas += min(furgoneta.num_bicicletas_cargadas - furgoneta.num_bicicletas_descargadas_destino1, \
                                             lista_faltantes_next[id_est_d2].demanda) * 2 # El euro que nos dan y el que ya no nos quitan
        
        print(furgoneta)

    return EstadoBicing(lista_estaciones, lista_furgonetas)

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
    print(f"\nRUTAS: {test_state.calcular_balance_rutas()} \nBENEFICIOS: {test_state.calcular_beneficios_estaciones()} \nPERDIDAS: {test_state.calcular_perdidas_estaciones()} \nBALANCE: {test_state.calcular_balance()}\n")