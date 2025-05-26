from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.webdriver.base_element import BaseElement
from src.webdriver.base_page import BasePage


class SearchElement(BaseElement[WebElement]):
    def __init__(self, obj: BasePage, timeout: int = 3) -> None:
        super().__init__(
            obj=obj,
            by=By.XPATH,
            value="//*[@id='twilight-sticky-header-root']/div/div/div/div/input",
            timeout=timeout,
        )
