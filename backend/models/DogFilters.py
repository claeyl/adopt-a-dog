from dataclasses import dataclass
from backend.models.types import Children, Tribool

@dataclass
class DogFilters:
  friendly_with_cats: Tribool = Tribool.UNKNOWN
  friendly_with_dogs: Tribool = Tribool.UNKNOWN
  single_dog_household: bool = False
  suitable_for_fulltime_workers: Tribool = Tribool.UNKNOWN
  behaviour_training_needed: bool = False
  experienced_dog_owners_needed: bool = False
  can_live_with_children: Children = "any"
  medical_needs: bool = False
  calm_home_needed: bool = False
  
  @classmethod
  def from_weaviate(cls, props: dict) -> "DogFilters":
    field_names = cls.__dataclass_fields__.keys()
    
    kwargs = {}
    for field_name in field_names:
      if field_name in props:
        kwargs[field_name] = props[field_name]
    return cls(**kwargs)