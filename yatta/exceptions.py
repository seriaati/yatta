__all__ = ("ConnectionTimeoutError", "DataNotFoundError", "YattaAPIError")


class YattaAPIError(Exception):
    def __init__(self, code: int) -> None:
        self.code = code

    def __str__(self) -> str:
        return f"An error occurred while requesting the API, status code: {self.code}"


class DataNotFoundError(YattaAPIError):
    def __init__(self) -> None:
        self.code = 404

    def __str__(self) -> str:
        return "Data not found"


class ConnectionTimeoutError(YattaAPIError):
    def __init__(self) -> None:
        self.code = 522

    def __str__(self) -> str:
        return "Connection to the API timed out"
