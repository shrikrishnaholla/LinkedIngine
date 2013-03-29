#!/usr/bin/python
"""This module acts as an interface between the database and the application"""
from pymongo import MongoClient
client = MongoClient()
db = client.linkedIngine_db       # Create/connect to a database with the name 'linkedIngine_db'
collection = db.linkedIngine_col  # Create/connect to a collection with the name 'linkedIngine_col'

def queryer(params):
    """This method returns a list of all the profiles in the database that satisfy the parameters"""
    resultlist = list()
    resultset = collection.find(params)
    if resultset.count() > 0:
        for person in resultset:
            resultlist.append(person)
    else: # Suppose the parameters are given wrongly, we mustn't NOT return anything. Try best effort approach
        values = params.values()
        for value in values:
            for result in collection.find({'tags':value}): # The keyword sent as parameter may be present as tag
                resultlist.append(result)
    return resultlist