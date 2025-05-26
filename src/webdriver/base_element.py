from collections.abc import Callable
from typing import TypeVar

from selenium.webdriver.support import expected_conditions as EC

from src.webdriver.base_page import BasePage
from src.webdriver.driver_generator import WebDriver

T = TypeVar("T")
EcMethod = Callable[..., Callable[[WebDriver], T]]

# TODO: Fix typing


class BaseElement[T]:
    def __init__(
        self,
        obj: BasePage,
        by: str,
        value: str,
        ec_method: EcMethod[T] = EC.presence_of_element_located,  # type: ignore
        timeout: float = 3,
        use_wait_until: bool = True,
    ) -> None:
        self.obj = obj
        self.by = by
        self.value = value
        self.ec_method = ec_method
        self.timeout = timeout
        self.use_wait_until = use_wait_until

    def find(self) -> T:
        if self.use_wait_until:
            return self.obj.wait_until(
                method=self.ec_method,
                method_kwargs={"locator": (self.by, self.value)},
                timeout=self.timeout,
            )  # type: ignore
        else:
            return self.obj.wait_until_not(
                method=self.ec_method,
                method_kwargs={"locator": (self.by, self.value)},
                timeout=self.timeout,
            )  # type: ignore
