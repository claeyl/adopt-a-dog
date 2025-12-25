import json
import joblib
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

# This script will be run once, to save our model

DATASET_PATH = "dataset.jsonl"
texts = []
labels = []

with open(DATASET_PATH, "r", encoding="utf-8") as f:
  for line in f:
    item = json.loads(line)
    texts.append(item["text"])
    labels.append(item["label"])

labels_np = np.array(labels)

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(texts, show_progress_bar=True)

clf = LogisticRegression(max_iter=2000)
clf.fit(embeddings, labels)

model.save("query_embedding_model")
joblib.dump(clf, "query_classifier.pkl")