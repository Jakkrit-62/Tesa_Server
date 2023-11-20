from pymongo import MongoClient

# Connect to MongoDB
db_client = MongoClient('localhost', 27017)

# Create Database
db = db_client.details

# Create Collection
storage = db.storage

# Create a sample data item
data_item = {
    "name": "Guy",
    "age": 20,
    "University": "PSU"
}

# Insert data into the database
insert_result = storage.insert_one(data_item)
print("Data inserted with record id", insert_result.inserted_id)

# Read data from the database
print("\nReading data from the database:")
for document in storage.find():
    print(document)
