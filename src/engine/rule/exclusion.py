from dataclasses import dataclass
from typing import Any


@dataclass
class Exclusion:
    """Matches base, but only if it doesn't also match anything in excluded."""
    base: Any
    excluded: list[Any]