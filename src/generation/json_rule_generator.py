import json
from generation.rule_generator import RuleGenerator


class JSONRuleGenerator(RuleGenerator):
    def generate(self, input_path: str, output_path: str, mode: str) -> None:
        try:
            with open(input_path, 'r') as input_file:
                data = json.load(input_file)

                if mode == "input":
                    self._generate_input_rules(data, output_path)
                elif mode == "output":
                    self._generate_output_rules(data, output_path)
                else:
                    raise ValueError(f"Invalid mode: ({mode}). Expected 'input' or 'output'.")
        except Exception as e:
            print(f"Error generating rules: ({e})")

    def _generate_input_rules(self, data: list[dict], output_path: str) -> None:
        """
        data looks like functions_definition.json: a list of
        {"name": ..., "parameters": {param_name: {"type": ...}, ...}, ...}

        Leaf values here ARE the vocabulary -> collect + alternate them.

        TODO (you write this):
        - collect every function's "name" value -> build the `name := ...` rule
        - for each function, build its own params_<fnname> rule from its
          parameters' types (use a type_to_rule lookup dict)
        - build the `parameters := ...` rule as alternation of all params_<fnname>
        - return the full rules text (all lines joined with "\n")
        """
        try:
            with open(output_path, "a") as output_file:
                output_file.write("# Input Rules\n")
                # how to get the depth of a json so we can start from the leafs it has to be generic we need to find the leafs keys
                leaf_keys = self.find_leaf_keys(data)
                for key in leaf_keys:
                    vocab = self.collect_vocab(data, key)
                    rule = f"{key} := {" | ".join(vocab)}"
                    output_file.write(rule + "\n")

        except Exception as e:
            print(f"Error generating input rules: {e}")

    def _generate_output_rules(self, data: list[dict], output_path: str) -> None:
        """
        data looks like output_shape.json: a list with one (or more) example
        answer objects. Leaf values here are placeholders -> we only care
        about their type, never their actual value.

        Builds rules bottom-up: recurse to the leaves first, they resolve
        to a type name immediately (string/float/integer/boolean). Every
        nested dict resolves only after its own children are done, then
        registers its own rule and hands its name back up to its parent.
        """
        try:
            example = data[0]
            rules: dict[str, str] = {}
            self._infer_shape(example, "answer", rules)

            with open(output_path, "a") as output_file:
                output_file.write("# Output Rules\n")
                for name, body in rules.items():
                    output_file.write(f"{name} := {body}\n")

        except Exception as e:
            print(f"Error generating output rules: {e}")

    def _infer_shape(self, value, name: str, rules: dict) -> str:
        """Recursively resolve value's shape, deepest first.

        Returns the rule name to reference `value` by. Dicts register
        their own rule in `rules` as a side effect before returning
        their name; leaves just return a type name directly.
        """
        if isinstance(value, dict):
            parts = []
            for key, sub_value in value.items():
                sub_ref = self._infer_shape(sub_value, f"{name}_{key}", rules)
                parts.append(f'"\\"{key}\\"" WS ":" WS {sub_ref}')
            body = ' WS "," WS '.join(parts)
            rules[name] = f'"{{" WS {body} WS "}}"'
            return name

        if isinstance(value, bool):
            return "boolean"
        if isinstance(value, str):
            return "string"
        if isinstance(value, float):
            return "float"
        if isinstance(value, int):
            return "integer"

        raise ValueError(f"Unsupported leaf type: {value!r}")

    def find_leaf_keys(self, data: dict, parent_key: str = '') -> set:
        """Recursively find all leaf_keys in a nested dict."""
        leaf_keys = set()
        if isinstance(data, dict):
            for key, value in data.items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                if isinstance(value, dict):
                    leaf_keys.update(self.find_leaf_keys(value, full_key))
                else:
                    leaf_keys.add(full_key)
        elif isinstance(data, list):
            for item in data:
                leaf_keys.update(self.find_leaf_keys(item, parent_key))
        return leaf_keys

    def collect_vocab(self, data, key: str) -> set:
        vocab = set()
        if isinstance(data, dict):
            for k, value in data.items():
                if k == key:
                    vocab.add(value)
                else:
                    vocab.update(self.collect_vocab(value, key))
        elif isinstance(data, list):
            for item in data:
                vocab.update(self.collect_vocab(item, key))
        return vocab