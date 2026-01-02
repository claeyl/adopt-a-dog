from typing import List
from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class DogInfoResponse(BaseModel):
  class Config:
    alias_generator = to_camel
    populate_by_name = True
  
  id: int
  name: str
  image_url: str
  gender: str
  age: float
  breed: str
  size: str
  weight: float
  adoption_fee: float
  tags: List[str]
  description: str
  explanation: str