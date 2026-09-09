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

    def parse_exclusion(self):
        """Parse atom, then while next non-ws char is '-', parse another atom
        to exclude. base - a - b -> Exclusion(base, [a, b])."""
        base = self.parse_atom()
        excluded = []
        while True:
            self.skip_ws()
            if self.peek() == "-":
                self.advance()
                self.skip_ws()
                excluded.append(self.parse_atom())
            else:
                break
        if not excluded:
            return base
        return Exclusion(base, excluded)

    def parse_atom(self):
        """parse_primary(), then check if next char is ? * or + and wrap in Repetition"""
        item = self.parse_primary()
        c = self.peek()
        if c == "?":
            self.advance()
            return Repetition(item, 0, 1)
        if c == "*":
            self.advance()
            return Repetition(item, 0, None)
        if c == "+":
            self.advance()
            return Repetition(item, 1, None)
        return item

    def parse_primary(self):
        """dispatch on what's next: '(' -> parse_alternation, '"' -> string
        literal, bare word -> ANYCHAR marker or Reference"""
        self.skip_ws()
        c = self.peek()
        if c == "(":
            self.advance()
            node = self.parse_alternation()
            self.skip_ws()
            if self.peek() != ")":
                raise SyntaxError(f"Expected ')' at position {self.pos}")
            self.advance()
            return node
        if c == '"':
            return self.parse_string_literal()
        return self.parse_reference()

    def parse_string_literal(self) -> str:
        """Parse a "..." literal, handling \\" \\\\ \\n \\t \\r \\/ \\b \\f escapes."""
        if self.peek() != '"':
            raise SyntaxError(f"Expected '\"' at position {self.pos}")
        self.advance()
        chars = []
        escapes = {'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f",
                   "n": "\n", "r": "\r", "t": "\t"}
        while True:
            c = self.peek()
            if c is None:
                raise SyntaxError("Unterminated string literal")
            if c == '"':
                self.advance()
                break
            if c == "\\":
                self.advance()
                esc = self.peek()
                if esc not in escapes:
                    raise SyntaxError(f"Invalid escape '\\{esc}' at position {self.pos}")
                chars.append(escapes[esc])
                self.advance()
            else:
                chars.append(c)
                self.advance()
        return "".join(chars)

    def parse_reference(self):
        """Parse a bare word: 'ANYCHAR' becomes the literal marker str
        'ANYCHAR', anything else becomes Reference(word)."""
        start = self.pos
        while self.peek() is not None and (self.peek().isalnum() or self.peek() == "_"):
            self.advance()
        if start == self.pos:
            raise SyntaxError(f"Unexpected character {self.peek()!r} at position {self.pos}")
        word = self.text[start:self.pos]
        if word == "ANYCHAR":
            return "ANYCHAR"
        return Reference(word)

    def skip_junk(self) -> None:
        """Skip blank lines and comment lines (starting with '#')."""
        while True:
            while self.peek() in (" ", "\t", "\r", "\n"):
                self.advance()
            if self.peek() == "#":
                while self.peek() is not None and self.peek() != "\n":
                    self.advance()
                continue
            break

    def parse_name(self) -> str:
        """Parse a bare rule name up to whitespace or ':='."""
        start = self.pos
        while self.peek() is not None and (self.peek().isalnum() or self.peek() == "_"):
            self.advance()
        if start == self.pos:
            raise SyntaxError(f"Expected rule name at position {self.pos}")
        return self.text[start:self.pos]

    def parse_grammar(self) -> dict[str, object]:
        """Parse the whole file into {rule_name: RuleNode}, skipping
        comments/blank lines. One Parser instance = one whole grammar file."""
        rules: dict[str, object] = {}
        while True:
            self.skip_junk()
            if self.peek() is None:
                break
            name = self.parse_name()
            self.skip_ws()
            if self.text[self.pos:self.pos + 2] != ":=":
                raise SyntaxError(f"Expected ':=' after {name!r} at position {self.pos}")
            self.pos += 2
            self.skip_ws()
            rules[name] = self.parse_alternation()
        return rules