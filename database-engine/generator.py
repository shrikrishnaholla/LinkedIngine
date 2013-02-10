#!/usr/bin/python
from random import randint as ri
mail = ['gmail', 'yahoo', 'outlook']
place = ['Bangalore', 'Delhi', 'Mumbai', 'Kolkata', 'Chennai', 'Pune']
field = ['Software', 'Computer Science', 'Information Technology', 'Computers', 'Software Engineering']
position = ['Director', 'Section Head', 'Project Head', 'Team Leader', 'Software Engineer']
company = ['Microsoft', 'Google', 'Adobe', 'Infosys', 'Wipro', 'SAP', 'Mindtree', 'Cisco', 'Thoughtworks', 'IBM', 'McAfee', \
'Mozilla', 'Canonical', 'Novell', 'HP', 'Lenovo', 'Asus', 'Dell', 'Toshiba']
degree = ['BE', 'BTech', 'MS', 'MTech', 'PhD']
college = ['IIT', 'IISc', 'NIT', 'PESIT']
skillset = ['Python', 'C', 'C++', 'Java', 'Ruby', 'JavaScript', 'Scala', 'Erlang', 'PHP', 'HTML5', 'CSS3', 'MySQL', 'MongoDB']

def generate():
    """Generate profile data for creating test database"""
    fname = ''
    for i in xrange(0,ri(3,10)):
        fname += chr(ri(97,122))

    lname =''
    for i in xrange(0,ri(3,10)):
        lname += chr(ri(97,122))

    uname = fname+'-'+lname+'/'+str(ri(0,999))+'/'+str(ri(0,999))+'/'+str(ri(0,999))+'/'
    # Public LinkedIn public profile link template

    email = fname+'.'+lname+'@'+mail[ri(0,len(mail)-1)]+'.com'
    locality = place[ri(0,len(place)-1)]
    industry = field[ri(0,len(field)-1)]
    current = position[ri(0,len(position)-1)] + ' at ' + company[ri(0,len(company)-1)]
    past = []
    for i in xrange(0,ri(0,5)):
        past.append(position[ri(0,len(position)-1)] + ' at ' + company[ri(0,len(company)-1)])
    education = []
    for i in xrange(0,ri(0,3)):
        education.append(degree[ri(0,len(degree)-1)] + ' at ' + college[ri(0,len(college)-1)])
    skills = []
    for i in xrange(0,ri(1,len(skillset)-1)):
        skills.append(skillset[ri(0,len(skillset)-1)])

    projectdescriptions = []
    for i in xrange(0,ri(0,3)):
        desc = ''
        for j in xrange(0,ri(20,100)):
            choice = ri(0,100)
            if choice % 10 == 0:
                desc += skillset[ri(0,len(skillset)-1)]
            elif choice % 20 == 0:
                desc += ' when I was working as ' + past[ri(0,len(past)-1)]
            else:
                word = ''
                for k in xrange(1,ri(1,7)):
                    word += chr(ri(97,122))
                desc += word
        projectdescriptions.append(desc)

    profile = dict()
    details = dict()
    profile[uname] = details
    details['fname'] = fname
    details['lname'] = lname
    details['email'] = email
    details['locality'] = locality
    details['industry'] = industry
    details['current'] = current
    details['past'] = past
    details['education'] = education
    details['skills'] = skills
    details['project-descriptions'] = projectdescriptions

    return profile