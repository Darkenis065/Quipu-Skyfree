import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from ML.Cluster import AnalisisDatos

@pytest.fixture
def analisis_datos():
    """Fixture to create an instance of AnalisisDatos."""
    return AnalisisDatos()

@pytest.fixture
def mock_rutina():
    """Fixture to mock the Rutina class."""
    mock = MagicMock()
    mock.datos_actuales = pd.DataFrame({
        'col1': np.random.rand(10),
        'col2': np.random.rand(10),
        'col3': np.random.rand(10)
    })
    mock.cargarDatos.return_value = True
    return mock

def test_cargar_datos_exito(analisis_datos, mock_rutina):
    """Test successful data loading."""
    analisis_datos.rutina = mock_rutina
    with patch('builtins.input', return_value='1'):
        assert analisis_datos.cargar_datos() is True
        assert analisis_datos.df is not None
        assert len(analisis_datos.columnas_disponibles) == 3

def test_cargar_datos_fallido(analisis_datos, mock_rutina):
    """Test failed data loading."""
    mock_rutina.cargarDatos.return_value = False
    analisis_datos.rutina = mock_rutina
    with patch('builtins.input', return_value='1'):
        assert analisis_datos.cargar_datos() is False
        assert analisis_datos.df is None

def test_seleccionar_columnas_exito(analisis_datos):
    """Test successful column selection."""
    analisis_datos.df = pd.DataFrame({
        'col1': np.random.rand(10),
        'col2': np.random.rand(10),
        'col3': np.random.rand(10)
    })
    analisis_datos.columnas_disponibles = ['col1', 'col2', 'col3']
    with patch('builtins.input', side_effect=['1', '2']):
        assert analisis_datos.seleccionar_columnas() is True
        assert analisis_datos.columnas_elegidas == ['col2', 'col1']
        assert analisis_datos.X_scaled is not None

def test_seleccionar_columnas_invalidas(analisis_datos):
    """Test invalid column selection."""
    analisis_datos.df = pd.DataFrame({
        'col1': np.random.rand(10),
        'col2': np.random.rand(10),
    })
    analisis_datos.columnas_disponibles = ['col1', 'col2']
    with patch('builtins.input', side_effect=['1', '1']):
        assert analisis_datos.seleccionar_columnas() is False

def test_aplicar_clustering_kmeans_exito(analisis_datos):
    """Test successful K-Means clustering."""
    analisis_datos.X_scaled = np.random.rand(10, 2)
    with patch('builtins.input', side_effect=['1', '3']):
        assert analisis_datos.aplicar_clustering() is True
        assert analisis_datos.labels is not None

def test_aplicar_clustering_hdbscan_exito(analisis_datos):
    """Test successful HDBSCAN clustering."""
    analisis_datos.X_scaled = np.random.rand(10, 2)
    with patch('builtins.input', return_value='2'):
        assert analisis_datos.aplicar_clustering() is True
        assert analisis_datos.labels is not None

def test_graficar_clusters(analisis_datos):
    """Test cluster graphing."""
    analisis_datos.X_scaled = np.random.rand(10, 2)
    analisis_datos.labels = np.random.randint(0, 2, 10)
    analisis_datos.df = pd.DataFrame({'col1': np.random.rand(10), 'col2': np.random.rand(10)})
    analisis_datos.columnas_elegidas = ['col1', 'col2']
    with patch('matplotlib.pyplot.show') as mock_show:
        analisis_datos.graficar_clusters()
        mock_show.assert_called_once()
