import logging
from http import HTTPMethod
from typing import Any, override

from httpx import Client, Request, Response
from httpx._client import USE_CLIENT_DEFAULT, UseClientDefault
from httpx._types import (
    AuthTypes,
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestExtensions,
    RequestFiles,
    TimeoutTypes,
)

from src.utils.url_router import UrlRouter


class BaseApiClient:
    log = logging.getLogger()

    def __init__(self, url_router: UrlRouter) -> None:
        self.url_router = url_router
        self.client = Client(
            event_hooks={
                "request": [self._log_request],
                # "response": [self._raise_error],
            }
        )

    def _log_request(self, request: Request) -> None:
        self.log.debug(
            f"Send Url: {request.url} with method: {request.method}, "
            f"headers: {request.headers}, data: {request.content}"
        )

    def _raise_error(self, response: Response) -> None:
        response.raise_for_status()

    def get_api_url(self, api_name: str) -> str:
        return self.url_router.get_api_url(api_name)

    def get_formatter_api_url(self, api_name: str, **kwargs: Any) -> str:
        return self.url_router.get_formatter_api_url(api_name, **kwargs)

    def request_json(
        self,
        method: HTTPMethod,
        url: str,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = 300,
        extensions: RequestExtensions | None = None,
    ) -> Any:
        res = self.client.request(
            method=method,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
        )
        return res.json()

    @override
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}, url_router: {self.url_router}>"
