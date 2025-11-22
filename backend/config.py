import os

from pymongo import MongoClient

connection_string = os.getenv("DB_CONNECTION")

client = MongoClient(connection_string)
collection = client.scriptscribe.users
