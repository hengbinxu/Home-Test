from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from src.webdriver.base_element import BaseElement
from src.webdriver.base_page import BasePage


class TabListElements(BaseElement[list[WebElement]]):
    def __init__(self, obj: BasePage, timeout: int = 3) -> None:
        super().__init__(
            obj=obj,
            by=By.XPATH,
            value='//*[@id="page-main-content-wrapper"]//ul/li',
            ec_method=EC.presence_of_all_elements_located,  # type: ignore
            timeout=timeout,
        )
