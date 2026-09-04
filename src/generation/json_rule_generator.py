import json
from generation.rule_generator import RuleGenerator


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
            with open(input_path, 'r', encoding="utf-8") as f:
                data = json.load(f)
                # assuming data is a list of input formats which is so based on the subject
                
        except Exception as e:
            raise RuntimeError(f"Failed to read input file: {e}")