import os
import weaviate
from dotenv import load_dotenv
from weaviate.classes.config import (
  Configure,
  DataType,
  Property,
  Tokenization,
)

try:
  load_dotenv()
  cohere_key = os.getenv("COHERE_API_KEY")
  
  if not cohere_key:
    raise Exception("Cohere key does not exist")
  
  headers = { "X-Cohere-Api-Key": cohere_key }
  client = weaviate.connect_to_local()
  
  dogs = client.collections.create(
  name="Dog",
  description="Collection of dogs available for adoption",
  # vector_config=Configure.Vectors.text2vec_cohere(source_properties=["tags", "description"]),
  # reranker_config=Configure.Reranker.cohere(),
  vector_config=Configure.Vectors.text2vec_transformers(source_properties=["tags", "description"]),
  reranker_config=Configure.Reranker.transformers(),
  properties=[
    Property(
      name="dog_id",
      data_type=DataType.INT,
      skip_vectorization=True,
    ),
    Property(
      name="name",
      data_type=DataType.TEXT,
      skip_vectorization=True,
    ),
    Property(
      name="image_url",
      data_type=DataType.TEXT,
      skip_vectorization=True,
    ),
    Property(
      name="gender",
      data_type=DataType.TEXT,
      skip_vectorization=True,
    ),
    Property(
      name="age",
      data_type=DataType.INT,
      skip_vectorization=True,
    ),
    Property(
      name="breed",
      data_type=DataType.TEXT,
      skip_vectorization=True,
    ),
    Property(
      name="size",
      data_type=DataType.TEXT,
      skip_vectorization=True,
    ),
    Property(
      name="weight",
      data_type=DataType.NUMBER,
      skip_vectorization=True,
    ),
    Property(
      name="adoption_fee",
      data_type=DataType.NUMBER,
      skip_vectorization=True,
    ),
    Property(
      name="tags",
      data_type=DataType.TEXT_ARRAY,
      vectorize_property_name=True,
      tokenization=Tokenization.LOWERCASE,
    ),
    Property(
      name="description",
      data_type=DataType.TEXT,
      vectorize_property_name=True,
      tokenization=Tokenization.WHITESPACE,
    ),
    # dog filters columns
    Property(
      name="friendly_with_cats",
      data_type=DataType.INT,
      skip_vectorization=True,
    ),
    Property(
      name="friendly_with_dogs",
      data_type=DataType.INT,
      skip_vectorization=True,
    ),
    Property(
      name="single_dog_household",
      data_type=DataType.BOOL,
      skip_vectorization=True,
    ),
    Property(
      name="suitable_for_fulltime_workers",
      data_type=DataType.INT,
      skip_vectorization=True,
    ),
    Property(
      name="behaviour_training_needed",
      data_type=DataType.BOOL,
      skip_vectorization=True,
    ),
    Property(
      name="experienced_dog_owners_needed",
      data_type=DataType.BOOL,
      skip_vectorization=True,
    ),
    Property(
      name="can_live_with_children",
      data_type=DataType.TEXT,
      skip_vectorization=True,
    ),
    Property(
      name="medical_needs",
      data_type=DataType.BOOL,
      skip_vectorization=True,
    ),
    Property(
      name="calm_home_needed",
      data_type=DataType.BOOL,
      skip_vectorization=True,
    ),
  ]
)
except Exception as err:
  print(f"Error: {err}")
finally:
  client.close()
