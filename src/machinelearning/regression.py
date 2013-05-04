#!/usr/bin/python
import dbinterface
import Orange
import re
import skillregressor

TABLE_NAME = 'ProfileTable.tab'

bestenggcolleges = open('data/bestcolleges.engg').readlines()
bestbcolleges    = open('data/bestcolleges.b').readlines()

bestenggcolleges.reverse()
bestbcolleges.reverse()

bestenggcolleges = [college.strip('\n') for college in bestenggcolleges]
bestbcolleges = [college.strip('\n') for college in bestbcolleges]

skills = dict()

def readSkillsFromFiles():
    """Read already learnt skills from the files"""
    skills['web']                  = open('data/skills/web', 'r').readlines()
    skills['mobile']               = open('data/skills/mobile', 'r').readlines()
    skills['research']             = open('data/skills/research', 'r').readlines()
    skills['management']           = open('data/skills/management', 'r').readlines()
    skills['networks']             = open('data/skills/networks', 'r').readlines()
    skills['software_engineering'] = open('data/skills/software_engineering', 'r').readlines()
    skills['uncategorized']        = open('data/skills/uncategorized', 'r').readlines()

readSkillsFromFiles()

for skill in skills.keys():
    skills[skill] = [item.strip('\n') for item in skills[skill]]

# Initialization of the orange table
domains = [Orange.feature.Continuous('experience'), Orange.feature.Discrete('education')]
domains.extend([Orange.feature.Continuous(skill) for skill in skills.keys()])
Domain = Orange.data.Domain(domains)

table = Orange.data.Table(Domain)
table.save(TABLE_NAME)

def regresser():
    """Compute regression on ALL profiles in the database
    [TODO]: Allow computation on a selective portion of the database"""
    for profile in dbinterface.collection.find():
        # Regression
        totalexperience = 0
        totaleducation  = 0
        # The value for experience will just be the decimal value of total number of years worked
        for experience in profile['experience']:
            if type(experience) == dict:
                totalexperience += experience.get('years', 0)
                totalexperience += 0.01 * (experience.get('months', 0) * 8.33) # = 100/12

        # Value for education will be based on the ranking of the college
        # The rankings have been obtained from a website
        # Higher ranking == greater value
        for college in profile['colleges']:
            for bestenggcollege in bestenggcolleges:
                if re.search(college, bestenggcollege):
                    totaleducation += bestenggcolleges.index(bestenggcollege)+1
            for bestbcollege in bestbcolleges:
                if re.search(college, bestbcollege):
                    totaleducation += bestbcolleges.index(bestbcollege)+1

        # Compute skill regression value
        skillindex = skillregressor.computeSkillRegression(profile, skills)
        for skill in skills.keys():
            if skill not in skillindex.keys():
                skillindex[skill] = 0
        readSkillsFromFiles()
        data = [totalexperience, totaleducation]
        data.extend([value for value in skillindex.values()])
        table.append(data)

        print 'Experience:', totalexperience, '\nEducation', totaleducation
        for skill in skillindex.keys():
            print skill, ':', skillindex[skill]

        dbinterface.collection.update({'public_profile_url':profile['public_profile_url']},
                                        {'$set': {
                                                    'experienceindex': totalexperience,
                                                    'educationindex' : totaleducation,
                                                    'skillindex'     : skillindex
                                                  }})

    table.save(TABLE_NAME)

    learner = Orange.regression.linear.LinearRegressionLearner()
    classifier = learner(table)

    print classifier

if __name__ == '__main__':
    regresser()