from dataclasses import dataclass
@dataclass
class Gene:
    id : str
    cromosoma : int

    def __str__(self):
        return self.id

    def __hash__(self):
        return hash(self.id)


