# Note this deletes the data as well as the schema definition

import weaviate

client = weaviate.connect_to_local()
client.collections.delete("Dog")
client.close()