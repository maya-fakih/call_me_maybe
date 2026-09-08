from dataclasses import dataclass
from typing import Any


@dataclass
class Sequence:
    """Things that must appear one after another, in order."""
    items: list[Any]