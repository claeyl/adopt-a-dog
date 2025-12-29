from dataclasses import dataclass
from typing import List


@dataclass
class DogResponseInfo:
  id: int
  name: str
  gender: str
  age: float
  breed: str
  size: str
  weight: float
  adoption_fee: float
  tags: List[str]
  description: str
  generated_explanation: str