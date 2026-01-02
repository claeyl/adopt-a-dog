from typing import List, Optional

from bs4 import ResultSet, Tag
from backend.models.DogFilters import DogFilters
from backend.models.Dog import Dog
from backend.models.types import Gender, Size, Tribool
from backend.populate_db.scrape_data import scrape_full_dog_info
from backend.populate_db.format_data import (
  format_id,
  format_gender,
  format_age,
  format_breed,
  format_size,
  format_weight,
  format_fee,
  format_dog_description
)


def get_dog_image_url(image_element: Tag) -> str:

  first_available_image = image_element.find("img")
  if not first_available_image:
    return ""
  return str(first_available_image["src"])


def parse_basic_dog_info(raw_text: str) -> tuple[int, str, Gender, int, str, Size, float, float]:
  name, id, _, gender, age, breed, size_and_weight, _, fee, _, _, _ = raw_text.split("\n")

  id = format_id(id)
  gender = format_gender(gender)
  age = format_age(age)
  breed = format_breed(breed)
  
  size, weight = size_and_weight.split(maxsplit=1)

  size = format_size(size)
  weight = format_weight(weight)
  fee = format_fee(fee)
  
  return id, name, gender, age, breed, size, weight, fee


def parse_dog_tags(tag_images: ResultSet[Tag]) -> List[str]:
  titles = [str(img["title"]).lower() for img in tag_images if img.has_attr("title")]
  return titles


def construct_dog_filters(tags: List[str]) -> DogFilters:
  # default values
  dog_filters = DogFilters()
  
  for metadata in tags:
    match metadata:
      case "no children":
        dog_filters.can_live_with_children = "none"
      case "calm home needed":
        dog_filters.calm_home_needed = True
      case "behavior training needed":
        dog_filters.behaviour_training_needed = True
      case "suitable for full-time workers":
        dog_filters.suitable_for_fulltime_workers = Tribool.TRUE
      case "choosy with dog friends":
        dog_filters.friendly_with_dogs = Tribool.FALSE
      case "medical needs":
        dog_filters.medical_needs = True
      case "no cats":
        dog_filters.friendly_with_cats = Tribool.FALSE
      case "experienced dog owners":
        dog_filters.experienced_dog_owners_needed = True
      case "single dog household":
        dog_filters.single_dog_household = True
      case "older children":
        dog_filters.can_live_with_children = "older"
      case "children":
        dog_filters.can_live_with_children = "any"
      case "dog friendly":
        dog_filters.friendly_with_dogs = Tribool.TRUE
      case "teenagers":
        dog_filters.can_live_with_children = "teenager"
      case "friendly with cats":
        dog_filters.friendly_with_cats = Tribool.TRUE
  
  return dog_filters


def get_full_dog_info(id: int) -> Optional[Dog]:
  response = scrape_full_dog_info(id)
  
  if response is None:
    return None
  
  dog_image_element, dog_content_element, dog_tag_element, dog_description_element = response
  
  # Parse dog image
  if dog_image_element:
    image_url = get_dog_image_url(dog_image_element)
  else:
    image_url = ""
  
  # Parse basic info for a dog
  dog_content_text = dog_content_element.get_text(separator="\n", strip=True)
  id, name, gender, age, breed, size, weight, adoption_fee = parse_basic_dog_info(dog_content_text)
  
  # Parse tags for a dog to obtain tags and filters
  tags = parse_dog_tags(dog_tag_element)
  filters = construct_dog_filters(tags)
  
  # Parse description for a dog
  if not dog_description_element:
    description = ""
  else:
    dog_description_text = [dog_para.get_text(separator=" ", strip=True) for dog_para in dog_description_element]
    description = format_dog_description(dog_description_text)
  
  return \
    Dog(
        id=id,
        name=name,
        image_url=image_url,
        gender=gender,
        age=age,
        breed=breed,
        size=size,
        weight=weight,
        adoption_fee=adoption_fee,
        tags=tags,
        description=description,
        filters=filters
      )