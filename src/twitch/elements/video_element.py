from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from src.webdriver.base_element import BaseElement
from src.webdriver.base_page import BasePage


class VideoElement(BaseElement[WebElement]):
    def __init__(
        self,
        obj: BasePage,
        timeout: int = 3,
    ) -> None:
        super().__init__(
            obj=obj,
            by=By.XPATH,
            value="//div[@data-test-selector='video-player__video-layout']",
            ec_method=EC.visibility_of_element_located,  # type: ignore
            timeout=timeout,
        )
