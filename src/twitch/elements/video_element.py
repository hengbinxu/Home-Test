from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.webdriver.base_element import BaseElement


class VideoElement(BaseElement):
    def __init__(
        self,
        timeout: int = 3,
    ) -> None:
        super().__init__(
            by=By.XPATH,
            value="//div[@data-test-selector='video-player__video-layout']",
            ec_method=EC.visibility_of_element_located,
            timeout=timeout,
        )
