from estaciones_bicing import Estaciones, Estacion
from state_bicing import EstadoBicing
from furgoneta_bicing import Furgoneta
from parameters_bicing import Parameters
import random

# Declaración de funciones
def generate_initial_state(lista_estaciones: list[Estacion], n_furgonetas: int) -> EstadoBicing:
    """
    Distribuim les furgonetes en les posicions inicials i retorna l'estat inicial.
    """
    lista_sobrantes_next, lista_distancias_centro = [], []
    for id_est in range(len(lista_estaciones)):
        est = lista_estaciones[id_est]
        
        est.bicicletas_sobrantes_next: int = est.num_bicicletas_next - est.demanda
        lista_sobrantes_next.append((est.bicicletas_sobrantes_next, id_est))

        est.distancia_centro: int = distancia_manhattan((est.coordX, est.coordY), (5000, 5000))
        lista_distancias_centro.append((est.distancia_centro, id_est))
    
    lista_sobrantes_next.sort(reverse=True)
    lista_distancias_centro.sort()
    
    mitad_estaciones = len(lista_estaciones)//2

    lista_furgonetas = [Furgoneta() for _ in range(n_furgonetas)]
    est_con_furgoneta = set()

    for furgoneta in lista_furgonetas:
        seleccionar_lista: str = random.choice(["sobrantes", "distancias"])
        
        if seleccionar_lista == "sobrantes":
            est_id = random.randint(0, mitad_estaciones)
            while lista_estaciones[lista_sobrantes_next[est_id][1]] in est_con_furgoneta:
                est_id = random.randint(0, mitad_estaciones)
            est_con_furgoneta.add(lista_estaciones[lista_sobrantes_next[est_id][1]])

            furgoneta.coordX = lista_estaciones[lista_sobrantes_next[est_id][1]].coordX
            furgoneta.coordY = lista_estaciones[lista_sobrantes_next[est_id][1]].coordY

        else: # seleccionar_lista == "distancias"
            est_id = random.randint(0, mitad_estaciones)
            while lista_estaciones[lista_distancias_centro[est_id][1]] in est_con_furgoneta:
                est_id = random.randint(0, mitad_estaciones)
            est_con_furgoneta.add(lista_estaciones[lista_distancias_centro[est_id][1]])

            furgoneta.coordX = lista_estaciones[lista_distancias_centro[est_id][1]].coordX
            furgoneta.coordY = lista_estaciones[lista_distancias_centro[est_id][1]].coordY

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
    
    generate_initial_state(estaciones.lista_estaciones, parameters.n_furgonetas)