from dataclasses import dataclass
from typing import List
from backend.models.DogTags import DogTags
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
  metadata: List[str]
  description: str
  tags: DogTags
