from typing import TypedDict

class Response(TypedDict):
    status: bool
    message: str

class ResponseToken(TypedDict, Response):
    token: str
    username: str
    name: str