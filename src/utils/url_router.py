import logging
from typing import Any, override
from urllib import parse

from src.utils.type_alias import Router
from src.utils.utils import HelperFuncs

log = logging.getLogger(__name__)


class UrlRouter:
    ROUTER: Router = {}

    def __init__(self, host: str, port: int | None = None) -> None:
        self.host = host
        self.port = port
        self.base_url = self.get_base_url()

    @property
    def domain(self) -> str:
        return parse.urlparse(self.host).netloc

    @classmethod
    def add_router(cls, new_router: Router) -> None:
        """
        Add new router to the current router.
        """
        for key, value in new_router.items():
            cls.ROUTER[key] = value

    def get_base_url(self) -> str:
        """
        Get host and port from environment, and combine them to base url.
        """
        if self.port:
            url = f"{self.host.rstrip('/')}:{self.port}/"
        else:
            url = self.host
        return url

    def get_api_url(self, api_name: str) -> str:
        try:
            api_endpoint = self.ROUTER[api_name]
        except KeyError:
            log.error(
                "The {api_name} doesn't exist in self.ROUTER.\n"
                f"self.ROUTER: {self.ROUTER}"
            )
        if api_endpoint:
            api_url = HelperFuncs.url_join(self.base_url, api_name)
        else:
            api_url = self.base_url
        return api_url

    def get_formatter_api_url(self, api_name: str, **kwargs: Any) -> str:
        url = self.get_api_url(api_name)
        return url.format(**kwargs)

    @override
    def __repr__(self) -> str:
        return (
            f"< args=(host={self.host}, port={self.port}),"
            f"base_url={self.base_url}, ROUTER={self.ROUTER} >"
        )
