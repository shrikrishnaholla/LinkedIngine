#!/usr/bin/python
"""This is a module used to scrape the public profiles of linkedIn users for meaningful profile data
Usage: Suppose the profile of the person XYZ whose data is required has a linkedIn profile whose public url goes by
www.linkedin.com/pub/xyz/123/456/789, on prompted, input 'xyz/123/456/789' into the console"""
# TODOs:
# 1: Ask user input only when testing (using ifmain) => make it an api that can be called from another module
# 2: search for the person and get his url instead of expecting the user to know it

import requests
from BeautifulSoup import BeautifulSoup
#initialize the structure in which to hold data, and also a list to hold the url of all profiles
d = dict()
links = []
while True:
    links.append(raw_input('Enter the public profile url: '))
    page = requests.get('http://www.linkedin.com/pub/'+links[len(links)-1])        # Send a GET request to their public profile
    soup = BeautifulSoup(page.content, convertEntities=BeautifulSoup.HTML_ENTITIES)
    soup = soup.find(id="main")                                                     # The id "main" contains their profile data

    # Scraping the data
    # TODO: can't this be modularized into a separate method?
    # TODO: repetition of steps - modularize
    d['fname'] = soup.find("span", { "class" : "given-name" }).getText()
    d['lname'] = soup.find("span", { "class" : "family-name" }).getText()
    d['locality'] = soup.find("span", { "class" : "locality" }).getText()
    d['industry'] = soup.find("dd", { "class" : "industry" }).getText()
    d['current'] = str(soup.find("ul", {"class":"current"}).findAll("li")[0].getText()).replace('at', ' at ') #TODO:devise an alternative

    # Scrape fields that can have more than one elements
    # TODO: repetition of procedures for a lot of stuff - modularize
    pastjobs = soup.find("dd", {"class":"summary-past"})
    if pastjobs:
        # TODO: use better variable names
        j=0
        d['past'] = dict()
        for i in pastjobs.findAll('li'):
            j+=1
            d['past'][j] = str(i.getText()).replace('at', ' at ') # used because, otherwise they would stick together. Ex: "StudentatPESIT"

    education = soup.find("dd", {"class":"summary-education"})
    if education:
        j=0
        d['education'] = dict()
        for i in education.findAll('li'):
            j+=1
            d['education'][j] = i.getText()

    skills = soup.find("ol", {"class":"skills"})
    if skills:
        j=0
        d['skills'] = dict()
        for i in skills.findAll('li'):
            j+=1
            d['skills'][j] = i.getText()

    projects = soup.find(id="profile-projects")
    if projects:
        j=0
        d['project-descriptions'] = dict()
        for i in projects.findAll('p'):
            j+=1
            d['project-descriptions'][j] = i.getText()

    choice = raw_input("One more? ")
    if choice.find('y') == -1 and choice.find('1') == -1: # The tester can either give just 'y' or 'yes' or '1'
        break