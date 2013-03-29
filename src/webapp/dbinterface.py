from pymongo import MongoClient
client = MongoClient()
db = client.linkedIngine_db
collection = db.linkedIngine_col

def queryer(profile):
    resultlist = list()
    for person in collection.find(profile):
        resultlist.append(person)
    return resultlist