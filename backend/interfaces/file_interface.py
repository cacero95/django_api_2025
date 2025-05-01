from typing import TypedDict

class FileResponse(TypedDict):
    status: bool
    path: str
    message: str