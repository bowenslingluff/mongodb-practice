from pymongo import MongoClient, errors
from urllib.parse import quote_plus
from bson.json_util import dumps
import os

MONGOUSER = os.getenv('MONGOUSER')
MONGOPASS = os.getenv('MONGOPASS')
MONGOHOST = os.getenv('MONGOHOST')
print("Env vars loaded:")
print("MONGOUSER:", MONGOUSER)
print("MONGOHOST:", MONGOHOST)

MONGO_URI = f"mongodb+srv://{quote_plus(MONGOUSER)}:{quote_plus(MONGOPASS)}@{MONGOHOST}/"


client = MongoClient(MONGO_URI, retryWrites=True)

client.admin.command('ping')
print("✅ Connection to MongoDB successful!")

mflix = client.sample_mflix

snack_collection = mflix.movie_snacks

snacks = [
    {
        "name": "Popcorn",
        "type": "Popcorn",
        "flavor": "Butter",
        "size": "Large",
        "price": 7.50,
        "available": True
    },
    {
        "name": "Orange Fanta",
        "type": "Soda",
        "flavor": "Orange",
        "size": "Medium",
        "price": 5.00,
        "available": True
    },
    {
        "name": "Sour Patch Kids",
        "type": "Candy",
        "flavor": "Sour Fruit Mix",
        "size": "Small",
        "price": 2.50,
        "available": False
    },
    {
        "name": "Nachos",
        "type": "Snack",
        "flavor": "Cheddar",
        "size": "Large",
        "price": 7.99,
        "available": True
    },
    {
        "name": "Peanut M&Ms",
        "type": "Candy",
        "flavor": "Chocolate + Peanut",
        "size": "Small",
        "price": 2.50,
        "available": True
    }
]

try:
    # Insert only if the collection is empty
    print(snack_collection)
    if snack_collection.count_documents({}) == 0:
        snack_collection.insert_many(snacks)
        print("Snack documents inserted.")
    else:
        print("Collection already has documents. Skipping insert.")

    available_snacks = snack_collection.find({"available": True}).limit(3)
    print("Three available snacks:")
    print(dumps(available_snacks, indent=2))
except errors.PyMongoError as e:
    print(f"Error: {e}")

client.close()

