import logging
from pathlib import Path
from typing import Any

from pydantic import Field, computed_field

from src.constants import DRIVER_CONFIG_DIR, Browser
from src.utils.base_model import BaseModel
from src.utils.utils import HelperFuncs

DEFAULT_CHROME_OPTIONS = [
    "--disable-gpu",
    "--no-sandbox",
]

DEFAULT_CHROME_CAPABILITIES = {
    "goog:loggingPrefs": {
        "performance": "ALL",
        "browser": "ALL",
        "client": "ALL",
        "server": "ALL",
        "driver": "ALL",
    },
    "timeouts": {
        "implicit": 10 * 1000,
        "pageLoad": 30 * 1000,
    },
}


class DriverConfig(BaseModel):
    browser: Browser = Browser.CHROME
    remote_url: str | None = None
    driver_path: str | None = None
    capabilities_: dict[str, Any] = Field(default_factory=dict, repr=False)
    browser_options_: list[str] = Field(default_factory=list, repr=False)
    experimental_options: dict[str, Any] = Field(default_factory=dict)
    extension_paths: list[str] = Field(default_factory=list)
    webdriver_kwargs: dict[str, Any] = Field(default_factory=dict)
    page_load_wait_time: float = 0
    implicitly_wait: float = 10

    @computed_field
    @property
    def capabilities(self) -> dict[str, Any]:
        if self.capabilities_:
            return self.capabilities_
        else:
            if self.browser == Browser.CHROME:
                return DEFAULT_CHROME_CAPABILITIES
            else:
                return self.capabilities_

    @computed_field
    @property
    def browser_options(self) -> list[str]:
        if self.browser_options_:
            return self.browser_options_
        else:
            if self.browser == Browser.CHROME:
                return DEFAULT_CHROME_OPTIONS
            else:
                return self.browser_options_


class LogConfig(BaseModel):
    screenshot_on: bool = True


class ViewportConfig(BaseModel):
    maximize: bool = True
    width: int = 1440
    height: int = 900
    orientation: str = "portrait"


class WebDriverConfig(BaseModel):
    driver: DriverConfig = Field(default=DriverConfig())
    log: LogConfig = Field(default=LogConfig())
    viewport: ViewportConfig = Field(default=ViewportConfig())


class WebDriverConfigFactory:
    """
    Webdriver configuration factory
    """

    CHROME_CONFIG_PATH = DRIVER_CONFIG_DIR / "chrome_config.json"
    SAFARI_CONFIG_PATH = DRIVER_CONFIG_DIR / "safari_config.json"
    FIREFOX_CONFIG_PATH = DRIVER_CONFIG_DIR / "firefox_config.json"
    EDGE_CONFIG_PATH = DRIVER_CONFIG_DIR / "edge_config.json"

    log = logging.getLogger()

    @classmethod
    def get_config_path(cls, browser: Browser) -> Path:
        match browser:
            case Browser.CHROME:
                return cls.CHROME_CONFIG_PATH

            case Browser.SAFARI:
                return cls.SAFARI_CONFIG_PATH

            case Browser.FIREFOX:
                return cls.FIREFOX_CONFIG_PATH

            case Browser.EDGE:
                return cls.EDGE_CONFIG_PATH

            case _:
                raise ValueError(f"{browser} isn't support. Can't get config_path.")

    @classmethod
    def get_config(cls, browser: Browser, **override_settings: Any) -> WebDriverConfig:
        fp = cls.get_config_path(browser)
        json_config = HelperFuncs.load_json(fp)
        if json_config:
            json_config = {**json_config, **override_settings}
            return WebDriverConfig(**json_config)
        else:
            cls.log.debug("Use default config")
            return WebDriverConfig()
