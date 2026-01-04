import json
import logging

from populate_db.scripts.seed_data import seed_data
from populate_db.constants import ALL_DOGS_PAGE_URL_PREFIX
from populate_db.scrape_data import scrape_available_dog_ids
from services.db_client import create_db_client
from typing import Set
from weaviate.classes.query import Filter

logger = logging.getLogger(__name__)

try:
  client = create_db_client()
  dogs = client.collections.use("Dog")
  
  # first get all the current dogs in the db
  with open("populate_db/scripts/current_dog_ids.json", "r") as f:
    data = json.load(f)
    current_dog_ids: Set[int] = set(data["ids"])
    
  # get current dogs from the website
  new_dog_ids = scrape_available_dog_ids(ALL_DOGS_PAGE_URL_PREFIX)
  new_dog_ids_set = set(new_dog_ids)
  
  dogs_to_delete = current_dog_ids - new_dog_ids_set
  dogs_to_insert = new_dog_ids_set - current_dog_ids
  
  # remove old dogs from db
  for dog in dogs_to_delete:
    dogs.data.delete_many(
      where=(Filter.by_property("dog_id").equal(dog))
    )
  
  # insert new dogs into db
  seed_data(list(dogs_to_insert))
  
  # update list and write to file
  with open("populate_db/scripts/current_dog_ids.json", "w") as f:
    dog_ids = {"ids": new_dog_ids}
    json.dump(dog_ids, f, indent=2)
except Exception as err:
  logger.exception(err)
finally:
  client.close()