import logging
import os
import re

from backend.models.Dog import Dog
from dotenv import load_dotenv
from huggingface_hub import InferenceClient, InferenceEndpointError, InferenceTimeoutError

logger = logging.getLogger(__name__)

def explain_relevance(dog: Dog, query: str) -> str:
  load_dotenv()
  hugging_face_key = os.getenv("HUGGING_FACE_API_KEY")
  if not hugging_face_key:
    logger.error("Couldn't find hugging face api key")
    raise ValueError("Couldn't find hugging face api key")
  
  prompt=f"""
  /no_think
  Write a brief explanation of why this dog matches what the person is looking for.
  
  What the person wants: {query}
  
  Matched Dog: {dog}
  
  Instructions:
  - Be specific about the connections - don't just say "good match"
  - Use only information provided about the dog - no assumptions
  - Write 2-3 natural sentences, maximum 60 words
  - Don't repeat the person's query verbatim - paraphrase the needs when connecting them
  """
  
  client = InferenceClient(
    provider="cerebras",
    api_key=hugging_face_key,
    timeout=30
  )
  
  messages = [{ "role": "system", "content": prompt }]
  
  content = ""
  try:
    response = client.chat_completion(
      messages=messages,
      model="Qwen/Qwen3-32B",
    )

    choice = response.choices[0]
    content = getattr(choice.message, "content", "").strip()

    if not content:
      logger.error("Inference returned empty content")

  except (InferenceTimeoutError, InferenceEndpointError) as e:
    logger.error(f"Inference failed: {e}")
  except Exception as e:
    logger.error(f"Unexpected error during inference: {e}")
  finally:
    return re.sub(r"<think>.*?<\/think>", "", content, flags=re.DOTALL).strip()
