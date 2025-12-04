from dataclasses import dataclass
from typing import List
from backend.models.DogFilters import DogFilters
from backend.models.types import Gender, Size

@dataclass
class Dog:
  id: int
  name: str
  gender: Gender
  age: float
  breed: str
  size: Size
  weight: float
  adoption_fee: float
  tags: List[str]
  description: str
  filters: DogFilters
