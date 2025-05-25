from pydantic import Field

from src.utils.base_model import BaseModel


class GetCompanyProfileResponse(BaseModel):
    country: str
    currency: str
    exchange: str
    ipo: str
    market_capitalization: float = Field(alias="marketCapitalization")
    name: str
    phone: str
    share_outstanding: float = Field(alias="shareOutstanding")
    ticker: str
    weburl: str
    logo: str
    finnhub_industry: str = Field(alias="finnhubIndustry")
