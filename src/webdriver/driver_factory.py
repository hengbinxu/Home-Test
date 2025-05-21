import logging
from typing import Any, override

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.webdriver import WebDriver as EdgeWebDriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.safari.webdriver import WebDriver as SafariWebDriver

from src.constants import Browser

type WebOptions = (
    webdriver.ChromeOptions
    | webdriver.EdgeOptions
    | webdriver.SafariOptions
    | webdriver.FirefoxOptions
)
type WebDriver = (
    ChromeWebDriver
    | SafariWebDriver
    | EdgeWebDriver
    | FirefoxWebDriver
    | RemoteWebDriver
)


class DriverFactory:
    log = logging.getLogger()

    def __init__(
        self,
        *,
        browser: Browser,
        remote_url: str | None = None,
        driver_path: str | None = None,
        capabilities: dict[str, Any] | None = None,
        browser_options: list[str] | None = None,
        experimental_options: dict[str, Any] | None = None,
        extension_paths: list[str] | None = None,
        webdriver_kwargs: dict[str, Any] | None = None,
    ) -> None:
        self.browser = browser
        self.remote_url = remote_url
        self.driver_path = driver_path
        self.capabilities = capabilities
        self.browser_options = browser_options
        self.experimental_options = experimental_options
        self.extension_paths = extension_paths
        self.webdriver_kwargs = webdriver_kwargs

    def _build_capabilities(
        self, capabilities: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        caps = {}
        match self.browser:
            case Browser.CHROME:
                caps.update(webdriver.DesiredCapabilities.CHROME.copy())

            case Browser.EDGE:
                caps.update(webdriver.DesiredCapabilities.EDGE.copy())

            case Browser.SAFARI:
                caps.update(webdriver.DesiredCapabilities.SAFARI.copy())

            case Browser.FIREFOX:
                caps.update(webdriver.DesiredCapabilities.FIREFOX.copy())

            case _:
                raise ValueError(
                    f"{self.browser} isn't support. Can't build capabilities."
                )
        if capabilities:
            caps.update(capabilities)
        return caps

    def _build_options(
        self,
        *,
        browser_options: list[str] | None = None,
        experimental_options: dict[str, Any] | None = None,
        extension_paths: list[str] | None = None,
    ) -> WebOptions:
        match self.browser:
            case Browser.CHROME:
                options = webdriver.ChromeOptions()

            case Browser.EDGE:
                options = webdriver.EdgeOptions()

            case Browser.SAFARI:
                options = webdriver.SafariOptions()

            case Browser.FIREFOX:
                options = webdriver.FirefoxOptions()

            case _:
                raise ValueError(f"{self.browser} isn't support. Can't build options.")

        if browser_options:
            for option in browser_options:
                if option.startswith("--"):
                    options.add_argument(option)
                else:
                    options.add_argument(f"--{option}")

        if experimental_options:
            for name, value in experimental_options.items():
                options.add_experimental_option(name, value)  # type: ignore

        if extension_paths:
            for path in extension_paths:
                options.add_extension(path)  # type: ignore
        return options

    def _build_browser_options(self) -> WebOptions:
        caps = self._build_capabilities(self.capabilities)
        browser_options = self._build_options(
            browser_options=self.browser_options,
            experimental_options=self.experimental_options,
            extension_paths=self.extension_paths,
        )
        for name, value in caps.items():
            browser_options.set_capability(name, value)
        return browser_options

    def _build_chrome_driver(self) -> ChromeWebDriver:
        browser_options = self._build_browser_options()
        driver = webdriver.Chrome(
            options=browser_options,  # type: ignore
            service=ChromeService(executable_path=self.driver_path),
            **(self.webdriver_kwargs or {}),
        )
        driver.execute_cdp_cmd("Performance.enable", {})
        return driver

    def _build_edge_driver(self) -> EdgeWebDriver:
        browser_options = self._build_browser_options()
        return EdgeWebDriver(
            service=EdgeService(executable_path=self.driver_path),  # type: ignore
            options=browser_options,  # type: ignore
            **(self.webdriver_kwargs or {}),
        )

    def _build_firefox_driver(self) -> FirefoxWebDriver:
        browser_options = self._build_browser_options()
        return FirefoxWebDriver(
            service=FirefoxService(executable_path=self.driver_path),  # type: ignore
            options=browser_options,  # type: ignore
            **(self.webdriver_kwargs or {}),
        )

    def _build_safari_driver(self) -> SafariWebDriver:
        """
        Build Safari driver

        Note:
            Run `safaridriver --enable` once
        """
        browser_options = self._build_browser_options()
        return SafariWebDriver(
            service=SafariService(executable_path=self.driver_path),  # type: ignore
            options=browser_options,  # type: ignore
            **(self.webdriver_kwargs or {}),
        )

    def _build_remote_driver(self) -> RemoteWebDriver:
        browser_options = self._build_browser_options()
        return RemoteWebDriver(
            command_executor=self.remote_url,  # type: ignore
            options=browser_options,
            **(self.webdriver_kwargs or {}),
        )

    def get_webdriver(self) -> WebDriver:
        if self.remote_url:
            self.log.debug(f"Use remote driver, remote_url: {self.remote_url}")
            return self._build_remote_driver()

        self.log.debug(
            f"Use local driver, browser: {self.browser}, "
            f"caps: {self.capabilities}, "
            f"options: {self.browser_options}, "
            f"experimental_options: {self.experimental_options}, "
            f"extension_paths: {self.extension_paths}, "
            f"webdriver_kwargs: {self.webdriver_kwargs}"
        )
        match self.browser:
            case Browser.CHROME:
                return self._build_chrome_driver()
            case Browser.EDGE:
                return self._build_edge_driver()
            case Browser.SAFARI:
                return self._build_safari_driver()
            case Browser.FIREFOX:
                return self._build_firefox_driver()
            case _:
                raise ValueError(f"{self.browser} isn't support. Can't get driver.")

    @override
    def __repr__(self) -> str:
        return (
            f"<DriverFactory browser: {self.browser}, "
            f"caps: {self.capabilities}, "
            f"options: {self.browser_options}, "
            f"experimental_options: {self.experimental_options}, "
            f"extension_paths: {self.extension_paths}, "
            f"webdriver_kwargs: {self.webdriver_kwargs}>"
        )
