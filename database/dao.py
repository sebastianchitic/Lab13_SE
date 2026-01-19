from database.DB_connect import DBConnect
from model.Interazione import Interazione
from model.Classificazione import Classificazione
from model.Gene import Gene


class DAO:

    @staticmethod
    def read_interazione():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM interazione"
        cursor.execute(query)
        for row in cursor:
            interazione = Interazione(
                id_gene1 = row["id_gene1"],
                id_gene2 = row["id_gene2"],
                tipo = row["tipo"],
                correlazione = row["correlazione"]
            )
            result.append(interazione)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_classificazione():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM classificazione"
        cursor.execute(query)
        for row in cursor:
            classificazione = Classificazione(
                id_gene = row["id_gene"],
                localizzazione = row["localizzazione"]
            )
            result.append(classificazione)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_gene():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT DISTINCT id, cromosoma FROM gene WHERE cromosoma > 0"
        cursor.execute(query)
        for row in cursor:
            gene = Gene(
                id = row["id"],
                cromosoma = row["cromosoma"]
            )
            result.append(gene)
        cursor.close()
        conn.close()
        return result

@staticmethod
    def get_archi_pesati():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        
        # Query modificata usando WHERE per i join
        query = """
            SELECT g1.cromosoma as c1, g2.cromosoma as c2, SUM(i.correlazione) as peso
            FROM interazione i, gene g1, gene g2
            WHERE i.id_gene1 = g1.id
              AND i.id_gene2 = g2.id
              AND g1.cromosoma <> g2.cromosoma
              AND g1.cromosoma > 0
              AND g2.cromosoma > 0
            GROUP BY g1.cromosoma, g2.cromosoma
        """
        
        cursor.execute(query)
        
        for row in cursor:
            # Restituisce una tupla (Cromosoma 1, Cromosoma 2, Peso Totale)
            result.append((row["c1"], row["c2"], row["peso"]))
            
        cursor.close()
        conn.close()
        return result
