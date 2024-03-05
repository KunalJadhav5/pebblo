import pytest
from unittest.mock import MagicMock, patch
from pebblo.app.config.config_validation import validate_config, DaemonConfig, LoggingConfig, ReportsConfig


@pytest.fixture
def config_dict():
    return {
        "daemon": {"host": "localhost", "port": 8000},
        "logging": {"level": "info"},
        "reports": {"format": "pdf", "renderer": "xhtml2pdf", "outputDir": "~/.pebblo"}
    }


def test_validate_config(config_dict):
    with patch('pebblo.app.config.config_validation.get_full_path', return_value='~/.pebblo'):
        with patch('pebblo.app.config.config_validation.logger.error') as mock_logger_error:
            validate_config(config_dict)
            assert mock_logger_error.call_count == 0


def test_daemon_config_validate():
    config = {"host": "localhost", "port": 8000}
    daemon_config = DaemonConfig(config)
    daemon_config.validate()
    assert not daemon_config.errors


def test_logging_config_validate():
    config = {"level": "info"}
    logging_config = LoggingConfig(config)
    logging_config.validate()
    assert not logging_config.errors


def test_reports_config_validate():
    config = {"format": "pdf", "renderer": "xhtml2pdf", "outputDir": "~/.pebblo"}
    reports_config = ReportsConfig(config)
    reports_config.validate()
    assert not reports_config.errors
