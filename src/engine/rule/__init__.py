from .sequence import Sequence
from .alternation import Alternation
from .reference import Reference
from .repetition import Repetition
from .exclusion import Exclusion

RuleNode = str | Sequence | Alternation | Reference | Repetition | Exclusion