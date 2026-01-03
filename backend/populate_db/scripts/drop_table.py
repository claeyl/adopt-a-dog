# Note this deletes the data as well as the schema definition

from services.db_client import create_db_client

client = create_db_client()
client.collections.delete("Dog")
client.close()