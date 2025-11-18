"""
Script de prueba para la clase Calculos integrada con Rutinas
Ejecutar: python test_calculos_integrado.py

Este script prueba:
1. Funciones individuales de cálculo
2. Análisis de datasets desde archivos
3. Análisis de DataFrames en memoria
4. Integración completa con el sistema
"""

from Calculations.calculos import Calculos
import pandas as pd
import numpy as np

def separador(titulo):
    """Imprime un separador visual"""
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70 + "\n")

def crear_dataset_prueba_desi():
    """Crea un dataset de prueba simulando datos DESI con flujos fotométricos"""
    n = 100
    
    # Simular flujos realistas (nanomaggies)
    # Galaxias a diferentes redshifts tienen diferentes colores
    redshifts = np.random.uniform(0.1, 0.8, n)
    
    # Relación aproximada: galaxias más lejanas (mayor z) son más rojas
    # flux_g decrece más rápido que flux_r con z
    flux_g = np.random.uniform(5, 100, n) * np.exp(-redshifts * 0.5)
    flux_r = np.random.uniform(10, 120, n) * np.exp(-redshifts * 0.3)
    flux_z = np.random.uniform(8, 110, n) * np.exp(-redshifts * 0.2)
    
    data = {
        'ra': np.random.uniform(0, 360, n),
        'dec': np.random.uniform(-90, 90, n),
        'type': np.random.choice(['GALAXY', 'QSO', 'STAR'], n, p=[0.7, 0.2, 0.1]),
        'flux_g': flux_g,
        'flux_r': flux_r,
        'flux_z': flux_z,
        'flux_w1': np.random.uniform(5, 50, n),
        'flux_w2': np.random.uniform(3, 40, n),
        'flux_ivar_g': np.random.uniform(0.1, 10, n),
        'flux_ivar_r': np.random.uniform(0.1, 10, n),
        'flux_ivar_z': np.random.uniform(0.1, 10, n),
    }
    return pd.DataFrame(data)

def crear_dataset_prueba_sdss():
    """Crea un dataset de prueba simulando datos SDSS"""
    n = 100
    data = {
        'objid': range(1, n+1),
        'ra': np.random.uniform(0, 360, n),
        'dec': np.random.uniform(-90, 90, n),
        'z': np.random.uniform(0.01, 0.3, n),  # Redshift
        'class': np.random.choice(['GALAXY', 'STAR', 'QSO'], n),
        'flux_g': np.random.uniform(10, 100, n),
        'flux_r': np.random.uniform(10, 100, n)
    }
    return pd.DataFrame(data)

def crear_dataset_prueba_neo():
    """Crea un dataset de prueba simulando datos NEO"""
    n = 50
    data = {
        'targetname': [f'Asteroid_{i}' for i in range(1, n+1)],
        'H': np.random.uniform(10, 25, n),  # Magnitud absoluta
        'q': np.random.uniform(0.5, 4.0, n),  # Perihelio en AU
        'e': np.random.uniform(0.0, 0.9, n),  # Excentricidad
        'incl': np.random.uniform(0, 30, n),  # Inclinación
        'a': np.random.uniform(1.0, 5.0, n)  # Semi-eje mayor
    }
    return pd.DataFrame(data)

def test_funciones_basicas():
    """Prueba las funciones básicas de cálculo"""
    separador("PRUEBAS DE FUNCIONES BÁSICAS")
    
    calc = Calculos()
    
    # Test 1: Hubble
    print("1️⃣  Calculando constante de Hubble...")
    H = calc.calcularHubble(velocidad=7000, distancia=100)
    print(f"   ✓ H = {H:.2f} km/s/Mpc")
    assert 60 < H < 80, "Valor de H fuera del rango esperado"
    
    # Test 2: Redshift (corregido: usar parámetros posicionales)
    print("\n2️⃣  Calculando redshift...")
    z = calc.calcularRedshift(656.3, 486.1)  # longitud_observada, longitud_emitida
    print(f"   ✓ z = {z:.6f}")
    assert z > 0, "Redshift debe ser positivo para objetos que se alejan"
    
    # Test 3: Distancia de Hubble
    print("\n3️⃣  Calculando distancia cosmológica...")
    dist = calc.calcularDistanciaHubble(z=0.1)
    print(f"   ✓ Distancia = {dist['distancia_Mpc']:.2f} Mpc")
    print(f"   ✓ Velocidad = {dist['velocidad_km_s']:.2f} km/s")
    assert dist['distancia_Mpc'] > 0, "Distancia debe ser positiva"
    
    # Test 4: Velocidad Angular
    print("\n4️⃣  Calculando velocidad angular...")
    periodo = 365.25 * 86400  # 1 año en segundos
    radio = 1.496e11  # 1 AU
    vel = calc.calcularVelocidadAngular(periodo, radio)
    print(f"   ✓ ω = {vel['velocidad_angular']:.10e} rad/s")
    print(f"   ✓ v = {vel['velocidad_lineal']/1000:.2f} km/s")
    
    # Test 5: Órbita
    print("\n5️⃣  Calculando parámetros orbitales...")
    orbita = calc.calcularOrbita(calc.MASA_SOL, 1.496e11, 0.0167)
    print(f"   ✓ Período = {orbita['periodo_años']:.4f} años")
    print(f"   ✓ Velocidad = {orbita['velocidad_orbital']/1000:.2f} km/s")
    assert 0.99 < orbita['periodo_años'] < 1.01, "Período de la Tierra debe ser ~1 año"
    
    print("\n✅ Todas las pruebas de funciones básicas pasaron correctamente")

