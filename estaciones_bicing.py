import random

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

    def copy(self) -> 'Estacion':
        new_estacion = Estacion(self.coordX, self.coordY)
        new_estacion.num_bicicletas_no_usadas = self.num_bicicletas_no_usadas
        new_estacion.num_bicicletas_next = self.num_bicicletas_next
        new_estacion.demanda = self.demanda
        new_estacion.diferencia = self.diferencia
        # Copia y asigna otros atributos si es necesario
        return new_estacion


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

        for id_est in range(num_movimientos):
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