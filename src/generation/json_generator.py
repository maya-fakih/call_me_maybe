from rule_generator import RuleGenerator

class JSONRuleGenerator(RuleGenerator):
    def generate(self, input_path: str, output_path: str) -> None:
        """
        1. load json
        2. decide: is this a functions_definition-shaped file
           or an output_shape-shaped file?
        3. call the matching helper
        4. write result to output_path
        """