def test_analisis_dataframe_sdss():
    """Prueba el análisis de un DataFrame SDSS en memoria"""
    separador("PRUEBA DE ANÁLISIS - DATASET SDSS (en memoria)")
    
    calc = Calculos()
    
    # Crear dataset de prueba
    df_sdss = crear_dataset_prueba_sdss()
    
    print(f"📊 Dataset de prueba creado:")
    print(f"   Objetos: {len(df_sdss)}")
    print(f"   Columnas: {list(df_sdss.columns)}")
    print(f"\n   Primeras 3 filas:")
    print(df_sdss.head(3))
    
    # Analizar
    print("\n🔬 Aplicando análisis...")
    df_resultado = calc.analizar_datos_csv(df=df_sdss, fuente="SDSS_TEST")
    
    # Verificar resultados
    print("\n📈 Verificando resultados...")
    columnas_esperadas = ['distancia_Mpc', 'distancia_años_luz', 'velocidad_recesion_km_s']
    for col in columnas_esperadas:
        assert col in df_resultado.columns, f"Columna {col} no encontrada"
        print(f"   ✓ {col}: OK")
    
    print(f"\n✅ Análisis de SDSS completado exitosamente")
    print(f"   Columnas agregadas: {len(df_resultado.columns) - len(df_sdss.columns)}")
    
    # Generar reporte
    reporte = calc.generar_reporte()
    print(reporte)
    
    # No retornar nada para pytest
    assert df_resultado is not None

def test_analisis_dataframe_neo():
    """Prueba el análisis de un DataFrame NEO en memoria"""
    separador("PRUEBA DE ANÁLISIS - DATASET NEO (en memoria)")
    
    calc = Calculos()
    
    # Crear dataset de prueba
    df_neo = crear_dataset_prueba_neo()
    
    print(f"☄️  Dataset de prueba NEO creado:")
    print(f"   Objetos: {len(df_neo)}")
    print(f"   Columnas: {list(df_neo.columns)}")
    print(f"\n   Primeras 3 filas:")
    print(df_neo.head(3))
    
    # Analizar
    print("\n🔬 Aplicando análisis orbital...")
    df_resultado = calc.analizar_datos_csv(df=df_neo, fuente="NEO_TEST")
    
    # Verificar resultados
    print("\n📈 Verificando resultados...")
    columnas_esperadas = ['periodo_orbital_años', 'velocidad_orbital_km_s', 'afelio_AU']
    for col in columnas_esperadas:
        assert col in df_resultado.columns, f"Columna {col} no encontrada"
        print(f"   ✓ {col}: OK")
    
    print(f"\n✅ Análisis de NEO completado exitosamente")
    
    # Mostrar estadísticas
    print(f"\n📊 Estadísticas orbitales:")
    print(f"   Período mínimo: {df_resultado['periodo_orbital_años'].min():.2f} años")
    print(f"   Período máximo: {df_resultado['periodo_orbital_años'].max():.2f} años")
    print(f"   Velocidad media: {df_resultado['velocidad_orbital_km_s'].mean():.2f} km/s")
    
    # No retornar nada para pytest
    assert df_resultado is not None

