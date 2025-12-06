from fastapi import FastAPI
from backend.models.dtos.ErrorResponse import ErrorResponse
from backend.models.dtos.QueryRequest import QueryRequest
from backend.models.dtos.DogResponseInfo import DogResponseInfo
from backend.models.dtos.QueryResponse import QueryResponse
from backend.services.query_service import query_collection

app = FastAPI()

@app.post("/query")
def query_dog_collection(request: QueryRequest) -> QueryResponse | ErrorResponse:
  try:
    response = query_collection(request.query)

    results = []
    for obj in response.objects:
      results.append(
        DogResponseInfo(
        id=obj.properties.get("dog_id"),   # type: ignore
        name=obj.properties.get("name"),   # type: ignore
        gender=obj.properties.get("gender"),   # type: ignore
        age=obj.properties.get("age"),   # type: ignore
        breed=obj.properties.get("breed"),   # type: ignore
        size=obj.properties.get("size"),   # type: ignore
        weight=obj.properties.get("weight"),   # type: ignore
        adoption_fee=obj.properties.get("adoption_fee"),   # type: ignore
        tags=obj.properties.get("tags"),   # type: ignore
        description=obj.properties.get("description"),   # type: ignore
      ))
    return QueryResponse(results=results)
  except Exception as e:
    return ErrorResponse(error=str(e))

@app.get("/")
def read_root():
  return {"Hello": "World"}