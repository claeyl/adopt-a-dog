from backend.models.dtos.DogInfoResponse import DogInfoResponse
from typing import List
from pydantic import BaseModel


class QueryResponse(BaseModel):
  results: List[DogInfoResponse]