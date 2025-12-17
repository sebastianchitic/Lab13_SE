from dataclasses import dataclass
@dataclass
class Classificazione:
    id_gene : str
    classificazione : str


    def __str__(self):
        return f"{self.id_gene} {self.classificazione}"

    def __hash__(self):
        return hash((self.id_gene, self.classificazione))

