from collections.abc import Callable

from src.constants import DocumentReadyState
from src.webdriver.driver_factory import WebDriver


def present_document_ready_state(
    state: DocumentReadyState,
) -> Callable[[WebDriver], bool]:
    def _predicate(driver: WebDriver) -> bool:
        return driver.execute_script("return document.readyState") == state

    return _predicate


def is_video_playing() -> Callable[[WebDriver], bool]:
    def _predict(driver: WebDriver) -> bool:
        return driver.execute_script(
            """
            const video = document.querySelector('video');
            return video && !video.paused && video.currentTime > 0;
        """
        )

    return _predict
