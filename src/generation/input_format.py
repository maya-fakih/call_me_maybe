import pydantic
from typing import Literal

AllowedType = Literal["string", "number", "boolean", "integer"]

class InputFormat(pydantic.BaseModel):
    name: str
    description: str
    parameters: dict[str, dict[str, AllowedType]]
    returns: dict[str, AllowedType]
    