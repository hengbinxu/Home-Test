from typing import Any

from pydantic import Field, computed_field
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from src.utils.base_model import BaseModel
from src.utils.utils import HelperFuncs
from src.webdriver.base_element import BaseElement
from src.webdriver.base_page import BasePage


class StreamerDetail(BaseModel):
    is_live: bool = Field(default=False)
    channel_id: str
    game_name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    viewers_desc: str | None = Field(default=None)

    @computed_field  # type: ignore
    @property
    def viewers(self) -> int | None:
        if self.viewers_desc:
            viewers_desc = (
                self.viewers_desc.lower()
                .replace("viewers", "")
                .replace("viewer", "")
                .strip()
            )
            return HelperFuncs.parse_number(viewers_desc)

    def is_the_same_game_name(self, game_name: str) -> bool:
        if self.game_name is not None:
            return self.game_name.lower().strip() == game_name.lower().strip()
        else:
            return False


class StreamerListElements(BaseElement[list[WebElement]]):
    def __init__(
        self,
        only_live: bool = False,
        game_name: str | None = None,
        raise_clickable_timeout_exc: bool = False,
        timeout: float = 3,
    ) -> None:
        """
        Get Twitch Streamer List

        Args:
            only_live (bool, optional):
                Only live streamers are included; recommended channels are not.
                Defaults to False.

            game_name (str | None, optional):
                Only get streamers whose game name matches the specified one.
                Defaults to None.

            raise_clickable_timeout_exc (bool, optional): Defaults to False.
            timeout (float, optional): Defaults to 5.
        """
        super().__init__(
            by=By.XPATH,
            value="//*[@id='page-main-content-wrapper']/div/div/div[1]/div/div/div",
            ec_method=EC.visibility_of_all_elements_located,  # type: ignore
            timeout=timeout,
        )
        self.only_live = only_live
        self.raise_clickable_timeout_exc = raise_clickable_timeout_exc
        self.game_name = game_name

    def __extract_streamer_channel_id(self, streamer_element: WebElement) -> str:
        channel_id_element = streamer_element.find_element(by=By.TAG_NAME, value="h2")
        return channel_id_element.text.strip()

    def __extract_streamer_game_name(self, steamer_element: WebElement) -> str | None:
        try:
            game_name_element = steamer_element.find_element(
                by=By.CSS_SELECTOR,
                value="div.Layout-sc-1xcs6mc-0.jCRQex > p.CoreText-sc-1txzju1-0.jtYpeE",
            )
            return game_name_element.text.strip()
        except NoSuchElementException:
            return None

    def __extract_streamer_viewer_desc(self, steamer_element: WebElement) -> str | None:
        try:
            streamer_views_element = steamer_element.find_element(
                by=By.CSS_SELECTOR,
                value="div.Layout-sc-1xcs6mc-0.jCRQex > p.CoreText-sc-1txzju1-0.jSkguG",
            )
            return streamer_views_element.text.strip()
        except NoSuchElementException:
            return None

    def __extract_streamer_description(self, steamer_element: WebElement) -> str | None:
        try:
            description_element = steamer_element.find_element(
                by=By.CSS_SELECTOR,
                value="div.Layout-sc-1xcs6mc-0.jCRQex > p.CoreText-sc-1txzju1-0.gBknDX",
            )
            return description_element.text.strip()
        except NoSuchElementException:
            return None

    def __extract_streamer_info(self, streamer_element: WebElement) -> StreamerDetail:
        element_text = streamer_element.text.split("\n")
        channel_id = self.__extract_streamer_channel_id(streamer_element)
        game_name = self.__extract_streamer_game_name(streamer_element)
        viewer_desc = self.__extract_streamer_viewer_desc(streamer_element)
        description = self.__extract_streamer_description(streamer_element)
        if element_text[0].lower() == "live":
            return StreamerDetail(
                is_live=True,
                channel_id=channel_id,
                game_name=game_name,
                viewers_desc=viewer_desc,
                description=description,
            )
        else:
            return StreamerDetail(is_live=False, channel_id=channel_id)

    def __get__(self, obj: BasePage, owner: Any) -> list[WebElement]:
        streamer_elements = super().__get__(obj, owner)
        avaiable_streamer_elements: list[WebElement] = []
        for element in streamer_elements:
            try:
                # Wait for the element to be clickable
                obj.wait_until(
                    method=EC.element_to_be_clickable,  # type: ignore
                    method_kwargs={"mark": element},
                    timeout=self.timeout,
                )
            except TimeoutException as e:
                obj.log.error(
                    f"text: {element.text} is not clickable, timeout: {self.timeout}"
                )
                if self.raise_clickable_timeout_exc:
                    raise e
                else:
                    continue

            streamer_detail = self.__extract_streamer_info(element)
            # It can do more filter according test scenario.
            if self.game_name is not None:
                if streamer_detail.is_the_same_game_name(self.game_name) is False:
                    continue

            if self.only_live and streamer_detail.is_live:
                avaiable_streamer_elements.append(element)
            else:
                avaiable_streamer_elements.append(element)
        return avaiable_streamer_elements
