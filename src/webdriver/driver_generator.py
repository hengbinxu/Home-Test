import logging
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, override

from selenium.common.exceptions import WebDriverException

from src.webdriver.driver_factory import DriverFactory, WebDriver
from src.webdriver.webdriver_config import WebDriverConfig


class WebDriverGenerator:
    log = logging.getLogger()

    def __init__(self, webdriver_config: WebDriverConfig) -> None:
        self.webdriver_config = webdriver_config
        self._webdriver: WebDriver | None = None

    def init_webdriver(self) -> WebDriver:
        driver_factory = DriverFactory(
            browser=self.webdriver_config.driver.browser,
            driver_path=self.webdriver_config.driver.driver_path,
            capabilities=self.webdriver_config.driver.capabilities,
            browser_options=self.webdriver_config.driver.browser_options,
            experimental_options=self.webdriver_config.driver.experimental_options,
            extension_paths=self.webdriver_config.driver.extension_paths,
            webdriver_kwargs=self.webdriver_config.driver.webdriver_kwargs,
        )
        self._webdriver = driver_factory.get_webdriver()
        self._webdriver.implicitly_wait(self.webdriver_config.driver.implicitly_wait)
        caps = self._webdriver.capabilities
        try:
            self.log.debug(
                f"[WebDriverGenerator] Capabilities: "
                f"browserName: {caps['browserName']}, "
                f"browserVersion: {caps['browserVersion']}, "
                f"platformName: {caps['platformName']}, "
                f"session_id: {self.session_id}"
            )
        except Exception as e:
            self.log.error(
                "[WebDriverGenerator] webdriver.capabilities did not have a  "
                "key that BrowserEngine was expecting. "
                "Is your driver executable the right version?"
            )
            raise e
        # Initial Browser Setup
        if self.webdriver_config.driver.page_load_wait_time:
            self.set_page_load_out(self.webdriver_config.driver.page_load_wait_time)

        if self.webdriver_config.viewport.maximize:
            self.maximize_window()
        else:
            self.viewport(
                width=self.webdriver_config.viewport.width,
                height=self.webdriver_config.viewport.height,
                orientation=self.webdriver_config.viewport.orientation,
            )

        return self._webdriver

    @property
    def session_id(self) -> str:
        return self._webdriver.session_id  # type: ignore

    @property
    def webdriver(self) -> WebDriver:
        return self.init_webdriver() if self._webdriver is None else self._webdriver

    def set_page_load_out(self, time_to_wait: float) -> None:
        self.webdriver.set_page_load_timeout(time_to_wait)

    def maximize_window(self) -> None:
        try:
            self.webdriver.maximize_window()
        except WebDriverException as e:
            self.log.error(f"[WebDriverGenerator] Can't maximize window: {e.msg}")

    def viewport(
        self,
        width: int,
        height: int,
        orientation: str = "portrait",
    ) -> None:
        """
        Control the size and orientation of the current context's browser window.
        Args:
            width: The width in pixels
            height: The height in pixels
            orientation: default is 'portrait'. Pass 'landscape' to
                reverse the width/height.
        Examples:
            viewport(1280, 800) # macbook-13 size
            viewport(1440, 900) # macbook-15 size
            viewport(375, 667)  # iPhone X size
        """
        self.log.debug(
            f"[WebDriverGenerator] Viewport set to width={width}, "
            f"height={height}, orientation={orientation}"
        )
        if orientation == "portrait":
            self.webdriver.set_window_size(width, height)
        elif orientation == "landscape":
            self.webdriver.set_window_size(height, width)
        else:
            raise ValueError("Orientation must be `portrait` or `landscape`.")

    @contextmanager
    def auto_webdriver(self) -> Generator[WebDriver, Any, None]:
        try:
            yield self.webdriver
        except Exception as e:
            caps = self.webdriver.capabilities
            self.log.error(
                f"[WebDriverGenerator] Capabilities: "
                f"browserName: {caps['browserName']}, "
                f"browserVersion: {caps['browserVersion']}, "
                f"platformName: {caps['platformName']}, "
                f"session_id: {self.session_id} "
                f"occur unexpected error."
            )
            raise e
        finally:
            self.quit()

    def quit(self) -> None:
        """
        Quits the driver.

        Closes any and every window/tab associated with the current session.
        """
        self.webdriver.quit()
        self.log.debug(
            "[WebDriverGenerator] Quit webdriver and close all windows "
            f"from the browser session. session_id: {self.session_id}"
        )

    @override
    def __repr__(self) -> str:
        return (
            f"<WebDriverGenerator webdriver_config: {self.webdriver_config}, "
            f"session_id: {self.session_id}"
        )
