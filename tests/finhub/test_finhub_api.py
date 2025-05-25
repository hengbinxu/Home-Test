import traceback
from datetime import UTC, datetime
from http import HTTPStatus

import pytest

from src.finnhub.finnhub_api_client import FinnHubApiClient
from src.validate_models.get_company_news import GetCompanyNewsResponse
from src.validate_models.get_company_profile import GetCompanyProfileResponse
from src.validate_models.get_quote import GetQuoteResponse
from src.validate_models.get_symbol_lookup import GetSymbolLookupResponse

TEST_COMPANY_NAME_EXCHANGE = [
    ["apple", "US"],
    ["tsm", "US"],
    ["nvda", "US"],
    ["meta", "US"],
    ["goog", "US"],
]

TEST_COMPANY_SYMBOL = ["AAPL", "TSM", "NVDA", "META", "GOOG"]


class TestFinHubApiClient:
    @pytest.mark.parametrize(
        "company_name,exchange",
        TEST_COMPANY_NAME_EXCHANGE,
        ids=["Apple", "TSMC", "Nvdia", "Meta", "Google"],
    )
    def test_get_symbol_lookup_status_code_and_response(
        self, company_name: str, exchange: str, finhun_api_client: FinnHubApiClient
    ) -> None:
        """
        Test response and status code of the get_symbol_lookup API.

        TestFlow:
            (1). Use the get_symbol_lookup API with different arguments to
            get status code and response
            (2). Check the status code and its response structure
        """
        res = finhun_api_client.get_symbol_lookup(q=company_name, exchange=exchange)
        assert res.status_code == HTTPStatus.OK
        error, err_msg = GetSymbolLookupResponse.validate_model(**res.json())
        assert error is False, err_msg

    @pytest.mark.parametrize(
        "symbol",
        TEST_COMPANY_SYMBOL,
        ids=["Apple", "TSMC", "Nvdia", "Meta", "Google"],
    )
    def test_get_company_profile_status_code_and_response(
        self, symbol: str, finhun_api_client: FinnHubApiClient
    ) -> None:
        """
        Test response and status code of the get_company_profile API.

        TestFlow:
            (1). Use the get_company_profile API with different arguments to
            get status code and response
            (2). Check the status code and its response structure
        """
        res = finhun_api_client.get_company_profile(symbol=symbol)
        assert res.status_code == HTTPStatus.OK
        error, err_msg = GetCompanyProfileResponse.validate_model(**res.json())
        assert error is False, err_msg

    @pytest.mark.parametrize(
        "symbol",
        TEST_COMPANY_SYMBOL,
        ids=["Apple", "TSMC", "Nvdia", "Meta", "Google"],
    )
    def test_get_quote_status_code_and_response(
        self, symbol: str, finhun_api_client: FinnHubApiClient
    ) -> None:
        """
        Test response and status code of the get_quote API.

        TestFlow:
            (1). Use the get_quote API with different arguments to
            get status code and response
            (2). Check the status code and its response structure
        """
        res = finhun_api_client.get_quote(symbol)
        assert res.status_code == HTTPStatus.OK
        error, err_msg = GetQuoteResponse.validate_model(**res.json())
        assert error is False, err_msg

    @pytest.mark.parametrize(
        "symbol,from_date,to_date",
        [
            ("AAPL", "2025-04-01", "2025-04-10"),
            ("TSM", "2025-04-01", "2025-04-10"),
            ("GOOG", "2025-04-01", "2025-04-10"),
        ],
        ids=["Apple", "TSMC", "Nvdia"],
    )
    def test_get_company_news_status_code_and_response(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        finhun_api_client: FinnHubApiClient,
    ) -> None:
        """
        Test response and status code of the get_company_news API.

        TestFlow:
            (1). Use the get_company_news API with different arguments to
            get status code and response
            (2). Check the status code and its response structure
            (3). Check the datetime of the response whether it is between the
            from_date and to_date
        """
        res = finhun_api_client.get_company_news(
            symbol=symbol, from_=from_date, to_=to_date
        )
        assert res.status_code == HTTPStatus.OK
        error = False
        try:
            response_data = GetCompanyNewsResponse(res.json())
        except Exception:
            error = True
            err_msg = traceback.format_exc()
        assert error is False, err_msg

        date_format = "%Y-%m-%d"
        from_ts = (
            datetime.strptime(from_date, date_format).replace(tzinfo=UTC).timestamp()
        )
        end_ts = (
            datetime.strptime(to_date + " 23:59:59", date_format + " %H:%M:%S")
            .replace(tzinfo=UTC)
            .timestamp()
        )
        for data in response_data.root:
            is_in_time_range = end_ts >= data.datetime >= from_ts
            assert is_in_time_range is True, (
                "Get the news out of the given time range, "
                f"symbol: {symbol}, from: {from_date}, to: {to_date}"
            )

    @pytest.mark.parametrize(
        "company_name,exchange",
        TEST_COMPANY_NAME_EXCHANGE,
        ids=["Apple", "TSMC", "Nvdia", "Meta", "Google"],
    )
    def test_getsymbol_api_response_valid_for_company_porfile_api(
        self, company_name: str, exchange: str, finhun_api_client: FinnHubApiClient
    ) -> None:
        """
        Test get_company_profile API by get_symbol_lookup API response.

        TestFlow:
            (1). Use the get_symbol_lookup API with different arguments to get
            the response.
            (2). Use Step1 response as argument for get_company_profile API
            (3). Check the status code and its response structure
        """
        # It's simple API functional test
        response = GetSymbolLookupResponse(
            **finhun_api_client.get_symbol_lookup(
                q=company_name, exchange=exchange
            ).json()
        )
        if response.count > 0:
            description = response.result.pop()
            res = finhun_api_client.get_company_profile(symbol=description.symbol)
            error, err_msg = GetCompanyProfileResponse.validate_model(**res.json())
            assert error is False, err_msg
        else:
            assert ValueError(
                f"Can't get any symbol by company_name: {company_name}, "
                f"exchange: {exchange}"
            )
