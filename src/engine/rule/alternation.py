from dataclasses import dataclass
from typing import Any


@dataclass
class Alternation:
    """A choice between options — the PDA must match exactly one."""
    options: list[Any]