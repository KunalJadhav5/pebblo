import os
from pebblo.app.utils.utils import get_full_path
from pebblo.app.libs.logger import logger, SUPPORTED_LOG_LEVELS
from abc import ABC, abstractmethod
import sys


class ConfigValidator(ABC):
    @abstractmethod
    def validate(self):
        pass


class DaemonConfig(ConfigValidator):
    def __init__(self, config):
        self.port = config.get("port")
        self.host = config.get("host")

    def validate(self):
        # Add validation logic here
        if not isinstance(self.host, str):
            raise ValueError("Error: Unsupported host specified in the configuration")

        try:
            self.port = int(self.port)
        except ValueError:
            logger.error("Error: Port must be an integer")
            sys.exit(1)

        self.port = int(self.port)

        if not (0 < self.port <= 65535):
            logger.error("Error: Port must be between 1 and 65535")
            sys.exit(1)


class LoggingConfig(ConfigValidator):
    def __init__(self, config):
        self.level = config.get('level')

    def validate(self):
        # Check if level is supported or not
        if self.level.upper() not in SUPPORTED_LOG_LEVELS:
            raise ValueError("Error: Unsupported logLevel specified in the configuration")


class ReportsConfig(ConfigValidator):
    def __init__(self, config):
        self.format = config.get("format")
        self.renderer = config.get("renderer")
        self.output_dir = config.get("outputDir")

    def validate(self):
        if self.format not in ["pdf"]:
            raise ValueError("Error: Unsupported format specified in the configuration")
        if self.renderer not in ["weasyprint", "xhtml2pdf"]:
            raise ValueError("Error: Unsupported renderer specified in the configuration")
        if not os.path.exists(get_full_path(self.output_dir)):
            raise FileNotFoundError(
                f"Error: Output directory '{self.output_dir}' specified for the reports does not exist")


def validate_config(config_dict):
    try:
        daemon_config = DaemonConfig(config_dict.get('daemon', {}))
        logging_config = LoggingConfig(config_dict.get('logging', {}))
        reports_config = ReportsConfig(config_dict.get('reports', {}))

        # Validate each section
        daemon_config.validate()
        logging_config.validate()
        reports_config.validate()
    except (ValueError, FileNotFoundError) as e:
        logger.error(f"Error occurred: {str(e)}")
        sys.exit(1)