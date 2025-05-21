from src.utils.utils import HelperFuncs


class TestHelperFuncs:
    def test_url_join(self) -> None:
        assert (
            HelperFuncs.url_join("http://localhost", "testApi")
            == "http://localhost/testApi"
        )
        assert (
            HelperFuncs.url_join("https://localhost", "/user")
            == "https://localhost/user"
        )
