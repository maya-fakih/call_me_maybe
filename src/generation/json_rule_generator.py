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
                # collect context from input data
                # only check what are the available keys and for each key put all the available options in a set but start from the leafs and work back rules
                # start from the leafs of the dict for all the similar keys at the leaf level collect that like here we have name: all the possible names a rule
                # then work it up as 2nd level we have an answer has name and parameters but dont specify all examples just set rule we might need it
                # then work it up we have the list of functions and we have have a rule for that as well though that is checking format which we will do for the output
                # to learn format not for input where we only want to learn the vocabulary and the rules for them
                # write the rules to the output file

                output_file.write("# Input Rules\n")
                # how to get the depth of a json so we can start from the leafs it has to be generic we need to find the leafs keys
                leaf_keys = self.find_leaf_keys(data)
                for key in leaf_keys:
                    vocab = self.collect_vocab(data, key)
                    rule = f"{key} := {" | ".join(vocab)}"
                    output_file.write(rule + "\n")

        except Exception as e:
            print(f"Error generating input rules: {e}")

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

    def collect_vocab(self, data: dict, key: str) -> set:
        """Collect all unique values for a given key in a nested dict."""
        vocab = set()
        if isinstance(data, dict):
            for value in data.values():
                vocab.update(self.collect_vocab(value, key))
        elif isinstance(data, list):
            for item in data:
                vocab.update(self.collect_vocab(item, key))
        else:
            vocab.add(data)
        return vocab