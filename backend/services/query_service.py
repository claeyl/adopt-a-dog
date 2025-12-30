import os
import logging
import weaviate

from dotenv import load_dotenv
from weaviate.classes.query import Rerank, MetadataQuery
from backend.services.filter_service import build_filter_expression, construct_json_filters_from_prompt

logger = logging.getLogger(__name__)

OVERFETCH_LIMIT = 20
RESULT_SIZE = 5

# This returns a list of Weaviate's QueryReturn type, but it is not exposed for public use, so type can't be annotated
def query_collection(query: str, top_k: int = RESULT_SIZE):
  load_dotenv()
  cohere_key = os.getenv("COHERE_API_KEY")
  if not cohere_key:
    raise Exception("Cohere key does not exist")
  
  headers = { "X-Cohere-Api-Key": cohere_key }
  client = weaviate.connect_to_local(headers=headers) # TODO: eventually change this to connect_to_weaviate_cloud
  
  try:
    dogs = client.collections.use("Dog")
    
    json_filters = construct_json_filters_from_prompt(query)
    filters = build_filter_expression(json_filters)
    
    response = dogs.query.near_text(
      query=query,
      filters=(filters),
      limit=OVERFETCH_LIMIT,
      rerank=Rerank(
        prop="description",
        query=query
      ),
      return_metadata=MetadataQuery(explain_score=True)
    )

    if not response.objects:
      return None
    return response.objects[:RESULT_SIZE]
  except Exception as err:
    print(err)
    raise err
  finally:
    client.close()