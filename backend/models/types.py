from typing import Literal
from enum import Enum

Gender = Literal["male", "female"]
Size = Literal["small", "medium", "large"]
Children = Literal["any", "older", "teenager", "none"]

class Tribool(Enum):
  TRUE = 0
  FALSE = 1
  UNKNOWN = 2
