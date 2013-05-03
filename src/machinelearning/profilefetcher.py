#!/usr/bin/python
"""The fetcher of LinkedIn profiles. This module acts as the controller for all operations related to 
crawling the LinkedIn profiles"""
import urllib2
import re
import argparse
import sys
import requests

import scraper
import classifier
import regression

from datetime import datetime

profileURL = re.compile(r'http://.*linkedin.com/pub/(?:[a-z]*[-]?)*(?:/?[0-9]?[a-z]?)*\?trk=pub-pbmap')

def fetchProfiles(initURL, maxcount):
    """Given the URL from where to initiate the crawling, it first fetches the webpage, sends it to
    the crawler for scraping data from the webpage. Not only that, it also reads all the public profile
    urls present in the current page and adds them to the list. In subsequent iterations, it will fetch
    the LinkedIn profiles of people associated with these urls. The iteration continues for the number of
    times specified by maxcount"""
    count = 0
    links = set([initURL])
    waitinglist = list()

    start = datetime.now()

    while count< maxcount:
        count += 1

        while True:
            newreq = links.pop()
            if newreq not in waitinglist:   # If the url hasn't be used already, add it to the waiting list
                waitinglist.append(newreq)
                break

        try:
            page = urllib2.urlopen(waitinglist[-1]).read() # Fetch the web page from the url just appended
        except:
            pass

        scraper.scrape(page, waitinglist[-1]) # Send the page and the url for scraping

        links.update(profileURL.findall(page))
        # Get all the urls present in this web page

        links = set([link.strip('"') for link in links])

        percentage = int(count*100.0/maxcount)    # Progress bar
        sys.stdout.write('\r'+'='*percentage+'>'+' '*(101-percentage) +str(percentage)+'%')
        sys.stdout.flush()

    print 'Fetched', count, 'profiles in', \
     (datetime.now() - start).minutes, 'minutes, and', (datetime.now() - start).minutes, 'seconds'

    start = datetime.now()
    classifier.classify()
    print 'Classified all profiles in database in', \
     (datetime.now() - start).minutes, 'minutes, and', (datetime.now() - start).minutes, 'seconds'

    regression.regresser()
    print 'Calculated regression for all profiles in database in', \
     (datetime.now() - start).minutes, 'minutes, and', (datetime.now() - start).minutes, 'seconds'

def google(params):
    """Google for LinkedIn profiles with the parameters"""
    print 'Googling with params', params
    url = 'http://google.com/search?btnI=1&q='+'+'.join(params)+'+linkedin' # Does the I'm Lucky! search
    try:
        page = requests.get(url, allow_redirects=True)
        if re.match(r'http://.*linkedin.com/pub/dir/*',page.url):
            return False
        else: 
            crawler.contentExtractor(page.content, page.url)
            return True
    except:
        return False

def acceptCLArguments():
    """Initializing parser for accepting command line arguements"""
    parser = argparse.ArgumentParser(
        description="""Build database of LinkedIn public profiles by crawling through their pages""")

    # Assign port number to socket
    parser.add_argument(
        '-u','--url', default='http://www.linkedin.com/pub/anantharaman-p-n/7/511/811', type=str, metavar='str',
        help='The URL of the public profile to start crawling from')

    # Number of profiles to generate
    parser.add_argument(
        '-n','--number', default=10, type=int, metavar='int',
        help='Number of profiles to fetch from LinkedIn [Default:10]')

    return parser.parse_args()

if __name__ == '__main__':
    args = acceptCLArguments()
    fetchProfiles(args.url, args.number)
    print