from engine.rule import Sequence, Alternation, Reference, Repetition, Exclusion

class Parser:
    def __init__(self, text: str):
        self.text_file = text
        self.pos = 0

    def peek(self) -> str | None:
        """Return the current char or none if at eol"""
        pass

    def advance(self) -> None:
        """Advance the position by one character."""
        pass

    def skip_ws(self) -> None:
        """Skip whitespace characters"""
        pass

    def parse_alternation(self):
        """Parse sequence and when next non ws char is '|' parse another"""
        pass

    def parse_sequence(self):
        """Parse objects seperated by ws, stop at " or ] or )..."""
        pass

    def parse_atom(self):
        """parse_primary(), then check if next char is ? * or + and wrap in Repetition"""
        pass

    def parse_primary(self):
        """dispatch on whats next, if its a ( then parse_alternation, if [ then parse_exclusion, if { then parse_repetition, if " then parse_string, else parse_reference"""
        pass
