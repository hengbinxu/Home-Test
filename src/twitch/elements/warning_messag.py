from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from src.webdriver.base_element import BaseElement
from src.webdriver.base_page import BasePage


class WarningMessageElement(BaseElement[WebElement]):
    def __init__(self, obj: BasePage, timeout: int = 3) -> None:
        super().__init__(
            obj=obj,
            by=By.XPATH,
            value="//div[@data-a-target='content-classification-gate-overlay']",
            timeout=timeout,
            ec_method=EC.visibility_of_element_located,  # type: ignore
        )

    def find(self) -> WebElement:
        self.message_element = super().find()
        return self.message_element

    def click_start_watching_button(self) -> None:
        if hasattr(self, "message_element"):
            self.message_element.find_element(
                by=By.XPATH,
                value="//div[@data-a-target='tw-core-button-label-text']",
            ).click()
        else:
            AttributeError(
                "You have to call find method to set self.message_element first"
            )
