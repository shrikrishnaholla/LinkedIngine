#!/usr/bin/python
"""This is a module used to scrape the public profiles of linkedIn users for meaningful profile data
Usage: Suppose the profile of the person XYZ whose data is required has a linkedIn profile whose public url goes by
www.linkedin.com/pub/xyz/123/456/789, on prompted, input 'xyz/123/456/789' into the console"""
# TODOs:
# 2: search for the person and get his url instead of expecting the user to know it

import requests
from BeautifulSoup import BeautifulSoup
#initialize the structure in which to hold data, and also a list to hold the url of all profiles
resume = dict()
links = []

def scrape(link):
    if len(link.split('linkedin.com/pub/')) > 1:    # If the input is the whole link
        link = link.split('linkedin.com/pub/')[-1]  # extract only the username string

    page = requests.get('http://www.linkedin.com/pub/'+link)    # Send a GET request to their public profile
    soup = BeautifulSoup(page.content, convertEntities=BeautifulSoup.HTML_ENTITIES)
    soup = soup.find(id="main")    # The id "main" contains their profile data

    # Scraping the data
    collect('fname', 'span', 'given-name')
    collect('lname', 'span', 'family-name')
    collect('locality', 'span', 'locality')
    collect('industry', 'dd', 'industry')

    # incompatible with collect()
    resume['current'] = str(soup.find("ul", {"class":"current"}).findAll("li")[0].getText()).replace('at', ' at ') 
    #TODO:devise an alternative

    # Scrape fields that can have more than one elements
    collectmultiple('dd', 'summary-past', 'past', 'li', 'at')
    collectmultiple('dd', 'summary-education', 'education', 'li')
    collectmultiple('ol', 'skills', 'skills', 'li')

    # incompatible with collectmultiple()
    projects = soup.find(id="profile-projects")
    if projects:
        counter=0
        resume['project-descriptions'] = dict()
        for project in projects.findAll('p'):
            counter+=1
            resume['project-descriptions'][counter] = project.getText()

def collect(hashkey, domnode, htmlclass):
    """Easy method to collect fields"""
    resume[hashkey] = soup.find(domnode, {"class":htmlclass}).getText()

def collectmultiple(domnode, htmlclass, hashkey, subnode,*at):
    """Easy method to collect fields with multiple attributes"""
    section = soup.find(domnode, {"class":htmlclass})
    if section:
        counter = 0
        resume[hashkey] = dict()
        for subsection in section.findAll(subnode):
            counter+=1
            if at:
                resume[hashkey][counter] = str(subsection.getText()).replace('at', ' at ')
            else:
                resume[hashkey][counter] = subsection.getText()

def testing():
    while True:
        links.append(raw_input('Enter the public profile url: '))
        if not links[-1] in links[:-1]:
            scrape(links[-1])
        choice = raw_input("One more? ")
        if choice.find('y') == -1 and choice.find('1') == -1: # The tester can either give just 'y' or 'yes' or '1'
            break

if __name__ == '__main__':
    testing()