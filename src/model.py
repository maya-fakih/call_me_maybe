from typing import Any
from llm_sdk import Small_LLM_Model


class Model:
    def __init__(
        self,
        model: Small_LLM_Model,
        functions: list[dict[str, Any]],
        prompts: list[dict[str, Any]],
    ) -> None:
        self.model = model
        self.functions = functions
        self.prompts = prompts

    def generate_json(output_file: str) -> None:
        with open(output_file) as out:
            