import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any, Self

from selenium.types import WaitExcTypes
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import POLL_FREQUENCY, WebDriverWait

from src.constants import SCREENSHOT_DIR, DocumentReadyState
from src.utils.url_router import UrlRouter
from src.utils.utils import HelperFuncs
from src.webdriver.custom_wait_conditions import (
    is_video_playing,
    present_document_ready_state,
)
from src.webdriver.driver_factory import WebDriver


class BasePage:
    log = logging.getLogger()

    PAGE_NAME: str

    def __init__(self, webdriver: WebDriver, url_router: UrlRouter) -> None:
        self.webdriver = webdriver
        self.url_router = url_router

    def visit(self) -> None:
        self.visit_page(self.PAGE_NAME)

    @property
    def action_chain(self) -> ActionChains:
        return ActionChains(self.webdriver)

    @property
    def window_size(self) -> dict[str, int]:
        return self.webdriver.get_window_size()

    @property
    def session_id(self) -> str:
        return self.webdriver.session_id  # type: ignore

    @property
    def page_title(self) -> str:
        return self.webdriver.title

    @property
    def current_url(self) -> str:
        return self.webdriver.current_url

    def get_page_url(self, page_name: str) -> str:
        return self.url_router.get_api_url(page_name)

    def visit_page(self, page_name: str) -> None:
        page_url = self.get_page_url(page_name)
        self.webdriver.get(page_url)
        self.log.debug(f"Visit the page_name: {page_name}, url: {page_url}")

    def reload(self) -> Self:
        self.webdriver.refresh()
        self.log.debug(f"Reload the current page, url: {self.current_url}")
        return self

    def find_element(self, by: str = By.ID, value: str | None = None) -> WebElement:
        return self.webdriver.find_element(by, value)

    def find_elements(
        self, by: str = By.ID, value: str | None = None
    ) -> list[WebElement]:
        return self.find_elements(by, value)

    def _webdriver_wait(
        self,
        timeout: float,
        poll_frequence: float = POLL_FREQUENCY,
        ignore_exceptions: WaitExcTypes | None = None,
    ) -> WebDriverWait:
        return WebDriverWait(
            driver=self.webdriver,
            timeout=timeout,
            poll_frequency=poll_frequence,
            ignored_exceptions=ignore_exceptions,
        )

    def wait_until[T](
        self,
        *,
        method: Callable[[WebDriver], T],
        method_kwargs: dict[Any, Any],
        timeout: float,
        poll_frequence: float = POLL_FREQUENCY,
        ignore_exceptions: WaitExcTypes | None = None,
        message: str = "",
    ) -> T:
        return self._webdriver_wait(
            timeout=timeout,
            poll_frequence=poll_frequence,
            ignore_exceptions=ignore_exceptions,
        ).until(method(**method_kwargs), message=message)  # type: ignore

    def wait_until_not[T](
        self,
        method: Callable[[WebDriver], T],
        method_kwargs: dict[Any, Any],
        timeout: float = 10.0,
        ignore_exceptions: WaitExcTypes | None = None,
        message: str = "",
    ) -> T:
        return self._webdriver_wait(
            timeout=timeout, ignore_exceptions=ignore_exceptions
        ).until_not(method=method(**method_kwargs), message=message)  # type: ignore

    def execute_script(self, javascript: str, *args: tuple[Any, ...]) -> Any:
        """
        Executes javascript in the current window or frame.

        Args:
            javascript: The script string to execute.
            args: Any arguments to be used in the script.
        """
        self.log.debug("Execute javascript into the Browser")
        return self.webdriver.execute_script(javascript, *args)

    def scroll_by(self, x: int, y: int) -> None:
        self.execute_script(f"window.scrollBy({x}, {y});")
        self.log.debug(f"Scroll by x: {x}, y: {y}")

    def get_document_ready_state(self) -> str:
        state = self.execute_script("return document.readyState")
        return state

    def wait_document_loading_completed(self) -> None:
        """
        An easy way to check document whether the document has fully loaded or not
        """
        self.wait_until(
            method=present_document_ready_state,  # type: ignore
            method_kwargs={"state": DocumentReadyState.COMPLETE},
            timeout=3,
        )

    def wait_video_playing(self) -> None:
        self.wait_until(method=is_video_playing, method_kwargs={}, timeout=5)  # type: ignore

    def quit(self) -> None:
        """
        Quits the driver.

        Closes any and every window/tab associated with the current session.
        """
        self.webdriver.quit()
        self.log.debug(
            "Quit webdriver and close all windows "
            f"from the browser session. session_id: {self.session_id}"
        )

    def get_element_all_attrs(self, element: WebElement) -> dict[str, str]:
        js = """
            var items = {};
            for (index = 0; index < arguments[0].attributes.length; ++index) {
                items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value
            }; return items;
        """  # noqa: E501
        return self.execute_script(js, element)  # type: ignore

    def find_element_all_attrs(
        self, by: str = By.ID, value: str | None = None
    ) -> dict[str, str]:
        element = self.find_element(by, value)
        return self.get_element_all_attrs(element)

    def __get_default_screenshot_fp(self) -> Path:
        current = HelperFuncs.get_current_utc_with_format("%Y-%m-%d-%H-%M-%S")
        return SCREENSHOT_DIR / f"{current}.png"

    def save_screenshot(self, fp: Path | None = None) -> None:
        if fp is None:
            fp = self.__get_default_screenshot_fp()
        self.webdriver.save_screenshot(fp)
        self.log.debug(f"Successfully save screenshot into {fp}")

    def back(self) -> None:
        """
        Goes one step backward in the browser history
        """
        self.webdriver.back()
        self.log.debug(f"Back to previois page: {self.current_url}")
