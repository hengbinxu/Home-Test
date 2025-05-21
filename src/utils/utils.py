import json
from pathlib import Path
from typing import Any


class HelperFuncs:
    @staticmethod
    def url_join(*args: str) -> str:
        slash = "/"
        return "/".join((arg.strip(slash) for arg in args))

    @staticmethod
    def load_json(fp: Path) -> Any:
        with open(fp) as rf:
            data = json.load(rf)
        return data
