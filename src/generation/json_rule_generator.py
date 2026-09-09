import json
from generation.rule_generator import RuleGenerator
from pydantic import TypeAdapter
from generation.input_format import FunctionDefinition


class JSONRuleGenerator(RuleGenerator):
    TYPE_TO_RULE = {
        "string": "string",
        "integer": "integer",
        "number": "(integer | float)",
        "boolean": "boolean",
    }

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
            with open(input_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            functions = TypeAdapter(list[FunctionDefinition]).validate_python(data)

            call_rule_names = []
            lines = ["# Input Rules", self._primitive_rules()]
            for fn in functions:
                lines.append(self._build_params_rule(fn))
                lines.append(self._build_call_rule(fn))
                call_rule_names.append(f"call_{fn.name}")

            lines.append("call := " + " | ".join(call_rule_names))

            with open(output_path, "a", encoding="utf-8") as out:
                out.write("\n".join(lines) + "\n")
        except Exception as e:
            raise RuntimeError(f"Failed to generate input rules: {e}")

    def _primitive_rules(self) -> str:
        """Leaf-level rules referenced by TYPE_TO_RULE (integer/float/boolean/string)
        and their own dependencies (WS, digit, escape, char). Emitted once per run,
        before any per-function rules, so every Reference to them resolves."""
        return "\n".join([
            'WS      := (" " | "\\t" | "\\n" | "\\r")*',
            'digit   := "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"',
            'integer := "-"? ("0" | ((digit - "0") digit*))',
            'float   := "-"? ("0" | ((digit - "0") digit*)) "." digit+',
            'boolean := "true" | "false"',
            'escape  := "\\\\" ("\\"" | "\\\\" | "/" | "b" | "f" | "n" | "r" | "t")',
            'char    := escape | (ANYCHAR - "\\"" - "\\\\")',
            'string  := "\\"" char* "\\""',
        ])

    def _build_params_rule(self, fn: FunctionDefinition) -> str:
        members = []
        for param_name, param_spec in fn.parameters.items():
            param_type = param_spec["type"]
            if param_type not in self.TYPE_TO_RULE:
                raise ValueError(f"Unknown parameter type {param_type!r} for {param_name!r}")
            type_rule = self.TYPE_TO_RULE[param_type]
            members.append(f'"\\"{param_name}\\"" WS ":" WS {type_rule}')
        body = ' WS "," WS '.join(members)
        return f'params_{fn.name} := "{{" WS {body} WS "}}"'

    def _build_call_rule(self, fn: FunctionDefinition) -> str:
        return (
            f'call_{fn.name} := "\\"name\\"" WS ":" WS "\\"{fn.name}\\"" '
            f'WS "," WS "\\"parameters\\"" WS ":" WS params_{fn.name}'
        )