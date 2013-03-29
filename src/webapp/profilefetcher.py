import urllib2
import re
import crawler
import argparse
import sys

def fetchProfiles(initURL, maxcount):
    count = 0
    links = set([initURL])
    fetched = list()

    while count< maxcount:
        count+=1

        while True:
            newreq = links.pop()
            if newreq not in fetched:
                fetched.append(newreq)
                break

        page = urllib2.urlopen(fetched[-1]).read()

        crawler.contentExtractor(page, fetched[-1])

        links.update(re.findall(r'http://.*linkedin.com/pub/(?:[a-z]*[-]?)*(?:/?[0-9]?[a-z]?)*\?trk=pub-pbmap', page))

        links = set([link.strip('"') for link in links])
        #links = set(links) 

        if maxcount % count == 0:
            sys.stdout.write('\r'+'='*int((count*10.0/maxcount)*10.0)+'>'+ ((count*100.0/maxcount))+'%')

def acceptCLArguments():
    # Initializing parser for accepting command line arguements
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