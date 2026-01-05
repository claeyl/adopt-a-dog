import os
import logging
import weaviate

from dotenv import load_dotenv
from weaviate import WeaviateClient
from weaviate.classes.init import Auth

logger = logging.getLogger(__name__)

"""
These functions will be called in a try-catch block, so any errors will be handled in the block
The client will also be closed in the caller function
"""

def create_db_client() -> WeaviateClient:
  load_dotenv()
  
  connect_to_local = os.getenv("RUN_LOCAL", "true")
  model = os.getenv("MODEL", "t2v")
  
  if connect_to_local == "true":
    if model == "t2v":
      return _create_db_client_local_t2v()
    else:
      return _create_db_client_local_cohere()
  
  cohere_key = os.getenv("COHERE_API_KEY")
  weaviate_url = os.environ["WEAVIATE_CLUSTER_URL"]
  weaviate_key = os.environ["WEAVIATE_API_KEY"]
  
  if not cohere_key:
    raise Exception("Cohere key does not exist")
  
  if not weaviate_url:
    raise Exception("Weaviate cloud endpoint does not exist")
  
  if not weaviate_key:
    raise Exception("Weaviate key does not exist")
  
  client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_key),
    headers={
      "X-Cohere-Api-Key": cohere_key
    }
  )
  logger.info(f"Connected to weaviate: {client.is_ready()}")
  client = _create_db_client_local_t2v()
  
  return client

# If using local weaviate instance with Cohere
def _create_db_client_local_cohere() -> WeaviateClient:
  load_dotenv()
  cohere_key = os.getenv("COHERE_API_KEY")
  if not cohere_key:
    raise Exception("Cohere key does not exist")
  
  headers = { "X-Cohere-Api-Key": cohere_key }
  client = weaviate.connect_to_local(headers=headers, host="weaviate")
  logger.info(f"Connected to weaviate: {client.is_ready()}")
  
  return client

# If using local weaviate instance with t2v
def _create_db_client_local_t2v() -> WeaviateClient:
  client = weaviate.connect_to_local(host="weaviate")
  logger.info(f"Connected to weaviate: {client.is_ready()}")
  
  return client
