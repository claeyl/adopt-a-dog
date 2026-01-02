import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models.Dog import Dog
from backend.models.dtos.DogInfoResponse import DogInfoResponse
from backend.models.dtos.QueryRequest import QueryRequest
from backend.models.dtos.QueryResponse import QueryResponse
from backend.services.explanation_service import explain_relevance
from backend.services.intent_service.intent_service import query_related_to_adoption
from backend.services.query_service import query_collection

logging.basicConfig(
  level=logging.DEBUG,
  format="%(asctime)s [%(levelname)s]: %(name)s - %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)
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
    query = request.query
    # first check if query is related to adopting a dog
    query_is_related = query_related_to_adoption(query)
    if not query_is_related:
      raise HTTPException(status_code=400, detail="Query is not related to dog adoption.")
    
    logger.debug(f"user query: {query}")
    response = query_collection(query)

    if not response:
      raise HTTPException(status_code=404, detail="No matching dogs found.")
    
    results = []
    for obj in response:
      dog_id = obj.properties.get("dog_id")
      logger.debug(
        f"{obj.properties.get('name')} (ID: {dog_id}) "
        f"has a rerank score of {obj.metadata.rerank_score}"
      )
      
      dog = Dog.from_weaviate(dog_id=dog_id, props=obj.properties)  # type: ignore
      results.append(
        DogInfoResponse(
        id=dog_id,                                                  # type: ignore
        **obj.properties,                                           # type: ignore
        explanation=explain_relevance(dog, query)                   # TODO: optimise this - currently call is sequential
      ))
    return QueryResponse(results=results)
  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error processing query: {str(e)}", exc_info=True)
    raise HTTPException(status_code=500, detail="Something went wrong, please try again")

@app.get("/")
def read_root():
  return {"server": "running"}
