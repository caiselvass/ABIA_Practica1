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