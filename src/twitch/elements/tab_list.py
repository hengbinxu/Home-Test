from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from src.webdriver.base_element import BaseElement


class TabListElements(BaseElement[list[WebElement]]):
    def __init__(self, timeout: int = 3) -> None:
        super().__init__(
            by=By.XPATH,
            value='//*[@id="page-main-content-wrapper"]//ul/li',
            ec_method=EC.presence_of_all_elements_located,  # type: ignore
            timeout=timeout,
        )
