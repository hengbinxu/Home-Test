import logging
import time

import pytest
from selenium.common.exceptions import ElementClickInterceptedException

from src.twitch.twitch import TwitchPage
from src.utils.utils import HelperFuncs
from src.webdriver.driver_factory import WebDriver

log = logging.getLogger()


@pytest.mark.web_test
class TestTwitchPage:
    def test_visit_home_page(self, webdriver: WebDriver) -> None:
        twitch_page = TwitchPage(webdriver)
        twitch_page.visit()
        assert (
            twitch_page.get_page_url(twitch_page.PAGE_NAME) == twitch_page.current_url
        )

    def test_search_and_click_random_streamer(self, webdriver: WebDriver) -> None:
        sleep_time = 2  # It's not a good way to handle loading page
        keyword = "StarCraft"
        twitch_page = TwitchPage(webdriver)
        twitch_page.visit_page("directory")
        twitch_page.search_by_keyword(keyword)
        assert twitch_page.current_url == HelperFuncs.url_join(
            twitch_page.get_page_url("search") + f"?term={keyword}"
        )
        twitch_page.click_tab_list("Channels")

        stop_while = False
        while True:
            twitch_page.wait_document_loading_completed()
            time.sleep(sleep_time)
            for _ in range(2):
                twitch_page.scroll_by(0, 300)
                time.sleep(sleep_time)

            streamer_list_elements = twitch_page.streamer_list_elememts.find()
            for _, streamer_element in streamer_list_elements[::-1]:
                try:
                    streamer_element.click()
                    break
                except ElementClickInterceptedException:
                    continue

            try:
                twitch_page.get_loaded_video_element()
                twitch_page.save_screenshot()
                stop_while = True
            except Exception:
                log.error(
                    "A recommended Twitch channel was clicked, "
                    "but since it isn't live, no video is available. "
                    "It is automatically added to the streamer "
                    "list once Selenium locates the target elements."
                )
                # Back to the previous page and locates the target elements again
                twitch_page.back()

            if stop_while:
                break
