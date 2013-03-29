
Webapp
======


Dbinterface
-----------

This module acts as an interface between the database and the application  

###queryer###

This method returns a list of all the profiles in the database that satisfy the parameters  

Profilefetcher
--------------

The fetcher of LinkedIn profiles. This module acts as the controller for all operations related to   
crawling the LinkedIn profiles  

###fetchProfiles###

Given the URL from where to initiate the crawling, it first fetches the webpage, sends it to  
    the crawler for scraping data from the webpage. Not only that, it also reads all the public profile  
    urls present in the current page and adds them to the list. In subsequent iterations, it will fetch  
    the LinkedIn profiles of people associated with these urls. The iteration continues for the number of  
    times specified by maxcount  

###google###

Google for LinkedIn profiles with the parameters  

###acceptCLArguments###

Initializing parser for accepting command line arguements  

Crawler
-------

This module is used to crawl through and scrape useful information from a LinkedIn profile web page  

###contentExtractor###

Extract contents from LinkedIn profile page and add them to the database if not present  

###multipleInstanceExtractor###

Extract entries that can have more than one values. Returned as a list of instances of occurance  

###fieldExtractor###

Extract entries whose nature is of the form 'Field:Value'  
