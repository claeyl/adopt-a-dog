from dataclasses import dataclass
from typing import List
from models.DogFilters import DogFilters
from models.types import Gender, Size

@dataclass
class Dog:
  id: int
  name: str
  image_url: str
  gender: Gender
  age: float
  breed: str
  size: Size
  weight: float
  adoption_fee: float
  tags: List[str]
  description: str
  filters: DogFilters
  
  @classmethod
  def from_weaviate(cls, dog_id: int, props: dict) -> "Dog":
    filters = DogFilters.from_weaviate(props)
    
    field_names = [f for f in cls.__dataclass_fields__.keys() if f != "filters"]
    dog_kwargs = {k: props[k] for k in field_names if k in props}

    dog_kwargs["id"] = dog_id
    dog_kwargs["filters"] = filters
    return cls(**dog_kwargs)


  def __str__(self) -> str:
    return f"{self.name} is a {self.gender} {self.breed}, {self.age} years old, {self.size} size. It has these tags: {self.tags}. {self.description}"