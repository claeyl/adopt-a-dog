import os
import logging
import weaviate

from dotenv import load_dotenv
from weaviate import WeaviateClient

logger = logging.getLogger(__name__)

"""
These functions will be called in a try-catch block, so any errors will be handled in the block
The client will also be closed in the caller function
"""

def create_db_client() -> WeaviateClient:
  client = weaviate.connect_to_local()
  logger.info(f"Connected to weaviate: {client.is_ready()}")
  
  return client


def _create_db_client_cohere() -> WeaviateClient:
  load_dotenv()
  cohere_key = os.getenv("COHERE_API_KEY")
  if not cohere_key:
    raise Exception("Cohere key does not exist")
  
  headers = { "X-Cohere-Api-Key": cohere_key }
  client = weaviate.connect_to_local(headers=headers)
  logger.info(f"Connected to weaviate: {client.is_ready()}")
  
  return client