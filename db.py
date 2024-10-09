# db.py

from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI

# Initialize MongoDB client
client = MongoClient(MONGO_URI)

# Select the database and collection
db = client['test']
collection = db['selectedtexts']

# Function to update the summary and tags in the MongoDB document
def update_text_summary(text_id, summary, tags):
    try:
        result = collection.update_one(
            {'_id': ObjectId(text_id)},
            {'$set': {'summary': summary, 'tags': tags}}
        )
        if result.matched_count > 0:
            print(f"Successfully updated text with id {text_id}")
        else:
            print(f"Document with id {text_id} not found")
    except Exception as e:
        print(f"Error updating MongoDB document: {e}")
