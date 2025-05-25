from httpx import Response

from src.config import settings
from src.utils.base_api_client import BaseApiClient
from src.utils.url_router import UrlRouter


class FinnHubRouter(UrlRouter):
    ROUTER = {
        "symbol_lookup": "/api/v1/search",
        "company_profile": "/api/v1/stock/profile2",
        "company_news": "/api/v1/company-news",
        "quote": "/api/v1/quote",
    }

    def __init__(self) -> None:
        super().__init__(host=settings.FINN_HUB_HOST)


class FinnHubApiClient(BaseApiClient):
    def __init__(self) -> None:
        super().__init__(url_router=FinnHubRouter())
        self.auth_headers = {
            "Content-Type": "application/json",
            "X-Finnhub-Token": settings.FINN_HUB_API_KEY,
        }

    def get_symbol_lookup(self, q: str, exchange: str = "US") -> Response:
        api_url = self.get_api_url("symbol_lookup")
        query_parameters = {"q": q, "exchange": exchange}
        return self.client.get(
            api_url, params=query_parameters, headers=self.auth_headers
        )

    def get_company_profile(
        self,
        symbol: str | None = None,
        isin: str | None = None,
        cusip: str | None = None,
    ) -> Response:
        api_url = self.get_api_url("company_profile")
        query_parameters = {}
        if cusip:
            query_parameters = {"cusip": cusip}
        if isin:
            query_parameters = {"isin": isin}
        if symbol:
            query_parameters = {"symbol": symbol}
        return self.client.get(
            api_url, params=query_parameters, headers=self.auth_headers
        )

    def get_quote(self, symbol: str) -> Response:
        api_url = self.get_api_url("quote")
        query_parameters = {"symbol": symbol}
        return self.client.get(
            api_url, params=query_parameters, headers=self.auth_headers
        )

    def get_company_news(self, symbol: str, from_: str, to_: str) -> Response:
        """
        List latest company news by symbol.
        This endpoint is only available for North American companies.

        Args:
            symbol (str): Company symbol.
            from_ (str): From date YYYY-MM-DD.
            to_ (str): To date YYYY-MM-DD.
        """
        api_url = self.get_api_url("company_news")
        query_parameters = {"symbol": symbol, "from": from_, "to": to_}
        return self.client.get(
            api_url, params=query_parameters, headers=self.auth_headers
        )
