from typing import List, Dict, Any
import csv
class Entrada:
    """Clase para manejar la entrada de datos desde archivos."""
    
    def __init__(self, archivoCSV: str, archivoDAT: str = None):
        self.archivoCSV = archivoCSV
        self.archivoDAT = archivoDAT
    
    def leerDatos(self) -> List[Dict[str, Any]]:
        """Lee los datos desde el archivo CSV."""
        datos = []
        try:
            with open(self.archivoCSV, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                datos = [fila for fila in lector]
            print(f"✓ Datos leídos correctamente: {len(datos)} registros")
        except FileNotFoundError:
            print(f"✗ Error: Archivo '{self.archivoCSV}' no encontrado")
        except Exception as e:
            print(f"✗ Error al leer datos: {str(e)}")
        return datos
