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
        self.system_prompt = f"""
            You are a helpful ai model that should predict the best
            function to answer a user prompt. You should provide the function
            and the parameters but not a solution in json format. Your main job
            is to focus on finding the best fit function for the prompt.
            The expected output format is a json object with name (name of function to use)
            , and parameters (parameters to call the function with).
            Example:
            [
            {
            "prompt": "What is the sum of 2 and 3?",
            "name": "fn_add_numbers",
            "parameters": {"a": 2.0, "b": 3.0}
            },
            {
            "prompt": "Reverse the string 'hello'",
            "name": "fn_reverse_string",
            "parameters": {"s": "hello"}
            }
            Your main goal is to guess the best fit fuction to the prompt while taking
            into consideration the parameter type it expects matches best with the given
            variables in the prompt.
        """

    def generate_response(self, prompt: str) -> str:
        pass

    def generate_json(output_file: str) -> None:
        with open(output_file) as out:
            for prompt in self.prompts:
                pass
