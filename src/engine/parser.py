from engine.rule import Sequence, Alternation, Reference, Repetition, Exclusion

class Parser:
    def __init__(self, text_file: str):
        try:
            with open(text_file, "r", encoding="utf-8") as f:
                self.text = f.read()
        except OSError as e:
            raise RuntimeError(f"Failed to open grammar file {text_file!r}: {e}")
        self.pos = 0

    def peek(self) -> str | None:
        """Return the current char or none if at eol"""
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]

    def advance(self) -> None:
        """Advance the position by one character."""
        self.pos += 1

    def skip_ws(self) -> None:
        """Skip whitespace characters"""
        while self.peek() is not None and self.peek() in " \t\r":
            self.advance()

    def parse_alternation(self):
        """Parse sequence and when next non ws char is '|' parse another"""
        options = [self.parse_sequence()]
        while True:
            self.skip_ws()
            if self.peek() == "|":
                self.advance()
                self.skip_ws()
                options.append(self.parse_sequence())
            else:
                break
        if len(options) == 1:
            return options[0]
        return Alternation(options)

    def parse_sequence(self):
        """Parse objects seperated by ws, stop at | ) newline or end of text"""
        items = [self.parse_exclusion()]
        while True:
            self.skip_ws()
            c = self.peek()
            if c is None or c in ")|\n":
                break
            items.append(self.parse_exclusion())
        if len(items) == 1:
            return items[0]
        return Sequence(items)

    def parse_atom(self):
        """parse_primary(), then check if next char is ? * or + and wrap in Repetition"""
        pass

    def parse_primary(self):
        """dispatch on whats next, if its a ( then parse_alternation, if [ then parse_exclusion, if { then parse_repetition, if " then parse_string, else parse_reference"""
        pass