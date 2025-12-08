from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models.dtos.QueryRequest import QueryRequest
from backend.models.dtos.DogResponseInfo import DogResponseInfo
from backend.models.dtos.QueryResponse import QueryResponse
from backend.services.query_service import query_collection

app = FastAPI()

origins = [
  "http://localhost:5173",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.post("/query")
def query_dog_collection(request: QueryRequest) -> QueryResponse:
  try:
    response = query_collection(request.query)

    results = []
    if not response.objects:
      raise HTTPException(status_code=404, detail="No matching dogs found.")
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
    raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
  return {"Hello": "World"}