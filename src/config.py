import logging
from logging.config import dictConfig

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.constants import ENV_DIR, ROOT_DIR, Envs, LogLevel


class Settings(BaseSettings):
    ENV: Envs = Field(default=Envs.TEST)
    LOG_LEVEL: LogLevel = Field(default=LogLevel.INFO)

    model_config = SettingsConfigDict(
        env_file=ENV_DIR / ".env",
        populate_by_name=True,
        case_sensitive=True,
        extra="ignore",
        use_enum_values=True,
    )


settings = Settings()


def logging_config() -> None:
    FMT = "%(asctime)s [%(levelname)s] %(module)s:%(funcName)s (%(lineno)d) %(message)s"
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "class": "logging.Formatter",
                "datefmt": "%Y-%m-%dT%H:%M:%S",
                "format": FMT,
            },
        },
        "handlers": {
            "default": {
                "class": "rich.logging.RichHandler",
                "level": settings.LOG_LEVEL,
                "formatter": "console",
            },
            "rotating_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": logging.ERROR,
                "formatter": "console",
                "filename": ROOT_DIR / "error_logs" / "app.log",
                "maxBytes": 2**23,  # 8MB
                "backupCount": 5,  # Keep 5 backup files
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "__main__": {
                "handlers": ["default", "rotating_file"],
                "level": settings.LOG_LEVEL,
                "propagate": False,
            },
            "tests": {
                "handlers": ["default", "rotating_file"],
                "level": settings.LOG_LEVEL,
                "propagate": False,
            },
            "src": {
                "handlers": ["default", "rotating_file"],
                "level": settings.LOG_LEVEL,
                "propagate": False,
            },
            "unit_tests": {
                "handlers": ["default", "rotating_file"],
                "level": settings.LOG_LEVEL,
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["default", "rotating_file"],
            "level": settings.LOG_LEVEL,
        },
    }
    dictConfig(LOGGING_CONFIG)
