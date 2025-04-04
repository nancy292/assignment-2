from pydantic import BaseModel
from typing import Optional

class Query(BaseModel):
    attribute: str
    operator: str
    value: str

class Users(BaseModel):
    name: str
    email: str
    boardsOwned: list[str]
    boardsJoined: list[str]
