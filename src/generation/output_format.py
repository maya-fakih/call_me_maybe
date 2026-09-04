import pydantic
from generation.input_format import AllowedType, FunctionDefinition


class OutputSchema(pydantic.BaseModel):
    name: str
    parameters: dict[str, AllowedType]

    @classmethod
    def from_definition(cls, fd: FunctionDefinition) -> "OutputSchema":
        return cls(
            name=fd.name,
            parameters={k: v["type"] for k, v in fd.parameters.items()},
        )