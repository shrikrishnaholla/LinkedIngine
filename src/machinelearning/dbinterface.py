#!/usr/bin/python
"""This module acts as an interface between the database and the application"""
#import profilefetcher
import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.linkedIngine_db_1       # Create/connect to a database with the name 'linkedIngine_db'
collection = db.linkedIngine_col_1  # Create/connect to a collection with the name 'linkedIngine_col'

def queryer(params):
    # Sample params dict
    #{
    #    'gender': 'male',
    #    'area': 'south',
    #    'categories': ['web','mobile','research','management','networks','software_engineering',
    #                    'experienceindex', 'educationindex']
    #}

    gender, area, categories = (params.get('gender'), params.get('area'), params.get('categories') )

    if gender and area:
        results = collection.find({'gender': gender, 'area':area})
    elif gender:
        results = collection.find({'gender': gender})
    elif area:
        results = collection.find({'area': area})
    else:
        results = collection.find()

    resultlist = list()
    for result in results:
        resultlist.append(result)

    if categories:
        for category in categories:
            resultlist = sorted(resultlist, key=lambda dic: dic[category], reverse=False)

    return resultlist

if __name__ == '__main__':
    print len(queryer({'gender':'male', 'area':'north', 'categories': ['software_engineering','experienceindex']}))
    print len(queryer({'categories': ['web']}))