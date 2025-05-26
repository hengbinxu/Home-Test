from enum import StrEnum
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

ENV_DIR = ROOT_DIR / "envs"
DRIVER_CONFIG_DIR = ROOT_DIR / "driver_config"
SCREENSHOT_DIR = ROOT_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

ERR_LOGS_DIR = ROOT_DIR / "error_logs"
ERR_LOGS_DIR.mkdir(exist_ok=True)

HTML_REPORTS_DIR = ROOT_DIR / "html_reports"
HTML_REPORTS_DIR.mkdir(exist_ok=True)


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


class DocumentReadyState(StrEnum):
    LOADING = "loading"
    INTERATIVE = "interative"
    COMPLETE = "complete"
