from dataclasses import dataclass


@dataclass
class HttpRequest:
    url: str
    method: str
    body: dict
    params: dict
