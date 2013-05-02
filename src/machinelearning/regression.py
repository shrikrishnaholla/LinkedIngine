#!/usr/bin/python
import dbinterface
import Orange
import re

TABLE_NAME = 'ProfileTable.tab'

bestenggcolleges = open('data/bestcolleges.engg').readlines()
bestbcolleges    = open('data/bestcolleges.b').readlines()

bestenggcolleges.reverse()
bestbcolleges.reverse()

bestenggcolleges = [college.strip('\n') for college in bestenggcolleges]
bestbcolleges = [college.strip('\n') for college in bestbcolleges]

skills = dict()
skills['web']                  = open('data/skills/web', 'r').readlines()
skills['mobile']               = open('data/skills/mobile', 'r').readlines()
skills['research']             = open('data/skills/research', 'r').readlines()
skills['management']           = open('data/skills/management', 'r').readlines()
skills['network management']   = open('data/skills/network management', 'r').readlines()
skills['software engineering'] = open('data/skills/software engineering', 'r').readlines()

for skill in skills.keys():
    skills[skill] = [item.strip('\n') for item in skills[skill]]

domains = [Orange.feature.Continuous('experience'), Orange.feature.Discrete('education')]
domains.extend([Orange.feature.Continuous(skill) for skill in skills.keys()])
Domain = Orange.data.Domain(domains)

table = Orange.data.Table(Domain)
table.save(TABLE_NAME)

def regresser():
    for profile in dbinterface.collection.find():
        # Regression
        totalexperience = 0
        totaleducation  = 0
        for experience in profile['experience']:
            if type(experience) == dict:
                totalexperience += experience.get('years', 0)
                totalexperience += 0.01 * (experience.get('months', 0) * 8.33)

        for college in profile['colleges']:
            for bestenggcollege in bestenggcolleges:
                if re.search(college, bestenggcollege):
                    totaleducation += bestenggcolleges.index(bestenggcollege)+1
            for bestbcollege in bestbcolleges:
                if re.search(college, bestbcollege):
                    totaleducation += bestbcolleges.index(bestbcollege)+1

        skillindex = dict()
        for skill, topics in skills.items():
            """numberofskills = 0
                                                for profileskill in profile['skills']:
                                                    pattern = re.compile(profileskill)
                                                    for topic in topics:
                                                        if pattern.search(skill):
                                                            numberofskills += 1
                                                skillindex[skill] = numberofskills * 100.0 / len(topics)"""
            skillindex[skill] = len([item for item in profile['skills'] for topic in topics if topic.find(item) != -1]) * 100.0 / len(topics)

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