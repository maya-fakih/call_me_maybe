from abc import ABC, abstractmethod

class RuleGenerator(ABC):
    @abstractmethod
    def generate(self, input_path: str, output_path: str) -> None:
        """Read input_path, write grammar text to output_path."""