def test_guardar_y_leer_csv():
    """Prueba guardar un dataset y leerlo después"""
    separador("PRUEBA DE GUARDAR Y LEER CSV")
    
    calc = Calculos()
    
    # Crear y guardar dataset
    df_test = crear_dataset_prueba_sdss()
    ruta_test = calc.data_path / "test_sdss_data.csv"
    
    print(f"💾 Guardando dataset de prueba...")
    calc.data_path.mkdir(parents=True, exist_ok=True)
    df_test.to_csv(ruta_test, index=False)
    print(f"   ✓ Guardado en: {ruta_test}")
    
    # Re-escanear datasets
    calc._escanear_datasets()
    
    # Listar datasets
    print(f"\n📚 Datasets disponibles:")
    datasets = calc.listar_datasets()
    for ds in datasets:
        print(f"   • {ds}")
    
    # Analizar desde archivo
    if "test_sdss_data" in datasets:
        print(f"\n🔍 Analizando desde archivo...")
        df_resultado = calc.analizar_datos_csv(dataset_name="test_sdss_data")
        
        print(f"\n✅ Dataset leído y analizado correctamente")
        print(f"   Filas: {len(df_resultado)}")
        print(f"   Columnas: {len(df_resultado.columns)}")
        
        # No retornar nada para pytest
        assert df_resultado is not None
    else:
        print("⚠️  Dataset no encontrado después de guardar")
        assert False, "Dataset no encontrado"

def test_comparacion_calculos():
    """Compara cálculos manuales con los de la clase"""
    separador("VERIFICACIÓN DE PRECISIÓN DE CÁLCULOS")
    
    calc = Calculos()
    
    # Test 1: Ley de Hubble
    print("🔬 Verificando Ley de Hubble...")
    z_test = 0.1
    v_esperada = calc.C * z_test
    d_esperada = v_esperada / calc.H0
    
    resultado = calc.calcularDistanciaHubble(z_test)
    
    assert abs(resultado['velocidad_km_s'] - v_esperada) < 0.01, "Error en cálculo de velocidad"
    assert abs(resultado['distancia_Mpc'] - d_esperada) < 0.01, "Error en cálculo de distancia"
    
    print(f"   ✓ Velocidad: {resultado['velocidad_km_s']:.2f} km/s (esperado: {v_esperada:.2f})")
    print(f"   ✓ Distancia: {resultado['distancia_Mpc']:.2f} Mpc (esperado: {d_esperada:.2f})")
    
    # Test 2: Tercera Ley de Kepler
    print("\n🪐 Verificando Tercera Ley de Kepler...")
    a = 1.496e11  # 1 AU en metros
    T_esperado = 365.25 * 86400  # 1 año en segundos
    
    orbita = calc.calcularOrbita(calc.MASA_SOL, a, 0)
    error_relativo = abs(orbita['periodo_segundos'] - T_esperado) / T_esperado * 100
    
    print(f"   ✓ Período calculado: {orbita['periodo_años']:.6f} años")
    print(f"   ✓ Error relativo: {error_relativo:.4f}%")
    
    assert error_relativo < 1, "Error en Tercera Ley de Kepler mayor al 1%"
    
    print("\n✅ Todos los cálculos verificados correctamente")

def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "="*70)
    print("🚀 SISTEMA DE PRUEBAS - CLASE CALCULOS")
    print("   Integración con Orquestador Rutinas")
    print("="*70)
    
    try:
        # Pruebas básicas
        test_funciones_basicas()
        
        # Pruebas de análisis
        test_analisis_dataframe_sdss()
        test_analisis_dataframe_neo()
        
        # Pruebas de archivos
        test_guardar_y_leer_csv()
        
        # Verificación de precisión
        test_comparacion_calculos()
        
        # Resumen final
        separador("RESUMEN DE PRUEBAS")
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("\n📝 La clase Calculos está lista para:")
        print("   1. Integrarse con el orquestador Rutinas")
        print("   2. Procesar datos de SDSS, DESI, NEO, NASA ESI")
        print("   3. Aplicar cálculos astronómicos automáticamente")
        print("   4. Generar reportes de análisis")
        print("\n🎯 Próximos pasos:")
        print("   • Copiar calculos.py a la carpeta Calculos/")
        print("   • Actualizar rutinas.py con la versión integrada")
        print("   • Ejecutar rutinas.py para probar el sistema completo")
        print("\n" + "="*70)
        
    except AssertionError as e:
        print(f"\n❌ PRUEBA FALLIDA: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    exito = main()
    exit(0 if exito else 1)