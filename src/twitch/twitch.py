from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from src.config import settings
from src.twitch.elements.search_element import SearchElement
from src.twitch.elements.streamer_list import StreamerListElements
from src.twitch.elements.tab_list import TabListElements
from src.twitch.elements.video_element import VideoElement
from src.twitch.elements.warning_messag import WarningMessageElement
from src.utils.url_router import UrlRouter
from src.webdriver.base_page import BasePage
from src.webdriver.driver_factory import WebDriver


class TwitchRouter(UrlRouter):
    ROUTER = {"home": "", "directory": "/directory", "search": "/search"}

    def __init__(self) -> None:
        super().__init__(host=settings.TWITCH_HOST)


class TwitchPage(BasePage):
    PAGE_NAME = "home"

    def __init__(self, webdriver: WebDriver) -> None:
        super().__init__(webdriver, TwitchRouter())
        self.search_element = SearchElement(obj=self)
        self.tab_list_elemets = TabListElements(obj=self)
        self.streamer_list_elememts = StreamerListElements(obj=self)
        self.warning_msg_element = WarningMessageElement(obj=self)
        self._video_element = VideoElement(obj=self)

    def search_by_keyword(self, keyword: str) -> None:
        search_element = self.search_element.find()
        search_element.click()
        search_element.send_keys(keyword)
        search_element.send_keys(Keys.ENTER)

    def click_tab_list(self, cliecked_tab_name: str) -> None:
        tab_list_elements = self.tab_list_elemets.find()
        for tab_element in tab_list_elements:  # type: ignore
            if tab_element.text.lower().strip() == cliecked_tab_name.lower().strip():
                tab_element.click()
                self.log.debug(f"Click the tab name: {cliecked_tab_name}")
                return
        raise ValueError(
            f"Can't find the clicked_tab_name: {cliecked_tab_name} "
            f"in tab_names: {[tab_name.text for tab_name in tab_list_elements]}"
        )

    def get_loaded_video_element(self) -> WebElement:
        video_element = self._video_element.find()
        self.wait_video_playing()
        return video_element
