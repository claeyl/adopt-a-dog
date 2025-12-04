import requests

from typing import List, Optional, Tuple
from bs4 import BeautifulSoup, ResultSet, Tag
from backend.models.Dog import Dog
from backend.populate_db.constants import INDIVIDUAL_DOG_PAGE_URL_PREFIX


def scrape_available_dog_ids(url: str) -> List[int]:
  """
  Get all dog IDs that are available for adoption from the main webpage
  Each dog will have their own webpage in the form of `https://www.dogshome.org.au/our-dogs/{id}/`
  """
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")
  
  available_dogs = soup.find("div", class_="dogsListingWrap container")
  
  dog_ids = []
  if available_dogs is not None:
    for dog_card in available_dogs.find_all(recursive=False):
      if dog_details := dog_card.select_one(".item_description"):
        
        if dog_status_badge := dog_details.select_one("span"):
          if "Adopted" in dog_status_badge.get_text():
            continue

        if dog_page_link := dog_details.select_one("a"):
          dog_id = str(dog_page_link["href"]).rstrip("/").split("/")[-1]
          if dog_id.isdigit():
            dog_ids.append(int(dog_id))

  return dog_ids


def scrape_full_dog_info(id: int) -> Optional[Tuple[Tag, ResultSet[Tag], ResultSet[Tag]]]:
  response = requests.get(f"{INDIVIDUAL_DOG_PAGE_URL_PREFIX}/{id}")
  soup = BeautifulSoup(response.content, "html.parser")
  
  dog_info = soup.find("div", class_="slingleDogWrapper")
  if not dog_info:
    return None
  
  """
  In the page, a dog's info is divided up into 3 parts that are relevant:
  A 'content' section that has basic information such as a dog's name, age, weight, size, etc.
  A 'tags' section that has tags about a dog's character, 
    such as their friendliness towards other dogs, whether they have medical needs, if they can live with children etc.
  A 'description' section that has a more in depth paragraph(s) explanation of a dog
  """
  dog_content_element = dog_info.select_one(".contWrap .dogDetailsWrap")
  dog_tags_element = dog_info.select(".contWrap .dogDetailsWrap .dogDetail.fullDetails.dogicons img")
  dog_description_element = dog_info.select(".contWrap .dogContent p")
  
  if not dog_content_element:
    return None
  
  return dog_content_element, dog_tags_element, dog_description_element
