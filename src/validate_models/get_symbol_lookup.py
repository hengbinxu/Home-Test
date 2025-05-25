from pydantic import Field

from src.utils.base_model import BaseModel


class Description(BaseModel):
    description: str
    display_symbol: str = Field(alias="displaySymbol")
    symbol: str
    type: str


class GetSymbolLookupResponse(BaseModel):
    count: int
    result: list[Description]
