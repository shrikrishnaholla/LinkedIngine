#!/usr/bin/python
"""This is an in-memory database engine
It should support CRUD (Create, Retrieve, Update, Delete operations)
"""
# curl -XGET https://api.github.com/users/shrikrishnaholla/repos|grep -i python => for reference for future use
import csv
database = dict()
def create(uname, details):
    """Create an entry to the database of LinkedIN profiles"""
    if database.has_key(uname):
        # TODO: don't print; this has to act as an api - not a console application
        # TODO: preferably use get()
        print "Profile for", uname, "already exists in database"
    else:
        database[uname] = details
        # TODO: Avoid printing to console
        print "Profile of", uname, "added to the database"

def update(uname, updates):
    """Update profiles' data"""
    # TODO: preferably use get()
    if database.has_key(uname):
        for key in updates.keys:
            database[uname][key] = updates[key]
    else:
        create(uname, updates)

def delete(uname):
    """Delete profile"""
    # TODO: use get()
    if database.has_key(uname):
        database.pop(uname)

def query(parameters):
    """Retrieves data based on parameters"""
    # TODO: can we allow for the user to give gmail-like queries? 
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
            resultset[profile] = database[profile]

    return resultset
                    
def display():
    """Displays the contents of the database (For testing purposes only)"""
    for professional, details in database.items():
        for field, description in details.items():
            print field,":",description
        print "="*50

if __name__ == '__main__':
    while True:
        choice = raw_input("""
            Enter a choice
            1: Create
            2: Update
            3: Delete
            4: Query
            5: Display
            """)
        if int(choice) == 1:
            # TODO: Once webscraping_demo is fixed and make api - like, can be moved to the top of the page
            import webscraping_demo
            for profile in webscraping_demo.links: # TODO: variables musn't be global - functions must return them
                create(profile[:profile.index('/')], webscraping_demo.d) # take the username and remove the /xxx/yyy/zzz numbers

            writer = csv.writer(open('data/profiles.csv', 'wb'))
            for key, value in database.items():
                # TODO: Devise a better method to store the value which is also a dictionary
                writer.writerow([key, value])
            
        elif int(choice) == 2: # TODO
            pass
        elif int(choice) == 3:
            name = raw_input("Enter uname of the profile to delete")
            delete(name)
        elif int(choice) == 4: # TODO
            pass
        elif int(choice) == 5: # TODO
            display()
        else:
            print "Enter a valid choice"

        quit = raw_input("Another operation? ")
        if quit.find('y') == -1 and quit.find('1') == -1: # The tester can either give just 'y' or 'yes' or '1'
            break
