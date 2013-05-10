from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import urlparse
import dbinterface
import json
import os

returnFields = ["first_name_r","last_name_r","headline_r","industry_r","degrees_r","majors_r","colleges_r","skills_r","job_titles_r","companies_r","public_profile_url_r"]
params = ["first_name","last_name","headline","industry","degrees","majors","colleges","skills","job_titles","companies","public_profile_url"]
class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): 
        log = open("log.txt", "a").write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format%args)) 
    ''''first_name_r=on&last_name_r=on&headline_r=on&industry_r=on&degrees_r=on&majors_r=on&colleges_r=on&skills_r=on&job_titles_r=on&companies_r=on&public_profile_url_r=on&count=10&first_name=test&last_name=test&last_name=test&last_name=test&last_name=test&last_name=test&last_name=test&skills=test&job_titles=test&companies=test&public_profile_url=test'''

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path) # get the path
        print parsed_path
        parsed_query = urlparse.parse_qs(parsed_path.query)
        self.requestHandlers(parsed_path.path, parsed_query)
        return

    def requestHandlers(self, parsedURL, parsedQuery):
        # if parsedURL == 'index.html' or '/':
        if len(parsedQuery) == 0:
            if parsedURL.endswith('css'):
                self.render(200,parsedURL[1:],'text/css')
            elif parsedURL.endswith('js'):
                self.render(200,parsedURL[1:],'text/javascript')
            elif parsedURL == '/favico.ico':
                return
            elif parsedURL.endswith('png'):
                print 'here'
                self.render(200,parsedURL[1:],'image/png')
            elif parsedURL == '/' or parsedURL == '/index.html':
                self.render(200, 'index.html')
            else:
                print "URL : " + parsedURL
                self.render(404,'404.html')
        else:
                print 'parsed query:', parsedQuery
                self.handleQuery(parsedQuery)
    def render(self, code, path, content_type = 'text/html'):
        print "Rendering :", path 
        html = open(path, 'rb')
        page = html.read()
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(page)
        return

    def handleQuery(self, query):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        returnDict = dict()
        numberOfProfiles = 'all'
        paramDict = dict()

        
        paramDict = self.buildParamDict('Male', query['query[]'], 'gender', 'male', paramDict)
        paramDict = self.buildParamDict('Female', query['query[]'], 'gender', 'female' , paramDict)
        paramDict = self.buildParamDict('North', query['query[]'], 'area', 'north' , paramDict)
        paramDict = self.buildParamDict('South', query['query[]'], 'area', 'south' , paramDict)
        paramDict = self.buildParamDict('East', query['query[]'], 'area', 'east' , paramDict)
        paramDict = self.buildParamDict('West', query['query[]'], 'area', 'west' , paramDict)
        paramDict = self.buildParamDict('Web', query['query[]'], 'categories', 'web' , paramDict)
        paramDict = self.buildParamDict('Mobile', query['query[]'], 'categories', 'mobile' , paramDict)
        paramDict = self.buildParamDict('Management', query['query[]'], 'categories', 'management' , paramDict)
        paramDict = self.buildParamDict('Software Engineering', query['query[]'], 'categories', 'software_engineering' , paramDict)
        paramDict = self.buildParamDict('Networks', query['query[]'], 'categories', 'networks' , paramDict)
        paramDict = self.buildParamDict('Research', query['query[]'], 'categories', 'research' , paramDict)
        paramDict = self.buildParamDict('Testing', query['query[]'], 'categories', 'testing' , paramDict)
        paramDict = self.buildParamDict('Experience', query['query[]'], 'categories', 'experienceindex' , paramDict)
        paramDict = self.buildParamDict('Education', query['query[]'], 'categories', 'educationindex' , paramDict)

        resultlist = dbinterface.queryer(paramDict)
        for result in resultlist:
            result.pop("_id")

        self.wfile.write(json.dumps(resultlist))
        return

    def buildParamDict(self, item, querylist, category, text, paramDict):
        paramDict[category] = paramDict.get(category, list())
        try:
            if item in querylist:
                paramDict[category].append(text)
        except ValueError:
            pass
        return paramDict

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass

if __name__ == '__main__':
    server = ThreadedHTTPServer(('', 8080), Handler)
    print 'Starting server on port 8080, use <Ctrl-C> to stop'
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Exiting server'
