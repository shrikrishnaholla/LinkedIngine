#!/usr/bin/python
"""This is an in-memory database engine
It should support CRD (Create, Retrieve, Delete operations)
Update has been omitted as this shouldn't update their profile details. This application's purpose is just analytical
"""
# curl -XGET https://api.github.com/users/shrikrishnaholla/repos|grep -i python => for reference for future use
import csv
import datacollector
database = dict()
def create(uname, details):
    """Create an entry to the database of LinkedIN profiles"""
    database[uname] = database.get(uname, details)

def delete(uname):
    """Delete profile"""
    if database.has_key(uname):
        del database[uname]   # more efficient than database.pop(uname)

def read():
    reader = csv.reader(open('data/profiles.csv', 'rb'))
    

def query(parameters):
    """Retrieves data based on parameters"""
    # TODO: can we allow for the user to give gmail-like queries? (boolean)
    # Ex: 
    # 1) people living in bangalore AND know python
    # 2) people living in bangalore OR mumbai

    resultset = dict()
    for profile in database:
        # @valid flag => keeps track of whether the profile satisfies ALL criteria
        valid = True
        for param in parameters:
            # @parameters is a dictionary containing all the query keys which are hashed to the expected values
            # Ex: For a query like "People who live in bangalore", would give a parameter dict of {"location": "Bangalore"}
            if profile.has_key(param) and profile[param].find(parameters[param]) == -1:
                # We are checking for return value of find() rather than matching with == because the values for fields in different profiles
                # are not consistent - some may have "Bangalore", some others "Bangalore, Karnataka, India", where direct matching would fail
                # with the second one
                # TODO: How to handle someone who has set his locality value to "Bengaluru" (think of similar cases)?
                valid = False # The profile has the field, and it doesn't match
                break
            else:
                # We need a second flag because the user might not have filled in that detail in his profile
                # So, we parse through his complete list of details and find out whether there's a mention of the particular value
                # anywhere at all in his profile
                valid = False
                for field in profile:
                    if profile[field].find(parameters[param]) != -1:
                        # The term exists in his profile somewhere
                        valid = True
                        break

        if valid:
            # There might be more than one profile that match the criteria
            resultset[profile] = database[profile]

    return resultset
                    
def display():
    """Displays the contents of the database on console (For testing purposes only)"""
    for professional, details in database.items():
        for field, description in details.items():
            print field,":",description
        print "="*100

if __name__ == '__main__':
    while True:
        choice = raw_input("""
            Enter a choice
            1: Create
            2: Delete
            3: Query
            4: Display
            5: Write existing database to file
            """)
        if int(choice) == 1:
            resumelist = datacollector.collect()
            for name, details in resumelist.items():
                create(name, details)

        elif int(choice) == 2:
            name = raw_input("Enter uname of the profile to delete")
            delete(name)

        elif int(choice) == 3: # TODO
            pass

        elif int(choice) == 4:
            display()

        elif int(choice) == 5:
            dbfile = open('data/profiles.csv', 'wb')
            writer = csv.writer(dbfile)
            for key, value in database.items():
                # TODO: Devise a better method to store the value which is also a dictionary
                dets = []
                for field, fieldval in value.items():
                    dets.append((field, fieldval))
                writer.writerow([key, dets])
            dbfile.close()

        else:
            print "Enter a valid choice"

        quit = raw_input("Another operation? ")
        if quit.find('y') == -1 and quit.find('1') == -1: # The tester can either give just 'y' or 'yes' or '1'
            break
