from typing import List, Literal, Optional
from pydantic import BaseModel
from backend.models.types import ComparisonOperator


class FilterCondition(BaseModel):
  comparison_operator: ComparisonOperator
  value: str | int | float | bool

class SimpleFilter(BaseModel):
  field: str
  logical_operator: Optional[Literal["or", "and"]]
  filters: List[FilterCondition]

class FilterExpression(BaseModel):
  filter_expression: List[SimpleFilter]

class FilterConstructionError(Exception):
  pass