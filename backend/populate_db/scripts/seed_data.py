import os
import weaviate

from dotenv import load_dotenv
from backend.populate_db.constants import ALL_DOGS_PAGE_URL_PREFIX
from backend.populate_db.extract_data import get_full_dog_info
from backend.populate_db.scrape_data import scrape_available_dog_ids

BATCH_SIZE = 200
ERROR_SIZE = 10

try:
  load_dotenv()
  cohere_key = os.getenv("COHERE_API_KEY")
  if not cohere_key:
    raise Exception("Cohere key does not exist")
  
  headers = { "X-Cohere-Api-Key": cohere_key }
  client = weaviate.connect_to_local(headers=headers)
  dogs = client.collections.use("Dog")

  with dogs.batch.fixed_size(batch_size=BATCH_SIZE) as batch:
    available_dogs = scrape_available_dog_ids(ALL_DOGS_PAGE_URL_PREFIX)
    for available_dog_id in available_dogs:
      dog = get_full_dog_info(available_dog_id)
      
      if dog is not None:
        dog_obj = {
          "dog_id": dog.id,
          "name": dog.name,
          "gender": dog.gender,
          "age": dog.age,
          "breed": dog.breed,
          "size": dog.size,
          "weight": dog.weight,
          "adoption_fee": dog.adoption_fee,
          "tags": dog.tags,
          "description": dog.description,
          "friendly_with_cats": dog.filters.friendly_with_cats.value,
          "friendly_with_dogs": dog.filters.friendly_with_dogs.value,
          "single_dog_household": dog.filters.single_dog_household,
          "suitable_for_fulltime_workers": dog.filters.suitable_for_fulltime_workers.value,
          "behaviour_training_needed": dog.filters.behaviour_training_needed,
          "experienced_dog_owners_needed": dog.filters.experienced_dog_owners_needed,
          "can_live_with_children": dog.filters.can_live_with_children,
          "medical_needs": dog.filters.medical_needs,
          "calm_home_needed": dog.filters.calm_home_needed
        }
        batch.add_object(properties=dog_obj)
        
      if batch.number_errors > ERROR_SIZE:
        raise Exception("Batch import stopped due to excessive errors.")

  # Check for failed objects
  if len(dogs.batch.failed_objects) > 0:
    raise Exception(f"Failed to import {len(dogs.batch.failed_objects)} objects")

except Exception as err:
  print(f"Error: {err}")
finally:
  client.close()
