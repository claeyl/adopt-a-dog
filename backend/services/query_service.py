import logging

from backend.services.db_client import create_db_client
from weaviate.classes.query import Rerank, MetadataQuery
from backend.services.filter_service import build_filter_expression, construct_json_filters_from_prompt

logger = logging.getLogger(__name__)

OVERFETCH_LIMIT = 20
RESULT_SIZE = 5

# This returns a list of Weaviate's QueryReturn type, but it is not exposed for public use, so type can't be annotated
def query_collection(query: str, top_k: int = RESULT_SIZE):
  client = create_db_client()
  
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