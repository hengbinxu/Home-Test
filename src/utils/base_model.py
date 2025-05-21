from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict


class BaseModel(_BaseModel):
    """
    It's the base model for implementing common methods
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
    )
