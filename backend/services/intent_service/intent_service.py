import joblib
import logging

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


def query_related_to_adoption(query: str) -> bool:
  embed_model = SentenceTransformer("backend/services/intent_service/query_embedding_model")
  clf = joblib.load("backend/services/intent_service/query_classifier.pkl")
  
  emb = embed_model.encode([query])
  label = clf.predict(emb)[0]
  logging.info(f"{query} -> {label} (confidence {clf.predict_proba(emb)[0][1]:.2f})")
  
  return bool(label)
