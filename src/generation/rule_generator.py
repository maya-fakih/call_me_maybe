from abc import ABC, abstractmethod


class RuleGenerator(ABC):
    @abstractmethod
    def generate(self, input_path: str, output_path: str, mode: str) -> None:
        """Read input_path, write grammar text to output_path.

        mode: "input"  -> leaf values ARE the vocabulary, collect + alternate
              "output" -> leaf values are placeholders, emit type only
        """