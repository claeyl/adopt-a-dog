from typing import Literal
from enum import Enum

Gender = Literal["male", "female"]
Size = Literal["small", "medium", "large"]
Children = Literal["any", "older", "teenager", "none"]

ComparisonOperator = Literal["equal", "not_equal", "less_than", "less_or_equal", "greater_than", "greater_or_equal"]
LogicalOperator = Literal["or", "and"]

class Tribool(Enum):
  TRUE = 0
  FALSE = 1
  UNKNOWN = 2
