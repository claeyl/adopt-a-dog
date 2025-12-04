from fastapi import FastAPI

app = FastAPI()

@app.post("/query/{query}")
def query_dog_collection(query: str):
  return {"dog": "Penny"}

@app.get("/")
def read_root():
  return {"Hello": "World"}