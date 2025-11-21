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

- `Calculations/`: Contiene la lógica para los cálculos astronómicos.
- `DB/`: Gestiona la conexión y consulta a las bases de datos astronómicas.
- `ML/`: Implementa los algoritmos de machine learning.
- `Routines/`: Orquesta el flujo de la aplicación y contiene el menú principal.
- `routines/data/`: Directorio donde se guardan los datasets descargados.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/Quipu-Skyfree.git
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Para iniciar la aplicación, ejecuta el siguiente comando desde el directorio raíz del proyecto:

```bash
python Routines/rutinas.py
```

Esto iniciará el menú interactivo en la línea de comandos, donde podrás seleccionar la fuente de datos, realizar cálculos y aplicar análisis de machine learning.
