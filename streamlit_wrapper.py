import sys
import os
import subprocess
from pathlib import Path

def run_streamlit_app():
    """
    Ejecuta la aplicación Streamlit de forma robusta.
    """
    try:
        # Encuentra la ruta de `app.py` relativo a este script
        wrapper_path = Path(__file__).parent.resolve()
        app_path = wrapper_path / "QuipuGUI" / "app.py"

        if not app_path.exists():
            print(f"Error: No se encontró 'app.py' en la ruta esperada: {app_path}")
            sys.exit(1)

        # Comando para ejecutar Streamlit
        command = [sys.executable, "-m", "streamlit", "run", str(app_path)] + sys.argv[1:]

        print(f"Ejecutando: {' '.join(command)}")

        # Ejecutar el proceso
        subprocess.run(command, check=True)

    except FileNotFoundError:
        print("Error: 'streamlit' no está instalado o no se encuentra en el PATH.")
        print("Asegúrate de haber instalado las dependencias: pip install -r requirements.txt")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"La aplicación Streamlit falló con el código de error {e.returncode}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_streamlit_app()
