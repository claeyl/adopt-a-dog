import asyncio
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.Dog import Dog
from models.dtos.DogInfoResponse import DogInfoResponse
from models.dtos.QueryRequest import QueryRequest
from models.dtos.QueryResponse import QueryResponse
from services.explanation_service import explain_relevance
from services.intent_service.intent_service import query_related_to_adoption
from services.query_service import query_collection

logging.basicConfig(
  level=logging.DEBUG,
  format="%(asctime)s [%(levelname)s]: %(name)s - %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)
load_dotenv()
app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=os.getenv("FRONTEND_API_URL", "http://localhost:8000"),
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.post("/query")
async def query_dog_collection(request: QueryRequest) -> QueryResponse:
  try:
    query = request.query
    # first check if query is related to adopting a dog
    # TODO: figure out how to host binary clasifier because Git does not allow large files
    environment = os.getenv("ENVIRONMENT", "local")
    if environment == "local":
      query_is_related = query_related_to_adoption(query)
      if not query_is_related:
        raise HTTPException(status_code=400, detail="Query is not related to dog adoption.")
    
    logger.debug(f"user query: {query}")
    response = query_collection(query)

    if not response:
      raise HTTPException(status_code=404, detail="No matching dogs found.")
    
    results = []
    promises = [_get_dog_info_response(obj, query) for obj in response]
    results = await asyncio.gather(*promises)
    return QueryResponse(results=results)
  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error processing query: {str(e)}", exc_info=True)
    raise HTTPException(status_code=500, detail="Something went wrong, please try again")


async def _get_dog_info_response(obj, query: str) -> DogInfoResponse:
  dog_id = obj.properties.get("dog_id")
  logger.debug(
    f"{obj.properties.get('name')} (ID: {dog_id}) "
    f"has a rerank score of {obj.metadata.rerank_score}"
  )
  
  dog = Dog.from_weaviate(dog_id=dog_id, props=obj.properties)  # type: ignore
  return DogInfoResponse(
    id=dog_id,                                                  # type: ignore
    **obj.properties,                                           # type: ignore
    explanation=await explain_relevance(dog, query)             # TODO: optimise this - currently call is sequential
  )


@app.get("/")
def read_root():
  return {"server": "running"}
