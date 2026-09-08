import json
from generation.rule_generator import RuleGenerator
from pydantic import TypeAdapter
from generation.input_format import FunctionDefinition


class JSONRuleGenerator(RuleGenerator):
    def generate(self, input_path: str, output_path: str, mode: str) -> None:
        try:
            if mode not in ["input", "output"]:
                raise ValueError(f"Invalid mode: {mode}. Must be 'input' or 'output'.")
            if mode == "input":
                self.generate_input_rules(input_path, output_path)
        except Exception as e:
            raise RuntimeError(f"Failed to generate rules: {e}")

    def generate_input_rules(self, input_path: str, output_path: str) -> None:
        try:
            with open(input_path, "r") as f:
                data = json.load(f)
            functions = TypeAdapter(list[FunctionDefinition]).validate_python(data)
            name_rule = "name := " + " | ".join(f'"\\"{fn.name}\\""' for fn in functions)        
        except Exception as e:
            raise RuntimeError(f"Failed to read input file: {e}")