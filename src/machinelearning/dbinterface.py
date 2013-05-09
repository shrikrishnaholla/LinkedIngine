#!/usr/bin/python
"""This module acts as an interface between the database and the application"""
#import profilefetcher
import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.linkedIngine_db_1       # Create/connect to a database with the name 'linkedIngine_db'
collection = db.linkedIngine_col_1  # Create/connect to a collection with the name 'linkedIngine_col'

def getOptions(which, options, querydict):
    if len(options) == 1:
        querydict[which] = options[0]
    else:
        querydict['$or'] = querydict.get('$or', list())
        for option in options:
            querydict['$or'].append({which:option})
    return querydict

def queryer(params):
    # Sample params dict
    #{
    #    'gender': ['male'],
    #    'area': ['south'],
    #    'categories': ['web','mobile','research','management','networks','software_engineering', 'testing',
    #                    'experienceindex', 'educationindex']
    #}

    gender, area, categories = (params.get('gender'), params.get('area'), params.get('categories') )
    querydict = dict()
    if gender:
        querydict = getOptions('gender', gender, querydict)
    if area:
        querydict = getOptions('area', area, querydict)
    results = collection.find(querydict)

    resultlist = list()
    for result in results:
        resultlist.append(result)

    if categories:
        for category in categories:
            resultlist = sorted(resultlist, key=lambda dic: dic[category], reverse=True)

    return resultlist

if __name__ == '__main__':
    print len(queryer({'gender':['male', 'female'], 'area':['north', 'south'], 'categories': ['software_engineering','experienceindex']}))
    print len(queryer({'categories': ['web']}))