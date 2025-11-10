class Skyfree:
    """Clase principal de la aplicación para mostrar resultados y cargar datos."""

    def __init__(self):
        self.rutina = Rutina()
        self.resultados = None

    def cargarDatos(self, archivo: str) -> bool:
        """Carga y procesa los datos."""
        return self.rutina.procesarDatos(archivo)

    def mostrarResultados(self) -> None:
        """Muestra los resultados del análisis."""
        if not self.resultados:
            print("⚠ No hay resultados para mostrar. Ejecute cargarDatos() primero.")
            return

        print("\n" + "="*60)
        print("RESULTADOS DEL ANÁLISIS ASTRONÓMICO")
        print("="*60 + "\n")

        print("🌟 CONSTANTE DE HUBBLE:")
        print(f"   H₀ = {self.resultados['hubble']:.2f} km/s/Mpc\n")

        print("🔴 REDSHIFT:")
        print(f"   Objetos analizados: {len(self.resultados['redshifts'])}")
        print(f"   z promedio: {sum(self.resultados['redshifts'])/len(self.resultados['redshifts']) if self.resultados['redshifts'] else 0:.4f}\n")

        print("⭐ CLASIFICACIÓN ESTELAR:")
        for tipo, cantidad in self.resultados['clasificacion_estrellas'].items():
            print(f"   {tipo}: {cantidad} estrellas")
        print()

        print("🪐 EXOPLANETAS:")
        print(f"   Total: {self.resultados['exoplanetas']['total']}")
        print(f"   Habitables: {self.resultados['exoplanetas']['habitables']}")
        print(f"   Masa promedio: {self.resultados['exoplanetas']['masa_promedio']:.2f} MJ\n")

        print("🧠 MACHINE LEARNING:")
        print(f"   Precisión del modelo: {self.resultados['red_neuronal']['accuracy']:.2%}")
        print(f"   Grupos identificados: {len(set(self.resultados['clusters']))}\n")

        print("🌌 ESTRUCTURA CÓSMICA:")
        print(f"   Filamentos: {self.resultados['red_cosmica']['filamentos']}")
        print(f"   Vacíos: {self.resultados['red_cosmica']['vacios']}")
        print(f"   Nodos: {self.resultados['red_cosmica']['nodos']}\n")

        print("="*60 + "\n")
