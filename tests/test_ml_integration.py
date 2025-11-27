import pytest
from unittest.mock import patch, MagicMock

# Asegurar que los módulos del proyecto se puedan importar
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skyfree.rutinas import Rutina
from ML.MachineL import MenuML

@patch('ML.MachineL.AnalisisDatos')
@patch('builtins.input', side_effect=['1', '0'])
def test_ml_integration_passes_rutina_to_cluster(mock_input, mock_analisis_datos):
    """
    Prueba la integración para asegurar que MenuML instancia AnalisisDatos
    pasándole correctamente el objeto 'rutina'.
    """
    # Mock para evitar que el método menu() real se ejecute
    mock_analisis_datos.return_value.menu = MagicMock()

    # 1. Crear una instancia de Rutina
    rutina_instance = Rutina()

    # 2. Crear una instancia de MenuML, pasándole la rutina
    menu_ml = MenuML(rutina=rutina_instance)

    # 3. Ejecutar el menú que instancia AnalisisDatos
    menu_ml.mostrar_menu()

    # 4. Verificar que AnalisisDatos fue instanciado con el objeto rutina
    mock_analisis_datos.assert_called_once_with(rutina_instance)
