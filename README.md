# Quipu-Skyfree

Quipu-Skyfree es un software de análisis de datos astronómicos diseñado con fines educativos. Permite a los usuarios conectarse a diversas bases de datos astronómicas, realizar cálculos científicos y aplicar algoritmos de machine learning para analizar los datos.

## Características

- **Conexión a bases de datos astronómicas**:
  - **SDSS** (Sloan Digital Sky Survey): Para datos de galaxias y espectros.
  - **DESI** (Dark Energy Spectroscopic Instrument): Para objetos del cosmos profundo.
  - **NASA ESI** (NASA Exoplanet Science Institute): Para datos de exoplanetas.
  - **NEO** (Near-Earth Object): Para datos de asteroides y cometas.
- **Cálculos astronómicos**:
  - Constante de Hubble
  - Redshift
  - Velocidad angular
  - Parámetros orbitales
  - Redshift fotométrico (photo-z)
- **Machine Learning**:
  - **Clustering**: Agrupación de datos mediante K-Means y HDBSCAN.
  - **Regresión con Redes Neuronales**: Predicción de valores mediante redes neuronales con TensorFlow/Keras.
- **Interfaz de línea de comandos (CLI)**: Un menú interactivo para guiar al usuario a través de las diferentes funcionalidades.

## Estructura del Proyecto

- `skyfree/`: Contiene la lógica principal de la aplicación.
- `Calculations/`: Contiene la lógica para los cálculos astronómicos.
- `DB/`: Gestiona la conexión y consulta a las bases de datos astronómicas.
- `ML/`: Implementa los algoritmos de machine learning.
- `data/`: Directorio donde se guardan los datasets descargados.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/Quipu-Skyfree.git
   ```
2. Instala las dependencias:
   ```bash
   pip install -e .
   ```

## Uso

Para iniciar la aplicación, ejecuta el siguiente comando desde el directorio raíz del proyecto:

```bash
python3 skyfree/rutinas.py
```

Esto iniciará el menú interactivo en la línea de comandos, donde podrás seleccionar la fuente de datos, realizar cálculos y aplicar análisis de machine learning.

## Ejemplos de Uso

A continuación, se muestran algunos ejemplos de cómo utilizar las funcionalidades principales del sistema.

### 1. Cargar Datos desde una Fuente Externa (SDSS)

Al iniciar la aplicación, verás el menú principal. Para cargar datos de galaxias desde el SDSS:

1.  **Selecciona la fuente de datos**: Elige la opción `2` para SDSS.
2.  **Ingresa los parámetros de búsqueda**:
    -   **RA (Ascensión Recta)**: `180.0`
    -   **DEC (Declinación)**: `0.0`
    -   **z-min (Redshift mínimo)**: `0.05`
    -   **z-max (Redshift máximo)**: `0.3`

El sistema se conectará al SDSS, descargará los datos y los guardará en un archivo CSV dentro del directorio `data/`.

### 2. Realizar Cálculos Astronómicos

Una vez que los datos están cargados, puedes realizar cálculos sobre ellos:

1.  **Accede al menú de análisis**: Después de cargar los datos, se te presentará el "MENÚ DE ANÁLISIS".
2.  **Selecciona los cálculos**: Elige la opción `1` para "Realizar cálculos astronómicos".
3.  **Elige el cálculo**: Dependiendo de la fuente de datos (para SDSS), puedes seleccionar:
    -   `1. Calcular distancia de Hubble`
    -   `2. Calcular constante de Hubble`

El sistema aplicará los cálculos y mostrará un reporte con los resultados.

### 3. Aplicar Machine Learning (Clustering)

También puedes usar herramientas de Machine Learning sobre los datos cargados:

1.  **Accede al menú de análisis**: Desde el "MENÚ DE ANÁLISIS", selecciona la opción `2` para "Usar herramientas de Machine Learning".
2.  **Selecciona el módulo de Clustering**: En el menú de Machine Learning, elige `1. Módulo de Clustering`.
3.  **Configura y ejecuta el análisis**:
    -   **Selecciona las columnas**: Elige las dos columnas numéricas que deseas analizar (por ejemplo, `redshift` y `concentration_index`).
    -   **Aplica el algoritmo**: Selecciona K-Means e ingresa el número de clusters.
    -   **Genera la gráfica**: El sistema creará una gráfica de dispersión con los clusters identificados.
