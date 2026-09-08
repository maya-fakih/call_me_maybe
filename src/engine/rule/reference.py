from dataclasses import dataclass


@dataclass
class Reference:
    """A pointer to another rule by name, resolved at build time."""
    rule_name: str