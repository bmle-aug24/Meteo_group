import pytest
import pandas as pd
import os
from unittest.mock import patch
from src.preprocess import remove_nan_target, preprocess_data, save_processed_data, load_config  # Mise à jour du chemin

# Test data
@pytest.fixture
def sample_data():
    data = {
        "Date": ["2025-01-01", "2025-01-02", None],
        "Location": ["Sydney", "Melbourne", None],
        "Rainfall": [1.2, None, 0.8],
        "RainTomorrow": ["Yes", "No", None],
    }
    return pd.DataFrame(data)


def test_remove_nan_target(sample_data):
    cleaned_data = remove_nan_target(sample_data, "RainTomorrow")
    assert len(cleaned_data) == 2  # Only two rows remain after removing NaN in the target column
    assert cleaned_data["RainTomorrow"].isnull().sum() == 0


def test_preprocess_data(sample_data):
    processed_data = preprocess_data(sample_data, "RainTomorrow")
    assert "Date" in processed_data.columns
    assert processed_data["Date"].dtype == pd.Int64Dtype()  # Vérifier le type correct (Int64Dtype, pour gérer les NaN)
    assert processed_data["Location"].dtype == "int64"  # Vérifier que Location est encodé en int64 # No NaNs remain


@patch("subprocess.run")  # Mise à jour du patch pour subprocess
def test_save_processed_data(mock_subprocess, tmpdir):
    # Simulate processed data
    X_train = pd.DataFrame({"col1": [1, 2, 3]})
    X_test = pd.DataFrame({"col1": [4, 5]})
    y_train = pd.Series([1, 0, 1])
    y_test = pd.Series([0, 1])

    # Temp directory for saving files
    config = {
        "data": {"processed_dir": tmpdir.strpath}
    }

    save_processed_data(X_train, X_test, y_train, y_test, config)

    # Check if files exist
    assert os.path.exists(os.path.join(tmpdir, "X_train.csv"))
    assert os.path.exists(os.path.join(tmpdir, "X_test.csv"))
    assert os.path.exists(os.path.join(tmpdir, "y_train.csv"))
    assert os.path.exists(os.path.join(tmpdir, "y_test.csv"))

    # Ensure DVC was called
    assert mock_subprocess.call_count == 4


def test_load_config(tmpdir):
    yaml_path = tmpdir.join("config.yaml")
    yaml_path.write(
        """
        data:
          raw_data_path: "data/raw/weather.csv"
          processed_dir: "data/processed/"
        model:
          target_column: "RainTomorrow"
        """
    )
    config = load_config(str(yaml_path))
    assert config["data"]["raw_data_path"] == "data/raw/weather.csv"
    assert config["data"]["processed_dir"] == "data/processed/"

