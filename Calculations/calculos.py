import pandas as pd
import numpy as np
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import glob

class Calculos:
    """
    Clase para realizar cálculos astronómicos y análisis de datasets.
    Incluye cálculos de constante de Hubble, redshift, velocidad angular,
    órbitas y análisis de datos CSV de diferentes fuentes (SDSS, DESI, NEO, NASA ESI).
    """
    
    # Constantes físicas
    C = 299792.458  # Velocidad de la luz en km/s
    H0 = 70  # Constante de Hubble en km/s/Mpc (valor por defecto)
    G = 6.67430e-11  # Constante gravitacional en m^3 kg^-1 s^-2
    AU = 1.496e11  # Unidad astronómica en metros
    MASA_SOL = 1.989e30  # Masa del Sol en kg
    
    def __init__(self, data_path: str = "data"):
        """
        Inicializa la clase con la ruta a los datos.
        
        Args:
            data_path: Ruta a la carpeta que contiene los archivos CSV
        """
        self.data_path = Path(data_path)
        self.datasets = {}
        self.ultimo_analisis = None
        self._escanear_datasets()
    
    def _escanear_datasets(self):
        """Escanea la carpeta de datos y lista los archivos CSV disponibles."""
        if not self.data_path.exists():
            print(f"⚠️  La ruta {self.data_path} no existe. Creándola...")
            self.data_path.mkdir(parents=True, exist_ok=True)
            return
        
        csv_files = list(self.data_path.glob("*.csv"))
        for file in csv_files:
            dataset_name = file.stem
            self.datasets[dataset_name] = file
        
        if self.datasets:
            print(f"✓ Datasets encontrados: {list(self.datasets.keys())}")
    
    def calcularHubble(self, velocidad: float, distancia: float) -> float:
        """
        Calcula la constante de Hubble a partir de velocidad y distancia.
        
        Args:
            velocidad: Velocidad de recesión en km/s
            distancia: Distancia en Mpc
            
        Returns:
            Constante de Hubble en km/s/Mpc
        """
        if distancia == 0:
            raise ValueError("La distancia no puede ser cero")
        
        H = velocidad / distancia
        return H
    
    def calcularRedshift(self, longitud_observada: float, longitud_emitida: float) -> float:
        """
        Calcula el redshift (corrimiento al rojo) de un objeto.
        
        Args:
            longitud_observada: Longitud de onda observada
            longitud_emitida: Longitud de onda emitida en reposo
            
        Returns:
            Valor del redshift z
        """
        if longitud_emitida == 0:
            raise ValueError("La longitud de onda emitida no puede ser cero")
        
        z = (longitud_observada - longitud_emitida) / longitud_emitida
        return z
    
    def calcularVelocidadAngular(self, periodo: float, radio: float) -> Dict[str, float]:
        """
        Calcula la velocidad angular y lineal de un objeto en órbita.
        
        Args:
            periodo: Período orbital en segundos
            radio: Radio de la órbita en metros
            
        Returns:
            Diccionario con velocidad_angular (rad/s) y velocidad_lineal (m/s)
        """
        if periodo == 0:
            raise ValueError("El período no puede ser cero")
        
        omega = (2 * np.pi) / periodo
        v_lineal = omega * radio
        
        return {
            "velocidad_angular": omega,
            "velocidad_lineal": v_lineal,
            "periodo": periodo,
            "radio": radio
        }
    
    def calcularOrbita(self, masa_central: float, radio: float, excentricidad: float = 0) -> Dict[str, float]:
        """
        Calcula parámetros orbitales de un objeto.
        
        Args:
            masa_central: Masa del objeto central en kg
            radio: Semi-eje mayor en metros
            excentricidad: Excentricidad de la órbita (0 = circular)
            
        Returns:
            Diccionario con período, velocidad, energía orbital
        """
        # Tercera ley de Kepler para el período
        T = 2 * np.pi * np.sqrt(radio**3 / (self.G * masa_central))
        
        # Velocidad orbital (circular)
        v_orbital = np.sqrt(self.G * masa_central / radio)
        
        # Energía orbital específica
        energia = -self.G * masa_central / (2 * radio)
        
        # Perihelio y afelio
        perihelio = radio * (1 - excentricidad)
        afelio = radio * (1 + excentricidad)
        
        return {
            "periodo_segundos": T,
            "periodo_dias": T / 86400,
            "periodo_años": T / (86400 * 365.25),
            "velocidad_orbital": v_orbital,
            "energia_especifica": energia,
            "perihelio": perihelio,
            "afelio": afelio,
            "excentricidad": excentricidad
        }
    
    def calcularPhotoz(self, flux_g: float, flux_r: float, flux_z: float = None) -> Dict[str, float]:
        """
        Calcula el redshift fotométrico (photo-z) usando colores fotométricos.
        
        Utiliza relaciones empíricas basadas en los colores g-r y r-z.
        Método simplificado basado en templates de galaxias.
        
        Args:
            flux_g: Flujo en banda g (nanomaggies)
            flux_r: Flujo en banda r (nanomaggies)
            flux_z: Flujo en banda z (nanomaggies, opcional)
            
        Returns:
            Diccionario con photo-z estimado y métricas de calidad
        """
        # Evitar logaritmos de valores no positivos
        if flux_g <= 0 or flux_r <= 0:
            return {
                'photo_z': np.nan,
                'color_gr': np.nan,
                'color_rz': np.nan,
                'calidad': 'mala',
                'metodo': 'photo-z'
            }
        
        # Convertir flujos a magnitudes: m = 22.5 - 2.5*log10(flux)
        mag_g = 22.5 - 2.5 * np.log10(flux_g)
        mag_r = 22.5 - 2.5 * np.log10(flux_r)
        
        # Calcular color g-r
        color_gr = mag_g - mag_r
        
        # Relación empírica simplificada para photo-z
        # Basada en templates de galaxias típicas
        # z ≈ a*(g-r) + b  (calibración típica)
        
        # Coeficientes calibrados para galaxias
        a = 0.25  # Pendiente típica
        b = -0.1  # Intersección
        
        # Cálculo base con color g-r
        photo_z_base = a * color_gr + b
        
        # Si tenemos banda z, mejorar la estimación
        if flux_z is not None and flux_z > 0:
            mag_z = 22.5 - 2.5 * np.log10(flux_z)
            color_rz = mag_r - mag_z
            
            # Corrección con segundo color
            # Para galaxias rojas: z tiende a ser mayor
            # Para galaxias azules: z tiende a ser menor
            correction = 0.15 * color_rz
            photo_z = photo_z_base + correction
            
            # Estimar calidad basada en consistencia de colores
            if abs(color_gr) < 2.0 and abs(color_rz) < 1.5:
                calidad = 'buena'
            elif abs(color_gr) < 3.0 and abs(color_rz) < 2.5:
                calidad = 'media'
            else:
                calidad = 'baja'
        else:
            photo_z = photo_z_base
            color_rz = np.nan
            
            # Calidad solo con un color
            if abs(color_gr) < 2.0:
                calidad = 'media'
            else:
                calidad = 'baja'
        
        # Asegurar que photo-z sea no negativo
        photo_z = max(0.0, photo_z)
        
        return {
            'photo_z': photo_z,
            'color_gr': color_gr,
            'color_rz': color_rz,
            'mag_g': mag_g,
            'mag_r': mag_r,
            'calidad': calidad,
            'metodo': 'colores_fotometricos'
        }
    
    def calcularDistanciaHubble(self, z: float, H0: Optional[float] = None) -> Dict[str, float]:
        """
        Calcula la distancia usando la ley de Hubble a partir del redshift.
        
        Args:
            z: Redshift
            H0: Constante de Hubble (opcional, usa valor por defecto si no se proporciona)
            
        Returns:
            Diccionario con distancia en diferentes unidades y velocidad
        """
        if H0 is None:
            H0 = self.H0
        
        # Velocidad de recesión
        v = self.C * z  # Aproximación para z pequeños
        
        # Distancia de Hubble
        d_Mpc = v / H0
        d_m = d_Mpc * 3.086e22  # Conversión a metros
        d_ly = d_Mpc * 3.262e6  # Conversión a años luz
        
        return {
            "redshift": z,
            "velocidad_km_s": v,
            "distancia_Mpc": d_Mpc,
            "distancia_metros": d_m,
            "distancia_años_luz": d_ly,
            "H0_usado": H0
        }
    
    def analizar_datos_csv(self, dataset_name: str = None, df: pd.DataFrame = None, 
                          fuente: str = None, calculos_aplicar: List[str] = None) -> pd.DataFrame:
        """
        Analiza un dataset CSV o DataFrame y aplica cálculos astronómicos.
        
        Args:
            dataset_name: Nombre del dataset a analizar (sin extensión .csv)
            df: DataFrame con los datos (alternativa a dataset_name)
            fuente: Nombre de la fuente de datos (SDSS, DESI, NEO, NASA ESI)
            calculos_aplicar: Lista de cálculos a aplicar ['hubble', 'redshift', 'orbital']
            
        Returns:
            DataFrame con los datos originales y columnas calculadas adicionales
        """
        # Cargar datos desde archivo o usar DataFrame proporcionado
        if df is not None:
            datos = df.copy()
            nombre = fuente if fuente else "DataFrame proporcionado"
        elif dataset_name:
            if dataset_name not in self.datasets:
                raise ValueError(f"Dataset '{dataset_name}' no encontrado. Disponibles: {list(self.datasets.keys())}")
            datos = pd.read_csv(self.datasets[dataset_name])
            nombre = dataset_name
        else:
            raise ValueError("Debe proporcionar dataset_name o df")
        
        print(f"\n{'='*60}")
        print(f"📊 ANALIZANDO DATASET: {nombre}")
        print(f"{'='*60}")
        print(f"Filas: {len(datos)}, Columnas: {len(datos.columns)}")
        print(f"Columnas disponibles: {list(datos.columns)[:10]}...")
        
        # Detectar automáticamente qué cálculos aplicar
        if calculos_aplicar is None:
            calculos_aplicar = self._detectar_calculos(datos, fuente or nombre)
        
        df_resultado = datos.copy()
        resultados_calculos = {
            'fuente': nombre,
            'n_objetos': len(datos),
            'calculos_aplicados': []
        }
        
        # CÁLCULOS PARA SDSS Y DESI (Redshift y distancias)
        if 'redshift' in calculos_aplicar:
            # Determinar qué columna de redshift usar: 'z' (espectroscópico) o 'photo_z' (fotométrico)
            columna_z = None
            if 'z' in datos.columns and datos['z'].notna().any():
                columna_z = 'z'
                print("\n🌌 Calculando distancias cosmológicas (Ley de Hubble) usando Redshift Espectroscópico ('z')...")
            elif 'photo_z' in datos.columns and datos['photo_z'].notna().any():
                columna_z = 'photo_z'
                print("\n🌌 Calculando distancias cosmológicas (Ley de Hubble) usando Redshift Fotométrico ('photo_z')...")
            else:
                print("\n⚠️  No se encontró una columna de redshift ('z' o 'photo_z') válida para calcular la distancia.")

            if columna_z:
                distancias_Mpc = []
                distancias_ly = []
                velocidades = []
                h0_usado = []

                for z_val in datos[columna_z]:
                    if pd.notna(z_val) and z_val > 0:
                        dist_info = self.calcularDistanciaHubble(z_val)
                        distancias_Mpc.append(dist_info['distancia_Mpc'])
                        distancias_ly.append(dist_info['distancia_años_luz'])
                        velocidades.append(dist_info['velocidad_km_s'])
                        h0_usado.append(dist_info['H0_usado'])
                    else:
                        distancias_Mpc.append(np.nan)
                        distancias_ly.append(np.nan)
                        velocidades.append(np.nan)
                        h0_usado.append(np.nan)

                df_resultado['distancia_Mpc'] = distancias_Mpc
                df_resultado['distancia_años_luz'] = distancias_ly
                df_resultado['velocidad_recesion_km_s'] = velocidades
                df_resultado['H0_usado'] = h0_usado

                resultados_calculos['calculos_aplicados'].append('distancia_hubble')
                resultados_calculos['distancia_media_Mpc'] = np.nanmean(distancias_Mpc)
                resultados_calculos['distancia_max_Mpc'] = np.nanmax(distancias_Mpc)
                resultados_calculos['z_medio'] = datos[columna_z].mean()

                print(f"   ✓ Distancia media: {np.nanmean(distancias_Mpc):.2f} Mpc")
                print(f"   ✓ Redshift medio ({columna_z}): {datos[columna_z].mean():.4f}")
                print(f"   ✓ Objetos procesados: {len([d for d in distancias_Mpc if not np.isnan(d)])}")
        
        # 🆕 CÁLCULOS FOTOMÉTRICOS PARA DESI (Photo-z)
        if 'photoz' in calculos_aplicar:
            print("\n📸 Calculando redshift fotométrico (photo-z)...")
            
            # Verificar que tenemos las columnas necesarias
            if 'flux_g' in datos.columns and 'flux_r' in datos.columns:
                photo_zs = []
                colores_gr = []
                colores_rz = []
                calidades = []
                distancias_photoz = []
                
                tiene_flux_z = 'flux_z' in datos.columns
                
                for idx, row in datos.iterrows():
                    flux_g = row.get('flux_g')
                    flux_r = row.get('flux_r')
                    flux_z = row.get('flux_z') if tiene_flux_z else None
                    
                    if pd.notna(flux_g) and pd.notna(flux_r) and flux_g > 0 and flux_r > 0:
                        photo_resultado = self.calcularPhotoz(flux_g, flux_r, flux_z)
                        
                        photo_z = photo_resultado['photo_z']
                        photo_zs.append(photo_z)
                        colores_gr.append(photo_resultado['color_gr'])
                        colores_rz.append(photo_resultado['color_rz'])
                        calidades.append(photo_resultado['calidad'])
                        
                        # Calcular distancia con photo-z
                        if photo_z > 0:
                            dist_info = self.calcularDistanciaHubble(photo_z)
                            distancias_photoz.append(dist_info['distancia_Mpc'])
                        else:
                            distancias_photoz.append(np.nan)
                    else:
                        photo_zs.append(np.nan)
                        colores_gr.append(np.nan)
                        colores_rz.append(np.nan)
                        calidades.append('sin_datos')
                        distancias_photoz.append(np.nan)
                
                # Agregar columnas al DataFrame
                df_resultado['photo_z'] = photo_zs
                df_resultado['color_g-r'] = colores_gr
                df_resultado['color_r-z'] = colores_rz
                df_resultado['photo_z_calidad'] = calidades
                df_resultado['distancia_photoz_Mpc'] = distancias_photoz
                
                # Estadísticas
                photo_zs_validos = [z for z in photo_zs if not np.isnan(z)]
                if photo_zs_validos:
                    resultados_calculos['calculos_aplicados'].append('photo_z')
                    resultados_calculos['photo_z_medio'] = np.mean(photo_zs_validos)
                    resultados_calculos['photo_z_min'] = np.min(photo_zs_validos)
                    resultados_calculos['photo_z_max'] = np.max(photo_zs_validos)
                    resultados_calculos['n_objetos_photoz'] = len(photo_zs_validos)
                    
                    # Distribución de calidades
                    from collections import Counter
                    calidades_count = Counter([c for c in calidades if c != 'sin_datos'])
                    resultados_calculos['calidades_photoz'] = dict(calidades_count)
                    
                    print(f"   ✓ Photo-z medio: {np.mean(photo_zs_validos):.4f}")
                    print(f"   ✓ Rango: {np.min(photo_zs_validos):.4f} - {np.max(photo_zs_validos):.4f}")
                    print(f"   ✓ Objetos procesados: {len(photo_zs_validos)}/{len(datos)}")
                    print(f"   ✓ Calidad: {calidades_count.most_common()}")
                else:
                    print("   ⚠️  No se pudieron calcular photo-z válidos")
            else:
                print("   ⚠️  Faltan columnas flux_g y flux_r para calcular photo-z")
        
        # CÁLCULOS PARA NEO (Órbitas de asteroides y cometas)
        if 'orbital' in calculos_aplicar:
            print("\n☄️  Calculando parámetros orbitales (NEO)...")
            
            # Columnas típicas de NEO: q (perihelio AU), e (excentricidad), a (semi-eje mayor)
            if 'q' in datos.columns and 'e' in datos.columns:
                periodos = []
                velocidades = []
                afelios = []
                semi_ejes = []
                
                for idx, row in datos.iterrows():
                    try:
                        if pd.notna(row.get('q')) and pd.notna(row.get('e')) and row['e'] < 1:
                            # Calcular semi-eje mayor: a = q / (1 - e)
                            q_au = row['q']
                            e = row['e']
                            a_au = q_au / (1 - e)
                            a_m = a_au * self.AU
                            
                            orbita = self.calcularOrbita(self.MASA_SOL, a_m, e)
                            
                            periodos.append(orbita['periodo_años'])
                            velocidades.append(orbita['velocidad_orbital'] / 1000)  # km/s
                            afelios.append(orbita['afelio'] / self.AU)  # AU
                            semi_ejes.append(a_au)
                        else:
                            periodos.append(np.nan)
                            velocidades.append(np.nan)
                            afelios.append(np.nan)
                            semi_ejes.append(np.nan)
                    except:
                        periodos.append(np.nan)
                        velocidades.append(np.nan)
                        afelios.append(np.nan)
                        semi_ejes.append(np.nan)
                
                df_resultado['periodo_orbital_años'] = periodos
                df_resultado['velocidad_orbital_km_s'] = velocidades
                df_resultado['afelio_AU'] = afelios
                df_resultado['semi_eje_mayor_AU'] = semi_ejes
                
                resultados_calculos['calculos_aplicados'].append('orbital')
                resultados_calculos['periodo_medio_años'] = np.nanmean(periodos)
                resultados_calculos['velocidad_media_km_s'] = np.nanmean(velocidades)
                
                print(f"   ✓ Período medio: {np.nanmean(periodos):.2f} años")
                print(f"   ✓ Velocidad media: {np.nanmean(velocidades):.2f} km/s")
                print(f"   ✓ Objetos procesados: {len([p for p in periodos if not np.isnan(p)])}")
        
        # CÁLCULOS PARA NASA ESI (Exoplanetas)
        if 'exoplanet' in calculos_aplicar:
            print("\n🪐 Calculando parámetros orbitales de exoplanetas...")
            
            # Columnas requeridas: pl_orbper (periodo orbital en días)
            if 'pl_orbper' in datos.columns:
                velocidades_orbitales = []
                semi_ejes_mayores = []

                for periodo_dias in datos['pl_orbper']:
                    if pd.notna(periodo_dias) and periodo_dias > 0:
                        try:
                            # Convertir periodo a segundos
                            periodo_seg = periodo_dias * 86400
                            # Asumir masa estelar igual a la del Sol para simplificar
                            masa_central_kg = self.MASA_SOL

                            # Tercera Ley de Kepler para el semieje mayor (a)
                            # a^3 = (G * M * T^2) / (4 * pi^2)
                            a_m = (self.G * masa_central_kg * periodo_seg**2 / (4 * np.pi**2))**(1/3)

                            # Velocidad orbital (asumiendo órbita circular)
                            # v = 2 * pi * a / T
                            v_ms = (2 * np.pi * a_m) / periodo_seg

                            # Convertir a unidades más convenientes
                            a_au = a_m / self.AU
                            v_kms = v_ms / 1000

                            semi_ejes_mayores.append(a_au)
                            velocidades_orbitales.append(v_kms)
                        except (ValueError, OverflowError):
                            semi_ejes_mayores.append(np.nan)
                            velocidades_orbitales.append(np.nan)
                    else:
                        semi_ejes_mayores.append(np.nan)
                        velocidades_orbitales.append(np.nan)

                df_resultado['semi_eje_mayor_AU'] = semi_ejes_mayores
                df_resultado['velocidad_orbital_kms'] = velocidades_orbitales

                resultados_calculos['calculos_aplicados'].append('orbital_exoplanet')
                resultados_calculos['velocidad_orbital_media_kms'] = np.nanmean(velocidades_orbitales)

                print(f"   ✓ Velocidad orbital media: {np.nanmean(velocidades_orbitales):.2f} km/s")
                print(f"   ✓ Objetos procesados: {len([v for v in velocidades_orbitales if not np.isnan(v)])}")
            else:
                print("   ⚠️  Falta la columna 'pl_orbper' para los cálculos de exoplanetas.")
        
        # Estadísticas generales
        print(f"\n📈 ESTADÍSTICAS DEL ANÁLISIS:")
        print(f"   Total de objetos: {len(df_resultado)}")
        print(f"   Cálculos aplicados: {', '.join(resultados_calculos['calculos_aplicados']) if resultados_calculos['calculos_aplicados'] else 'Ninguno'}")
        
        if 'class' in datos.columns:
            print(f"\n   📊 Distribución por clase:")
            for clase, count in datos['class'].value_counts().head(5).items():
                print(f"      • {clase}: {count}")
        
        # Guardar resultado del último análisis
        self.ultimo_analisis = {
            'dataframe': df_resultado,
            'resultados': resultados_calculos
        }
        
        return df_resultado
    
    def _detectar_calculos(self, df: pd.DataFrame, fuente: str) -> List[str]:
        """Detecta automáticamente qué cálculos aplicar según las columnas disponibles."""
        calculos = []
        
        # Detectar datos de redshift espectroscópico (SDSS, DESI con z)
        if 'z' in df.columns:
            calculos.append('redshift')
        
        # Detectar datos fotométricos para photo-z (DESI sin z)
        if 'flux_g' in df.columns and 'flux_r' in df.columns:
            # Si no tiene redshift espectroscópico, usar photo-z
            if 'z' not in df.columns or df['z'].isna().all():
                calculos.append('photoz')
                print("   🔍 Detectados flujos fotométricos → aplicando photo-z")
        
        # Detectar datos orbitales (NEO)
        if any(col in df.columns for col in ['q', 'e', 'a', 'Q']):
            calculos.append('orbital')
        
        # Detectar datos de exoplanetas (NASA ESI)
        if any(col in df.columns for col in ['pl_orbper', 'pl_bmasse', 'pl_rade', 'st_teff']):
            calculos.append('exoplanet')
        
        return calculos
    
    def obtener_ultimo_analisis(self) -> Optional[Dict]:
        """Retorna el resultado del último análisis realizado."""
        return self.ultimo_analisis
    
    def listar_datasets(self) -> List[str]:
        """Retorna la lista de datasets disponibles."""
        return list(self.datasets.keys())
    
    def obtener_info_dataset(self, dataset_name: str) -> Dict:
        """
        Obtiene información básica de un dataset sin cargarlo completamente.
        
        Args:
            dataset_name: Nombre del dataset
            
        Returns:
            Diccionario con información del dataset
        """
        if dataset_name not in self.datasets:
            raise ValueError(f"Dataset '{dataset_name}' no encontrado")
        
        df = pd.read_csv(self.datasets[dataset_name], nrows=5)
        
        return {
            "nombre": dataset_name,
            "ruta": str(self.datasets[dataset_name]),
            "columnas": list(df.columns),
            "num_columnas": len(df.columns)
        }
    
    def generar_reporte(self) -> str:
        """Genera un reporte textual del último análisis."""
        if not self.ultimo_analisis:
            return "No hay análisis disponible"
        
        resultado = self.ultimo_analisis['resultados']
        
        reporte = f"""
{'='*60}
📊 REPORTE DE ANÁLISIS ASTRONÓMICO
{'='*60}

Fuente: {resultado['fuente']}
Objetos analizados: {resultado['n_objetos']}
Cálculos aplicados: {', '.join(resultado['calculos_aplicados']) if resultado['calculos_aplicados'] else 'Ninguno'}

"""
        
        if 'distancia_media_Mpc' in resultado:
            reporte += f"""
🌌 RESULTADOS COSMOLÓGICOS (Redshift Espectroscópico):
   • Distancia media: {resultado['distancia_media_Mpc']:.2f} Mpc
   • Distancia máxima: {resultado['distancia_max_Mpc']:.2f} Mpc
   • Redshift medio: {resultado['z_medio']:.4f}
"""
        
        if 'photo_z_medio' in resultado:
            reporte += f"""
📸 RESULTADOS FOTOMÉTRICOS (Photo-z):
   • Photo-z medio: {resultado['photo_z_medio']:.4f}
   • Rango photo-z: {resultado['photo_z_min']:.4f} - {resultado['photo_z_max']:.4f}
   • Objetos con photo-z: {resultado['n_objetos_photoz']}/{resultado['n_objetos']}
"""
            if 'calidades_photoz' in resultado:
                reporte += f"   • Calidad de estimaciones:\n"
                for calidad, count in resultado['calidades_photoz'].items():
                    reporte += f"      - {calidad}: {count} objetos\n"
        
        if 'periodo_medio_años' in resultado:
            reporte += f"""
☄️  RESULTADOS ORBITALES:
   • Período medio: {resultado['periodo_medio_años']:.2f} años
   • Velocidad media: {resultado['velocidad_media_km_s']:.2f} km/s
"""
        
        reporte += f"\n{'='*60}\n"
        
        return reporte