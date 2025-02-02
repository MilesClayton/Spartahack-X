from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json



def upload_to_db():
    username = "Jakeaspade" # input("Enter database login: ")
    password = "Whitegold626" # input("Enter Password: ")
    uri = f"mongodb+srv://{username}:{password}@freedb.xh3be.mongodb.net/?retryWrites=true&w=majority&appName=FreeDB"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    db = client.My_Database.Test

    with open("Detected_Threat_Data/data.json", "r") as file:
        data = json.load(file)
    file.close()

    results = db.insert_one(data)
    if results.acknowledged:
        print("Data successfully uploaded to mongoDB!")
    return db

def download_from_db(db):
    latest_entry = db.find_one(sort=[("_id", -1)])

    # Print the result
    return latest_entry