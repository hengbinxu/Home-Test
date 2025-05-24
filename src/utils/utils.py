import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class HelperFuncs:
    @staticmethod
    def url_join(*args: str) -> str:
        slash = "/"
        return "/".join(arg.strip(slash) for arg in args)

    @staticmethod
    def load_json(fp: Path) -> Any:
        with open(fp) as rf:
            data = json.load(rf)
        return data

    @staticmethod
    def get_current_utc() -> datetime:
        return datetime.now(UTC)

    @staticmethod
    def get_current_utc_with_format(format_: str = "%Y-%m-%d %H:%M:%S") -> str:
        return HelperFuncs.get_current_utc().strftime(format_)

    @staticmethod
    def get_current_ts() -> int:
        """
        Get current timestamp
        """
        return int(HelperFuncs.get_current_utc().timestamp())

    @staticmethod
    def parse_number(text: str) -> int:
        text = text.strip().upper()
        unit = text[-1].lower()
        match unit:
            case "k":
                return int(float(text[:-1]) * 1000)
            case "m":
                return int(float(text[:-1]) * 1000_000)
            case "b":
                return int(float(text[:-1]) * 1_000_000_000)
            case _:
                return int(float(text))
