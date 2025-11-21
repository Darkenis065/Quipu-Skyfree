# Contenido de mi_paquete_nombre/streamlit_wrapper.py - VERSIÓN ALTERNATIVA

import sys
import os
import subprocess
import QuipuSkyfree

def run_streamlit_app():
    """
    Función alternativa que ejecuta la aplicación Streamlit llamando al binario 'streamlit'.
    """
    
    # Ruta absoluta al directorio principal del paquete
    package_dir = os.path.dirname(QuipuSkyfree.__file__)
    
    # Ruta completa al archivo app.py: paquete/QuipuGUI/app.py
    app_path = os.path.join(
        package_dir,
        'QuipuGUI',
        'app.py'
    )
    
    if not os.path.exists(app_path):
        print(f"Error: No se encontró la aplicación Streamlit en {app_path}")
        sys.exit(1)

    # Creamos el comando: [ 'streamlit', 'run', '/ruta/a/QuipuGUI/app.py', ...args ]
    command = ["streamlit", "run", app_path] + sys.argv[1:]
    
    print(f"Ejecutando: {' '.join(command)}")
    
    # Ejecutamos el comando de Streamlit
    try:
        # Usa subprocess.run para ejecutar el comando en la terminal
        # Esto evita la importación directa de streamlit.cli
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print("Error: El comando 'streamlit' no se encuentra. Asegúrate de que Streamlit esté instalado y en la PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Streamlit terminó con un error: {e}")
        sys.exit(e.returncode)

if __name__ == '__main__':
    run_streamlit_app()
