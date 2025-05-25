import traceback
from typing import Any

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

    @classmethod
    def validate_model(cls, **kwargs: Any) -> tuple[bool, str | None]:
        error = False
        err_msg = None
        try:
            cls(**kwargs)
        except Exception:
            error = True
            err_msg = traceback.format_exc()
        return (error, err_msg)
