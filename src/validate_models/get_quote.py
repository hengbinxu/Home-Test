from pydantic import Field

from src.utils.base_model import BaseModel


class GetQuoteResponse(BaseModel):
    c: float = Field(description="Current price")
    h: float = Field(description="High price of the day")
    l: float = Field(description="Low price of the day")  # noqa: E741
    o: float = Field(description="Open price of the day")
    pc: float = Field(description="Previous close price")
    t: int = Field(description="Timestamp")
