#!/usr/bin/python
"""
Naive Bayes Classifier to classify profiles.
Classifications: (1): Male/Female
                 (2): North/South/East/West
"""

import dbinterface
import nltk

def gender_features(word):
    return {'last_letter': word[-2]}

def initGenderClassifier():
    from nltk.corpus import names
    names = ([(name, 'male') for name in names.words('male.txt')] +
              [(name, 'female') for name in names.words('female.txt')])
    featuresets = [(gender_features(n), g) for (n,g) in names]
    return nltk.NaiveBayesClassifier.train(featuresets)

gender_classifier = initGenderClassifier()

def initLocationClassifier():
    cities = open('data/indiancities', 'r').readlines()
    classes = [({'name':city.split()[0]},city.split()[1]) for city in cities]
    return nltk.NaiveBayesClassifier.train(classes)

location_classifier = initLocationClassifier()

def classify():
    for profile in dbinterface.collection.find():
        first_name = profile['first_name']
        locality   = profile['locality'].split()[0]

        gender, location = None, None

        # Classifiers
        if not profile.has_key('gender') or not profile.has_key('location'):
            gender = gender_classifier.classify(gender_features(first_name))
            location = location_classifier.classify({'name':locality})

        dbinterface.collection.update({'public_profile_url':profile['public_profile_url']},
                                         {'$set': {'gender':gender, 'location':location}})

if __name__ == '__main__':
    page = open('reference.profile.2', 'r')
    import scraper
    resume = scraper.scrape(page, 'http://www.example.com/')
    classify()