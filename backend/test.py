from pymongo import MongoClient

# Connection URI
CONNECTION_STRING = "mongodb+srv://developement:Aw1undaNmPi1g3xy@devepmentone.bhpyl.mongodb.net/?retryWrites=true&w=majority&appName=devepmentOne"

# Initialize client
client = MongoClient(CONNECTION_STRING)

# Access or create a database
db = client["development"]

# Create or access a collection
collection = db["test_collection"]

# Insert a document
collection.insert_one({"name": "test", "value": "sample"})

# Verify insertion
print("Collections:", db.list_collection_names())

# Close the client connection
client.close()
