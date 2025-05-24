import logging
from collections.abc import Generator
from typing import Any, cast

import pytest

from src.constants import Browser
from src.utils.utils import HelperFuncs
from src.webdriver.driver_factory import WebDriver
from src.webdriver.driver_generator import WebDriverGenerator
from src.webdriver.webdriver_config import WebDriverConfig, WebDriverConfigFactory

log = logging.getLogger()


def __get_error_msg(driver_config: WebDriverConfig) -> str:
    """
    Get the error message for executing selenium error

    Args:
        driver_config (WebDriverConfig)
    """
    err_msg = (
        "Unexpected error while executing the selenium, "
        f"browser: {driver_config.driver.browser}"
    )
    if driver_config.driver.remote_url:
        err_msg += f", remote_url: {driver_config.driver.remote_url}"
    return err_msg


def pytestsession_start(session: pytest.Session) -> None:
    session.start_at = HelperFuncs.get_current_ts()  # type: ignore


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser",
        dest="browser",
        action="store",
        type=Browser,
        default=Browser.CHROME,
        help="Which drive will be used",
    )


@pytest.fixture()
def webdriver(request: pytest.FixtureRequest) -> Generator[WebDriver, Any, None]:
    browser = cast(Browser, request.config.getoption("--browser"))
    driver_config = WebDriverConfigFactory.get_config(browser)
    webdriver_generator = WebDriverGenerator(driver_config)
    try:
        yield webdriver_generator.webdriver
    except Exception as e:
        log.error(__get_error_msg(driver_config))
        raise e
    finally:
        webdriver_generator.quit()
