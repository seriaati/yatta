from __future__ import annotations

__all__ = ("ConnectionTimeoutError", "DataNotFoundError", "YattaAPIError")


class YattaAPIError(Exception):
    """Raise for yatta-py API errors."""

    def __init__(self, code: int) -> None:
        self.code = code
        super().__init__(f"An error occurred while requesting the API, status code: {self.code}")


class DataNotFoundError(YattaAPIError):
    """Raise when requested data is not found (HTTP 404)."""

    def __init__(self) -> None:
        super().__init__(404)

    def __str__(self) -> str:
        return "Data not found"


class ConnectionTimeoutError(YattaAPIError):
    """Raise when the connection to the API times out (HTTP 522)."""

    def __init__(self) -> None:
        super().__init__(522)

    def __str__(self) -> str:
        return "Connection to the API timed out"
