import random
from typing import List, Union
from aima.search import Problem, hill_climbing, simulated_annealing

class Estacion(object):
    """
    Clase que representa una estación de Bicing
    """

    def __init__(self, x: int, y: int):
        """
        * coordX y coordY son atributos públicos que representan las
          coordenadas X e Y de la estación Bicing en metros
          bicicletas para la siguiente hora
        * num_bicicletas_next es un atributo público que guarda
          el número de bicicletas que habrá en la siguiente hora
          sin contar con los traslados
        * num_bicicletas_no_usadas es un atributo público que guarda
          el número de bicicletas que no se moverán en la hora actual
        """
        self.coordX: int = x * 100
        self.coordY: int = y * 100
        self.num_bicicletas_no_usadas: int = 0
        self.num_bicicletas_next: int = 0
        self.demanda: int = 0
        self.bicicletas_faltantes: int = self.demanda - self.num_bicicletas_next

    def __repr__(self):
        return f"(CoordX: {self.coordX}, CoordY: {self.coordY})"


class Estaciones(object):
    """
    Clase que representa una lista ordenada de estaciones (instancias de Estacion)
    """

    def __init__(self, num_estaciones: int, num_bicicletas: int, semilla: int):
        """
        Constructora de Estaciones
        * num_estaciones: número de estaciones a generar
        * num_bicicletas: número de bicicletas a repartir
        * semilla: semilla del generador de números aleatorios
        """
        self.num_bicicletas: int = num_bicicletas
        self.rng: random.Random = random.Random(semilla)
        mitad_estaciones: int = int(num_estaciones / 2)
        self.lista_estaciones: list[Estacion] = []

        for _ in range(mitad_estaciones):
            est = Estacion(self.rng.randint(0, 99), self.rng.randint(0, 99))
            self.lista_estaciones.append(est)

        for _ in range(mitad_estaciones, num_estaciones):
            est = Estacion(self.rng.randint(0, 49) + 25, self.rng.randint(0, 49) + 25)
            self.lista_estaciones.append(est)

        self.__genera_estado_actual()
        self.__genera_estado_movimientos()
        self.__genera_proxima_demanda()

    def __repr__(self):
        str_estaciones = "---------- ESTACIONES ----------\n"
        list_str_estaciones = []
        count = 1
        for est in self.lista_estaciones:
            list_str_estaciones.append(f"Estacion {count}: {est.__repr__()}")
            count += 1

        str_estaciones += str.join(", ", list_str_estaciones)
        return str_estaciones

    def __genera_estado_actual(self):
        """
        Assigna bicicletas a las estaciones de forma aleatoria.
        """
        for est in self.lista_estaciones:
            est.num_bicicletas_no_usadas = 0

        i = self.num_bicicletas
        while i > 0:
            asignadas = self.rng.randint(0, 1)
            id_est = self.rng.randint(0, len(self.lista_estaciones) - 1)
            self.lista_estaciones[id_est].num_bicicletas_no_usadas = \
                self.lista_estaciones[id_est].num_bicicletas_no_usadas + asignadas
            i = i - asignadas

    def __genera_estado_movimientos(self):
        """
        Genera movimientos de bicicletas entre estaciones de forma aleatoria.
        """
        num_movimientos: int = int(float(self.num_bicicletas) * 0.8)

        for est in self.lista_estaciones:
            est.num_bicicletas_next = 0

        for _ in range(num_movimientos):
            var3 = self.rng.randint(0, len(self.lista_estaciones) - 1)
            var2 = self.rng.randint(0, len(self.lista_estaciones) - 1)
            if self.lista_estaciones[var3].num_bicicletas_no_usadas > 0:
                self.lista_estaciones[var3].num_bicicletas_no_usadas = \
                    self.lista_estaciones[var3].num_bicicletas_no_usadas - 1
                self.lista_estaciones[var2].num_bicicletas_next = \
                    self.lista_estaciones[var2].num_bicicletas_next + 1

        for est in self.lista_estaciones:
            est.num_bicicletas_next = est.num_bicicletas_next + est.num_bicicletas_no_usadas

    def __genera_proxima_demanda(self):
        """
        Genera la demanda de bicicletas para la siguiente hora.s
        """
        media_bicicletas: int = int(self.num_bicicletas / len(self.lista_estaciones))

        for est in self.lista_estaciones:
            if self.rng.random() > 0.5:
                factor = 1
            else:
                factor = -1
            est.demanda = media_bicicletas + factor * self.rng.randint(0, int(float(media_bicicletas) * 0.5) - 1)


