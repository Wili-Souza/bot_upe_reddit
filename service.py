from pymongo import MongoClient
from config import url_db

client = MongoClient(url_db)
db = client.botDB

# --- collections
qa = db.qaReddit
replied = db.idReddit
commands = db.commandsReddit


# --- get documents
def get_qa():
    return  list(qa.find())

def get_ids():
    return [x["value"] for x in replied.find()]

def get_commands():
    return list(commands.find())


# --- insert documents
def save_as_replied(doc_id):
    replied.insert_one({"value": doc_id})
