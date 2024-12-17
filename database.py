# database.py
from pymongo import MongoClient
from config import config

# Initialize MongoDB client and connect to the database
client = MongoClient(config.MONGO_URI)
# db = client['quizapp']  # Access the database named 'quizapp'
db = client['quizapp']

users_collection = db['users']
print(f"this is user collection {users_collection} from database {db}")
