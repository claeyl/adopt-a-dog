import re

from models.types import Gender, Size


def format_id(raw: str) -> int:
  """
  Dog ID given in the form of a text `ID: 16760`
  Return the ID if it exists
  """
  match = re.search(r"ID: (\d+)", raw)
  
  if not match:
    # should never reach here because earlier calls filter out invalid ids
    raise ValueError(f"Can't parse dog id: {raw}")
  return int(match.group(1))


def format_gender(raw: str) -> Gender:
  match = re.match(r"female", raw, re.IGNORECASE)
  return "female" if match else "male"


def format_breed(raw: str) -> str:
  return raw.lower()


def format_size(raw: str) -> Size:
  match = re.search(r"(small|medium|large)", raw, re.IGNORECASE)
  if match:
    size = match.group(1).lower()
    if size in ("small", "medium", "large"):
      return size
  return "medium"


def format_age(raw: str) -> int:
  """
  Given an age in the form of 'X Years & Y Months & Z Week', return the dog's age rounded down to the number of years
  If we have an incomplete string like 'Y Months & Z Week' or 'Z Week' OR 'Y Months', return 0
  """
  match = re.search(r"(\d+) Years", raw)
  if match:
    return int(match.group(1))
  else:
    return 0


def format_weight(raw: str) -> float:
  return _extract_number(raw)


def format_fee(raw: str) -> float:
  return _extract_number(raw)


def format_dog_description(raw_description: list[str]) -> str:
  """
  Given a dog's description wrapped in <p> tags, extract all text within the <p> tags,
  but exclude the last <p> tag, as it is a call to action to adopt a dog (not part of description)
  """
  description_minus_cta = raw_description[:-1]
  return " ".join(description_minus_cta)


def _extract_number(sentence: str) -> float:
  """
  Extract a number from a given string and return it
  Return 0.0 if no number can be extracted
  """
  number = re.search(r"\d+\.?\d*", sentence)
  if number:
    return float(number.group(0))
  return 0.0
