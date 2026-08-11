import enum

class JsonStates(enum.Enum):
    BRACKET_OPEN = 1        # [
    BRACES_OPEN = 2         # {
    PROMPT_KEY = 3          # "prompt":
    PROMPT_STRING = 4       # copy the original prompt, no model call
    COMMA = 5
    NAME = 6                 # "name": " -> model picks via masking
    CLOSE_QUOTES = 7          # "
    PARAMETERS = 8           # "parameters": {...} -> call find_parameters()
    CLOSE_PARENTHESIS = 9     # }
    NEXT = 10                 # ,