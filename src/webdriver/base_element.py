from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

from selenium.webdriver.support import expected_conditions as EC

from src.webdriver.base_page import BasePage
from src.webdriver.driver_generator import WebDriver

T = TypeVar("T")
P = ParamSpec("P")

EcMethod = Callable[..., Callable[[WebDriver], T]]

# TODO: Fix typing


class BaseElement[T]:
    def __init__(
        self,
        by: str,
        value: str,
        ec_method: EcMethod[T] = EC.presence_of_element_located,  # type: ignore
        timeout: float = 3,
        use_wait_until: bool = True,
    ) -> None:
        self.by = by
        self.value = value
        self.ec_method = ec_method
        self.timeout = timeout
        self.use_wait_until = use_wait_until

    def __get__(self, obj: BasePage, owner: Any) -> T:
        if self.use_wait_until:
            return obj.wait_until(
                method=self.ec_method,
                method_kwargs={"locator": (self.by, self.value)},
                timeout=self.timeout,
            )  # type: ignore
        else:
            return obj.wait_until_not(
                method=self.ec_method,
                method_kwargs={"locator": (self.by, self.value)},
                timeout=self.timeout,
            )  # type: ignore
