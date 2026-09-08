import pydantic
from generation.input_format import AllowedType, FunctionDefinition

TYPE_CHECKS: dict[AllowedType, type | tuple[type, ...]] = {
    "string": str,
    "boolean": bool,
    "integer": int,
    "number": (int, float),
}


class OutputSchema(pydantic.BaseModel):
    """Shape of one generated answer: real argument values (not type labels)."""
    name: str
    parameters: dict[str, bool | int | float | str]

    def matches(self, fd: FunctionDefinition) -> bool:
        """Does this answer's name + each parameter's actual value type agree with function definition?"""
        if self.name != fd.name or set(self.parameters) != set(fd.parameters):
            return False
        return all(
            isinstance(value, TYPE_CHECKS[fd.parameters[key]["type"]])
            for key, value in self.parameters.items()
        )