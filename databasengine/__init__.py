#!/usr/bin/python
"""This is an in-memory database engine
It should support CRD (Create, Retrieve, Delete operations)
Update has been omitted as this shouldn't update their profile details. This application's purpose is just analytical
"""
# curl -XGET https://api.github.com/users/shrikrishnaholla/repos|grep -i python => for reference for future use
import datacollector
import query
from os import system
from datetime import datetime
database = dict()
def create(uname, details):
    """Create an entry to the database of LinkedIN profiles"""
    database[uname] = database.get(uname, details)

def delete(uname):
    """Delete profile"""
    if database.has_key(uname):
        del database[uname]   # more efficient than database.pop(uname)
                    
def display():
    """Displays the contents of the database on console (For testing purposes only)"""
    for professional, details in database.items():
        for field, description in details.items():
            print field,":",description
        print "="*100

if __name__ == '__main__':
    while True:
        choice = raw_input("""
            Welcome to LinkedIngine testing console!
            
            Enter a choice
            1: Create
            2: Delete
            3: Query
            4: Display
            5: Write existing database to file
            6: Quit

            """)
        try:
            if int(choice) == 1:
                try:
                    resumelist = datacollector.collect()  # Call to the data collector in datacollector.py
                    for name, details in resumelist.items():
                        create(name, details)             # Add profiles to the database individually
                except IOError:
                    print "Error: Database File Not Present\n."
                    continue
            elif int(choice) == 2:
                name = raw_input("Enter uname of the profile to delete")
                delete(name)

            elif int(choice) == 3:
                system('clear')                       # clear the console screen
                print query.__doc__
                print """
    
    Use quit to exit QuerySQL.
    
    Enter your query: """
                print "\n"
                while True:                                                 #remove "while" while integrating
                    qstring = raw_input("QuerySQL> ")
                    if(qstring.strip().lower() == "quit"):
                        print "Exiting QuerySQL..."
                        break
                    else:
                        try:
                            resultset = query.querystring(qstring, database) # Call the method in query.py
                            if len(resultset) > 0:
                                for result in resultset:                     # Print the obtained results (which is in a list)
                                    for field in result:
                                        print field, ':', result[field]
                                    print '='*50
                            else:
                                print "No match found"
                        except Exception as e:
                            print "Syntax Error in the entered Query, please check your syntax"
                            log = open("log.txt","a")
                            log.write(datetime.now().isoformat() +" | "+qstring.strip()+" | "+e.message +"\n")
                            log.close()

            elif int(choice) == 4:
                display()              # Display ALL the profiles in the database.

            elif int(choice) == 5:
                fo = open("data/datastore.in", "wb")
                fo.write(str(database))
                fo.close()

            elif int(choice) == 6:
                print "Exiting..\n"
                break

            else:
                raise ValueError

        except ValueError:              #invalid chice exception
            print "\nError:Invalid Choice"
            print "Please Enter a valid choice"
            continue

        quit = raw_input("Another operation? ")
        if quit.find('y') == -1 and quit.find('1') == -1: # The tester can either give just 'y' or 'yes' or '1'
            print "\tExiting..\n"
            break
