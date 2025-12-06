import os
import weaviate

from dotenv import load_dotenv
from weaviate.classes.query import MetadataQuery, Rerank
from backend.services.filter_service import build_filter_expression, construct_json_filters_from_prompt


RESULT_SIZE = 5

def query_collection(query: str):
  load_dotenv()
  cohere_key = os.getenv("COHERE_API_KEY")
  if not cohere_key:
    raise Exception("Cohere key does not exist")
  
  headers = { "X-Cohere-Api-Key": cohere_key }
  client = weaviate.connect_to_local(headers=headers)
  
  try:
    dogs = client.collections.use("Dog")
    
    json_filters = construct_json_filters_from_prompt(query)
    filters = build_filter_expression(json_filters)
    
    response = dogs.query.near_text(
      query=query,
      filters=(filters),
      rerank=Rerank(
        prop="description",
        query=query
      ),
      limit=RESULT_SIZE,
    )
    return response
  except Exception as err:
    print(err)
    raise err
  finally:
    client.close()