from dataclasses import dataclass
from backend.models.types import Children, Tribool

@dataclass
class DogTags:
  friendly_with_cats: Tribool
  friendly_with_dogs: Tribool
  single_dog_household: bool
  suitable_for_fulltime_workers: Tribool
  behaviour_training_needed: bool
  experienced_dog_owners_needed: bool
  can_live_with_children: Children
  medical_needs: bool
  calm_home_needed: bool