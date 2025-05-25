from pydantic import RootModel

from src.utils.base_model import BaseModel


class CompanyNews(BaseModel):
    category: str
    datetime: int
    headline: str
    image: str
    related: str
    source: str
    summary: str
    url: str


class GetCompanyNewsResponse(RootModel[list[CompanyNews]]):
    pass
