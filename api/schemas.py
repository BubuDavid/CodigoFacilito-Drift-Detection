from pydantic import BaseModel


class InputBody(BaseModel):
    x1: float
    x2: float
    tag: str = "base"
