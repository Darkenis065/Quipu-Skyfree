import pytest
from unittest.mock import patch, MagicMock, mock_open, call
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
from ML.NN import AnalisisRegresionNN

@pytest.fixture
def analisis_regresion_nn(mock_rutina_nn):
    """Fixture to create an instance of AnalisisRegresionNN."""
    return AnalisisRegresionNN(mock_rutina_nn)

@pytest.fixture
def mock_rutina_nn():
    """Fixture to mock the Rutina class for NN tests."""
    mock = MagicMock()
    mock.datos_actuales = pd.DataFrame({
        'feature': np.arange(20),
        'target': 2 * np.arange(20) + 1,
        'other': np.random.rand(20)
    })
    mock.cargarDatos.return_value = True
    return mock

def test_cargar_datos_nn_exito(analisis_regresion_nn, mock_rutina_nn):
    """Test successful data loading for NN."""
    analisis_regresion_nn.rutina = mock_rutina_nn
    with patch('builtins.input', return_value='1'):
        assert analisis_regresion_nn.cargar_datos() is True
        assert analisis_regresion_nn.df is not None
        assert len(analisis_regresion_nn.columnas_disponibles) == 3

def test_seleccionar_y_preparar_datos_exito(analisis_regresion_nn):
    """Test successful data preparation for NN."""
    analisis_regresion_nn.df = pd.DataFrame({
        'feature': np.arange(20),
        'target': 2 * np.arange(20) + 1
    })
    analisis_regresion_nn.columnas_disponibles = ['feature', 'target']
    with patch('builtins.input', side_effect=['1', '2']):
        assert analisis_regresion_nn.seleccionar_y_preparar_datos() is True
        assert analisis_regresion_nn.feature_name == 'feature'
        assert analisis_regresion_nn.target_name == 'target'
        assert analisis_regresion_nn.X_train is not None
        assert analisis_regresion_nn.X_val is not None

def test_configurar_hiperparametros_exito(analisis_regresion_nn):
    """Test successful hyperparameter configuration."""
    with patch('builtins.input', side_effect=['32', '16', '8', '10', '16', '0.001']):
        assert analisis_regresion_nn.configurar_hiperparametros() is True
        assert analisis_regresion_nn.hiperparametros['epochs'] == 10

@patch('ML.NN.keras')
def test_entrenar_red_neuronal_exito(mock_keras, analisis_regresion_nn):
    """Test successful neural network training."""
    analisis_regresion_nn.X_train = np.random.rand(16, 1)
    analisis_regresion_nn.y_train = np.random.rand(16, 1)
    analisis_regresion_nn.X_val = np.random.rand(4, 1)
    analisis_regresion_nn.y_val = np.random.rand(4, 1)
    analisis_regresion_nn.hiperparametros = {
        'neuronas_c1': 32, 'neuronas_c2': 16, 'neuronas_c3': 8,
        'epochs': 10, 'batch_size': 16, 'learning_rate': 0.001
    }
    mock_model = MagicMock()
    mock_keras.Sequential.return_value = mock_model
    analisis_regresion_nn.entrenar_red_neuronal()
    mock_model.fit.assert_called_once()

@patch('ML.NN.keras')
@patch('matplotlib.pyplot.show')
def test_graficar_y_registrar_resultados(mock_show, mock_keras, analisis_regresion_nn):
    """Test graphing and result logging."""
    # Mock history
    history_mock = MagicMock()
    history_mock.history = {'val_loss': [0.1], 'val_mae': [0.2], 'loss': [0.3], 'mae': [0.4]}
    analisis_regresion_nn.history = history_mock

    # Mock model and prediction
    mock_model = MagicMock()
    mock_model.predict.return_value = np.random.rand(4, 1)
    mock_keras.models.load_model.return_value = mock_model

    # Setup scalers and data
    analisis_regresion_nn.X_val = np.random.rand(4, 1)
    analisis_regresion_nn.y_val = np.random.rand(4, 1)
    analisis_regresion_nn.X_train = np.random.rand(16, 1)
    analisis_regresion_nn.y_train = np.random.rand(16, 1)
    analisis_regresion_nn.scaler_X.fit(analisis_regresion_nn.X_train)
    analisis_regresion_nn.scaler_y.fit(analisis_regresion_nn.y_train)
    analisis_regresion_nn.feature_name = 'feature'
    analisis_regresion_nn.target_name = 'target'
    analisis_regresion_nn.hiperparametros = {'epochs': 1}


    mock_file = mock_open()
    with patch('builtins.open', mock_file):
        analisis_regresion_nn.graficar_y_registrar_resultados()

    # Check that the specific file was opened and written to
    mock_file.assert_any_call('registro_hiperparametros.txt', 'w')
    assert mock_show.call_count == 3
