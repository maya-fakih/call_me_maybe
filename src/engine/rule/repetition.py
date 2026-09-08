from dataclasses import dataclass
from typing import Any


@dataclass
class Repetition:
    """item repeated between min_count and max_count times (max_count=None = unbounded)."""
    item: Any
    min_count: int
    max_count: int | None = None