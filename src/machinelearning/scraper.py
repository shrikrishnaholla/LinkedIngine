#!/usr/bin/python
"""Scrape useful profile information from an html page using BeautifulSoup"""

from BeautifulSoup import BeautifulSoup
import dbinterface

def scrape(page, public_profile_url):
    resume = dict()
    soup = BeautifulSoup(page, convertEntities=BeautifulSoup.HTML_ENTITIES)
    soup = soup.find(id="main")    # The id "main" contains their profile data
    resume['first_name'] = collect(soup, 'span', 'given-name')
    resume['last_name']  = collect(soup, 'span', 'family-name')
    resume['headline']  = collect(soup, 'p', 'headline-title title')
    resume['locality']   = collect(soup, 'span', 'locality')
    resume['industry']   = collect(soup, 'dd', 'industry')
    # Scrape fields that can have more than one elements
    resume['degrees']   = collect(soup, 'span', 'degree', True)
    resume['major']     = collect(soup, 'span', 'major', True)
    resume['colleges']  = collect(soup, 'h3', 'summary fn org', True)
    resume['job_titles']= collect(soup, 'a', 'title', True)
    resume['companies'] = collect(soup, 'span', 'org summary', True)
    resume['experience'] = collect(soup, 'span', 'duration', True)
    resume['skills']    = collect(soup, 'a', 'jellybean', True)

    # incompatible with crawl_from_list()
    projects = soup.find(id="profile-projects")
    if projects:
        resume['project-descriptions'] = []
        for project in projects.findAll('p'):
            resume['project-descriptions'].append(project.getText())

    for experience in resume['experience']:
        string = experience.strip('()')
        years = -1; months = -1

        string, years = extractExperience(string, 'years')
        if years < 0:
            string, years = extractExperience(string, 'year')
        
        string, months = extractExperience(string, 'months')
        if months < 0:
            string, months = extractExperience(string, 'month')
        
        if years > -1 or months > -1:
            replacement = dict()
            if years > -1:
                replacement['years'] = years
            if months > -1:
                replacement['months'] = months
            if len(replacement.keys()) > 0:
                resume['experience'][resume['experience'].index(experience)] = replacement

    resume['public_profile_url'] = public_profile_url

    if dbinterface.collection.find(resume).count() == 0:
        dbinterface.collection.save(resume)

    return resume

def collect(soup, domnode, htmlclass, multiple=False):
    """Easy method to collect fields"""
    if multiple:
        return [result.getText() for result in soup.findAll(domnode, {"class":htmlclass})]
    else:
        content = soup.find(domnode, {"class":htmlclass})
        if content:
            return content.getText()
        else:
            return ''

def extractExperience(string, text):
    var = -1
    if string.find(text) != -1:
        try:
            var = int(string[:string.index(text)-1])
            string = string[string.index(text)+len(text)-1:].strip()
        except ValueError:
            if string[1] == ' ':
                string, var = extractExperience(string[2:], text)
    return (string, var)

if __name__ == '__main__':
    page = open('reference.profile.2', 'r')
    resume = scrape(page, 'http://www.example.com/')

    for key in resume.keys():
        print key, ':', resume[key]