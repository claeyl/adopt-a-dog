from typing import List
from pydantic import BaseModel
from backend.models.dtos.DogResponseInfo import DogResponseInfo


class QueryResponse(BaseModel):
  results: List[DogResponseInfo]