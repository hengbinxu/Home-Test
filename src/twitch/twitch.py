from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from src.config import settings
from src.twitch.elements.search_element import SearchElement
from src.twitch.elements.streamer_list import StreamerListElements
from src.twitch.elements.tab_list import TabListElements
from src.twitch.elements.video_element import VideoElement
from src.utils.url_router import UrlRouter
from src.webdriver.base_page import BasePage
from src.webdriver.driver_factory import WebDriver


class TwitchRouter(UrlRouter):
    ROUTER = {"home": "", "directory": "/directory", "search": "/search"}

    def __init__(self) -> None:
        super().__init__(host=settings.TWITCH_HOST)


class TwitchPage(BasePage):
    PAGE_NAME = "home"
    search_element = SearchElement()
    tab_list_elemets = TabListElements()
    streamer_list_elememts = StreamerListElements(only_live=True)
    _video_element = VideoElement()

    def __init__(self, webdriver: WebDriver) -> None:
        super().__init__(webdriver, TwitchRouter())

    @classmethod
    def adjust_streamer_list_elements_init_args(
        cls,
        on_live: bool = True,
        game_name: str | None = None,
        raise_clickable_timeout_exc: bool = False,
        timeout: float = 3,
    ) -> None:
        cls.streamer_list_elememts = StreamerListElements(
            only_live=on_live,
            game_name=game_name,
            raise_clickable_timeout_exc=raise_clickable_timeout_exc,
            timeout=timeout,
        )

    def search_by_keyword(self, keyword: str) -> None:
        self.search_element.click()
        self.search_element.send_keys(keyword)
        self.search_element.send_keys(Keys.ENTER)

    def click_tab_list(self, cliecked_tab_name: str) -> None:
        for tab_element in self.tab_list_elemets:  # type: ignore
            if tab_element.text.lower().strip() == cliecked_tab_name.lower().strip():
                tab_element.click()
                self.log.debug(f"Click the tab name: {cliecked_tab_name}")
                return
        raise ValueError(
            f"Can't find the clicked_tab_name: {cliecked_tab_name} "
            f"in tab_names: {[tab_name.text for tab_name in self.tab_list_elemets]}"
        )

    def get_loaded_video_element(self) -> WebElement:
        video_element = self._video_element
        self.wait_video_playing()
        return video_element
