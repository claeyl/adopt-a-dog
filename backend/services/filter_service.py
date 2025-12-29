import json
import logging
import os

from backend.models.FilterExpression import FilterCondition, FilterExpression, FilterConstructionError
from backend.models.types import LogicalOperator
from dotenv import load_dotenv
from huggingface_hub import InferenceClient, InferenceEndpointError, InferenceTimeoutError
from pydantic import ValidationError
from typing import List
from weaviate.classes.query import Filter

logger = logging.getLogger(__name__)

def construct_json_filters_from_prompt(query: str) -> FilterExpression:
  load_dotenv()
  hugging_face_key = os.getenv("HUGGING_FACE_API_KEY")
  if not hugging_face_key:
    logger.error("Couldn't find hugging face api key")
    raise ValueError("Couldn't find hugging face api key")
  
  prompt = """
  You are given a natural-language query about a user's needs and wants when adopting a dog.
  Your task is to extract only the properties explicitly mentioned or clearly implied in the query

  ## Valid Fields:
  - gender: "female" | "male"
  - age: integer (years)
  - size: "small" | "medium" | "large"
  - weight: float (kg)
  - adoption_fee: float
  - friendly_with_cats: 0 | 1 | 2
  - friendly_with_dogs: 0 | 1 | 2
  - single_dog_household: boolean
  - suitable_for_fulltime_workers: 0 | 1 | 2
  - behaviour_training_needed: boolean
  - experienced_dog_owners_needed: boolean
  - can_live_with_children: "none" | "any" | "older" | "teenager"
  - medical_needs: boolean
    - For this field, it refers to ongoing medical care requirements (e.g., "needs daily medication", "requires special diet", "needs regular vet visits").
    - This excludes disabilities like deafness, blindness, a dog having three legs, etc.
  - calm_home_needed: boolean

  ## Logical Operator Rules
  For numeric range fields: age, weight, adoption_fee
    - Use "and" when combining multiple conditions in a continuous range (e.g., "between 1 and 5 years old")
    - Use "or" when conditions are disjoint (e.g., "less than 5 kg or greater than 8 kg")
  For all other fields
    - If multiple filters are possible for a field (e.g., "small or medium"), use "or".
  logical_operator should be null if there is only one filter in the group.
    
  ## Comparison Operator Rules
  - "equal"
  - "not_equal"
  - "less_than"
  - "less_or_equal"
  - "greater_than"
  - "greater_or_equal"
    
  ## Special Field Rules

  ### Tri-state Properties
  For the following fields:
  - friendly_with_cats
  - friendly_with_dogs
  - suitable_for_fulltime_workers

  Use numeric values:
  - 0 = true
  - 1 = false
  - 2 = unknown
    
  ## Children Compatibility
  Map real ages or descriptions to categories:
    - "none" → cannot live with children
    - "any" → any age. Note that this field is always included when the query a dog needs to live with children
    - "older" → 10+
    - "teenager" → 13+
  If multiple children are mentioned, use the youngest child for determining filters.
    
  ## Example Output 1
  Query: I'm looking for a friendly girl dog, preferrably small or medium size. I commute for work monday to friday, so I need an independent dog tha can be left alone during weekdays. I have 2 kids, one's a teen and one is 12
  
  {
    "filter_expression": [
      {
        "field": "gender",
        "logical_operator": null,
        "filters": [
          { "comparison_operator": "equal", "value": "female" }
        ]
      },
      {
        "field": "size",
        "logical_operator": "or",
        "filters": [
          { "comparison_operator": "equal", "value": "small" },
          { "comparison_operator": "equal", "value": "medium" }
        ]
      },
      {
        "field": "suitable_for_fulltime_workers",
        "logical_operator": null,
        "filters": [
          { "comparison_operator": "equal", "value": 0 }
        ]
      },
      {
        "field": "can_live_with_children",
        "logical_operator": "or",
        "filters": [
          { "comparison_operator": "equal", "value": "any" },
          { "comparison_operator": "equal", "value": "older" }
        ]
      }
    ]
  }

  ## Example Output 2
  Query: Looking for a puppy not too big, has to get along with cats, and can't be dog aggresive

  {
    "filter_expression": [
      {
        "field": "age",
        "logical_operator": null,
        "filters": [
          { "comparison_operator": "less_or_equal", "value": 1 }
        ]
      },
      {
        "field": "size",
        "logical_operator": null,
        "filters": [
          { "comparison_operator": "not_equal", "value": "large" }
        ]
      },
      {
        "field": "friendly_with_cats",
        "logical_operator": null,
        "filters": [
          { "comparison_operator": "equal", "value": 0 }
        ]
      },
      {
        "field": "friendly_with_dogs",
        "logical_operator": null,
        "filters": [
          { "comparison_operator": "equal", "value": 0 }
        ]
      }
    ]
  }

  ## Example Output 3
  Query: It's my first time owning a dog

  {
    "filter_expression": [
      {
        "field": "experienced_dog_owners_needed",
        "logical_operator": null,
        "filters": [
          {
            "comparison_operator": "equal",
            "value": true
          }
        ]
      }
    ]
  }
  """
  
  client = InferenceClient(
    provider="cerebras",
    api_key=hugging_face_key,
    timeout=30
  )
  
  messages = [
    { "role": "system", "content": prompt },
    { "role": "user", "content": query }
  ]
  
  response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "FilterExpression",
        "schema": FilterExpression.model_json_schema(),
        "strict": True,
    },
  }
  
  try:
    response = client.chat_completion(
      messages=messages,
      response_format=response_format,  # type: ignore
      model="Qwen/Qwen3-32B",
      temperature=0.2,
    )
  except InferenceTimeoutError as e:
    logger.error("Inference timed out")
    raise FilterConstructionError("Inference timed out") from e
  except InferenceEndpointError as e:
    logger.error("Inference endpoint failed")
    raise FilterConstructionError("Inference endpoint failed") from e
  
  # Defensive Guards, in the event that `response` is None
  if not response.choices:
    logger.error("Inference returned no choices")
    raise FilterConstructionError("Inference returned no choices")

  content = response.choices[0].message.content
  if not content:
    logger.error("Inference returned empty content")
    raise FilterConstructionError("Inference returned empty content")
  
  # Parse JSON
  try:
    filter_json = json.loads(content)
  except json.JSONDecodeError as e:
    logger.error(f"JSON filter expression cannot be parsed: {e}")
    raise FilterConstructionError(f"JSON filter expression cannot be parsed: {e}") from e
  
  # Validate against Pydantic model
  try:
    filter_expression = FilterExpression.model_validate(filter_json)
  except ValidationError as e:
    logger.error(f"LLM response does not match expected schema: {e}")
    raise FilterConstructionError(f"LLM response does not match expected schema: {e}") from e
  
  return filter_expression