class Furgoneta(object):
    def __init__(self, x: int, y: int, num_bicicletas: int):
        self.coordX = x
        self.coordY = y
        self.num_bicicletas = num_bicicletas

    def __eq__(self, other):
        return isinstance(other, Furgoneta) and \
            self.coordX == other.coordX and \
                self.coordY == other.coordY and \
                    self.num_bicicletas == other.num_bicicletas
    
    def __repr__(self):
        return f"(CoordX: {self.coordX}, CoordY: {self.coordY}, NumBicicletas: {self.num_bicicletas})"

    def getX(self):
        return self.coordX
    
    def getY(self):
        return self.coordY
    
    def getNumBicicletas(self):
        return self.num_bicicletas
    
class MoveFurgoneta(object):
    def __init__(self, furgoneta: Furgoneta, estacion_carga: Estacion, estaciones_destino: list[Estacion] = []):
        self.furgoneta = furgoneta
        self.estacion_carga = estacion_carga
        self.estaciones_destino = estaciones_destino
    
    # def __repr__(self):
    #     str_estaciones_destino = ""
    #     for estacion in self.estaciones_destino:
    #         str_estaciones_destino += f"{estacion.__repr__()}"
    #     return f"Move furgoneta: {self.furgoneta.__repr__()}:\nEstacion carga: \nTo estaciones: {s"


class EstadoBicing(object):
    def __init__(self, estaciones: Estaciones, furgonetas: list[Furgoneta] = []):
        self.estaciones = estaciones
        self.furgonetas = furgonetas
        
    def __eq__(self, other):
        return isinstance(other, EstadoBicing) and self.estaciones == other.estaciones and self.furgonetas == other.furgonetas

    def __lt__(self, other):
        return hash(self) < hash(other)
    
    def __hash__(self):
        return hash((self.estaciones, self.furgonetas))
    
    def __repr__(self):
        str_furgonetas = ""
        count = 1
        for furgoneta in self.furgonetas:
            str_furgonetas += f"Furgoneta {count}: {furgoneta.__repr__()}\n"
            count += 1
        
        f"{self.estaciones.__repr__()}\n\n---------- FURGONETAS ----------\n{str_furgonetas}"
    
    def calcular_km(self):
        pass

    def heuristic(self):
        pass

    def generate_actions(self):
        pass

    def apply_action(self, action):
        pass


class ProblemaBicing(Problem):
    def __init__(self, initial_state: EstadoBicing):
        self.expanded_nodes = 0
        super.__init__(initial_state)
        pass


    def actions(self, state: EstadoBicing):
        pass

    def result(self, state: EstadoBicing, action):
        pass

    def path_cost(self, c, state1, action, state2):
        pass
    
    def h(self, node):
        return node.state.heuristic()

if __name__ == '__main__':
    """
    Prueba de funcionamiento:
    Creación de una instancia de estaciones y escritura a consola de:
    * Información de cada estacion
    * Datos por estacion de bicicletas presentes, demandadas, diferencia y excedente
    * Datos globales de bicicletas demandadas, disponibles para mover
      y bicicletas que es necesario mover
    """
    estaciones = Estaciones(25, 1250, 42)
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

# BAIGES
#kjkkjkj
