import os
from pymongo import MongoClient

host = os.environ.get("MONGO_HOST", "localhost")
port = os.environ.get("MONGO_PORT", "27017")
connection_string = f"mongodb://{host}:{port}/"

client = MongoClient(connection_string)
collection = client.scriptscribe.users