def build_single_filter(filter_condition: FilterCondition, filter_field: str) -> Filter:
  COMPARISON_OPERATOR_MAP = {
    "equal": "equal",
    "not_equal": "not_equal",
    "less_than": "less_than",
    "less_or_equal": "less_or_equal",
    "greater_than": "greater_than",
    "greater_or_equal": "greater_or_equal"
  }
  
  comparison_operator = filter_condition.comparison_operator
  value = filter_condition.value
  
  if comparison_operator in COMPARISON_OPERATOR_MAP:
    return getattr(Filter.by_property(filter_field), comparison_operator)(value)

  logger.debug(f"Unsupported operator: {comparison_operator}")
  raise ValueError(f"Unsupported operator: {comparison_operator}")


# This returns weaviate's _Filters type, but it is not exposed for public use, so type can't be annotated
def build_compound_filter(filter_conditions: List[FilterCondition], filter_field: str, logical_operator: LogicalOperator):
  compound_filters = [build_single_filter(filter_condition, filter_field) for filter_condition in filter_conditions]
  
  match logical_operator:
    case "or":
      return Filter.any_of(compound_filters) # type: ignore
    case "and":
      return Filter.all_of(compound_filters) # type: ignore


# This returns weaviate's _Filters type, but it is not exposed for public use, so type can't be annotated
def build_filter_expression(filter_expression: FilterExpression):
  filters = []
  
  for filter in filter_expression.filter_expression:
    if filter.logical_operator is None:
      filters.append(build_single_filter(filter.filters[0], filter.field))
    else:
      filters.append(build_compound_filter(filter.filters, filter.field, filter.logical_operator))
  
  if len(filters) == 0:
    return None
  logger.debug(f"filter produced: {filters}")
  return Filter.all_of(filters)
