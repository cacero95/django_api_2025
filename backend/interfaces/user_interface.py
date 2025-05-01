from typing import TypedDict

class Token_payload(TypedDict):
    id: str
    ISS: str
    iat: str
    exp: str

class Defined_token(TypedDict):
    token: str
    url: str