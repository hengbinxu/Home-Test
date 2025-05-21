from enum import StrEnum
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

ENV_DIR = ROOT_DIR / "envs"
DRIVER_CONFIG_DIR = ROOT_DIR / "driver_config"


class Envs(StrEnum):
    DEV = "dev"
    PROD = "prod"
    TEST = "test"


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Browser(StrEnum):
    CHROME = "chrome"
    EDGE = "edge"
    SAFARI = "safari"
    FIREFOX = "firefox"
