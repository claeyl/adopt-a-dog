import anthropic
import json
import os

from typing import Annotated, List, Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from weaviate.classes.query import Filter


ComparisonOperator = Literal["equal", "not_equal", "less_than", "less_or_equal", "greater_than", "greater_or_equal"]

class SimpleFilter(BaseModel):
  type: Literal["simple_filter"]
  field: str
  comparison_operator: ComparisonOperator
  value: str | int | float | bool

class OrFilter(BaseModel):
  type: Literal["or_filter"]
  filters: List[SimpleFilter]

class FilterExpression(BaseModel):
  filter_expression: List[
    Annotated[
      SimpleFilter | OrFilter,
      Field(discriminator="type")
    ]
  ]

class FilterConstructionError(Exception):
  """Raised when filter construction fails"""
  pass

def construct_json_filters_from_prompt(query: str) -> FilterExpression:
  load_dotenv()
  anthropic_key = os.getenv("ANTHROPIC_API_KEY")
  if not anthropic_key:
    raise ValueError("Couldn't find Anthropic key")
  
  client = anthropic.Anthropic(api_key=anthropic_key)
  
  prompt = """
  You are given a natural-language query about a user's needs and wants when adopting a dog.
  Your task is to extract only the properties explicitly mentioned or clearly implied in the query and convert them into JSON filters.
  
  ## Output Requirements
  Return a JSON object with this exact structure:
  {
    "filter_expression": [...]
  }
  The array contains filter objects. Each filter object can be either:

  ### Simple Filter
  {
    "type": "simple_filter",
    "field": "<field_name>",
    "comparison_operator": "<operator>",
    "value": <value>
  }

  ### OR Filter (for multiple acceptable values of the same field)
  {
    "type": "or_filter",
    "filters": [
      {
        "type": "simple_filter",
        "field": "<field_name>",
        "comparison_operator": "<operator>",
        "value": <value>
      },
      ...
    ]
  }
  
  If multiple acceptable values exist for a single field, return an object with:
  - "type" = "or_filter"
  - "filters" - a List of "simple_filter" objects, the structure is described above

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
  - medical_needs: boolean.
    - For this field, it refers to ongoing medical care requirements (e.g., "needs daily medication", "requires special diet", "needs regular vet visits").
    - This excludes disabilities like deafness, blindness, a dog having three legs, etc.
  - calm_home_needed: boolean
  
  ## Comparison Operator Rules
  - "equal" - exact match (e.g., "female dog" → gender equal "female")
  - "not_equal" - explicit exclusion (e.g., "not a large dog" → size not_equal "large")
  - "less_than" - strict maximum (e.g., "under 5kg" → weight less_than 5)
  - "less_or_equal" - inclusive maximum (e.g., "5kg or less" → weight less_or_equal 5)
  - "greater_than" - strict minimum (e.g., "over 20kg" → weight greater_than 20)
  - "greater_or_equal" - inclusive minimum (e.g., "at least 2 years old" → age greater_or_equal 2)
  
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
  
  ## Children Compatability
  If the query mentions children or any other concepts relating to dogs having to live with children, convert real ages into one of the categories:
  - "none" → cannot live with children
  - "any" → can live with children of any age
  - "older" → can only live with children who are aged 10+
  - "teenager" → can only live with children who are aged 13+

  Examples:
  - "I have a 5-year-old" → can_live_with_children equal "any"
  - "I have really young children" → can_live_with_children equal "any"
  - "I have a 12-year-old" → or_filter with can_live_with_children equal "older" OR equal "any"
  - "I have a 15-year-old" → can_live_with_children not_equal "none"
  - "I have an 11-year-old and a 14-year-old" → or_filter with can_live_with_children equal "older" OR equal "any".
    - The reason why we don't include teenagers is because we also have an 11 year old
  
  ## Important Instructions
  - Only include filters for properties explicitly mentioned or clearly implied in the query
  - Do not infer unrelated characteristics
  - Return valid JSON only - no markdown backticks, no explanations, no additional text
  - If nothing is mentioned, return: {"filter_expression": []}
  
  ## Example Output
  {
    "filter_expression": [
      {
        "type": "simple_filter",
        "field": "gender",
        "comparison_operator": "equal",
        "value": "female"
      },
      {
        "type": "or_filter",
        "filters": [
          {
            "type": "simple_filter",
            "field": "size",
            "comparison_operator": "equal",
            "value": "small"
          },
          {
            "type": "simple_filter",
            "field": "size",
            "comparison_operator": "equal",
            "value": "medium"
          }
        ]
      },
      {
        "type": "simple_filter",
        "field": "suitable_for_fulltime_workers",
        "comparison_operator": "equal",
        "value": true
      },
    ]
  }
  """
  
  try:
    response = client.messages.create(
      model="claude-sonnet-4-20250514",
      max_tokens=1024,
      system=prompt,
      messages=[
        {
          "role": "user",
          "content": query
        },
      ]
    )
  except anthropic.APIError as e:
    raise FilterConstructionError(f"Failed to call Anthropic API: {e}")
  
  if not response.content:
    raise FilterConstructionError("Received empty response from LLM")
  
  response_obj = response.content[0]
  if not isinstance(response_obj, anthropic.types.text_block.TextBlock):
    raise ValueError(f"Unexpected content type from llm call: {type(response_obj)}")

  response_text = response_obj.text  
  response_json = response_text.replace("```json", "").replace('```', '').strip()
  
  # Parse JSON
  try:
    filter_json = json.loads(response_json)
  except json.JSONDecodeError as e:
    raise FilterConstructionError(f"LLM returned invalid JSON: {e}\n, response preview: {response_json[:200]}")
  
  # Validate against Pydantic model
  try:
    filter_expression = FilterExpression.model_validate(filter_json)
  except ValidationError as e:
    raise FilterConstructionError(f"LLM response does not match expected schema: {e}")
  
  return filter_expression


def build_simple_filter(simple_filter: SimpleFilter) -> Filter:
  COMPARISON_OPERATOR_MAP = {
    "equal": "equal",
    "not_equal": "not_equal",
    "less_than": "less_than",
    "less_or_equal": "less_or_equal",
    "greater_than": "greater_than",
    "greater_or_equal": "greater_or_equal"
  }
  
  field = simple_filter.field
  comparison_operator = simple_filter.comparison_operator
  value = simple_filter.value
  
  if comparison_operator in COMPARISON_OPERATOR_MAP:
    return getattr(Filter.by_property(field), comparison_operator)(value)

  raise ValueError(f"Unsupported operator: {comparison_operator}")


# This returns weaviate's _Filters type, but it is not exposed for public use, so I can't annotate the type
def build_or_filter(or_filter: OrFilter):
  filters = []
  for filter in or_filter.filters:
    filters.append(build_simple_filter(filter))
  
  return Filter.any_of(filters)


# This returns weaviate's _Filters type, but it is not exposed for public use, so I can't annotate the type
def build_filter_expression(filter_expression: FilterExpression):
  filters = []
  for filter in filter_expression.filter_expression:
    if filter.type == "simple_filter":
      filters.append(build_simple_filter(filter))
    elif filter.type == "or_filter":
      filters.append(build_or_filter(filter))
  
  if len(filters) == 0:
    return None
  print(filters)
  return Filter.all_of(filters)
