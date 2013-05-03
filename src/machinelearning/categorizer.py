import nltk

def words(sentence):
    return {'words': tuple(sentence.split())}

skills = dict()
skills['web']                  = open('data/skills/web', 'r').readlines()
skills['mobile']               = open('data/skills/mobile', 'r').readlines()
skills['research']             = open('data/skills/research', 'r').readlines()
skills['management']           = open('data/skills/management', 'r').readlines()
skills['networks']             = open('data/skills/networks', 'r').readlines()
skills['software_engineering'] = open('data/skills/software_engineering', 'r').readlines()
skills['uncategorized']        = open('data/skills/uncategorized', 'r').readlines()

web                  = [(words(skill), 'web') for skill in skills['web']]
mobile               = [(words(skill), 'mobile') for skill in skills['mobile']]
research             = [(words(skill), 'research') for skill in skills['research']]
management           = [(words(skill), 'management') for skill in skills['management']]
networks             = [(words(skill), 'networks') for skill in skills['networks']]
software_engineering = [(words(skill), 'software_engineering') for skill in skills['software_engineering']]

skillset = web + mobile + research + management + networks + software_engineering

classifier = nltk.NaiveBayesClassifier.train(skillset)

def categorize(uncategorizedskill):
    return classifier.classify(words(uncategorizedskill))

if __name__ == '__main__':
    categorizedskills = dict()
    for skill in skills['uncategorized']:
        category = categorize(skill)
        categorizedskills[category] = categorizedskills.get(category, []) + [skill]
    import skillregressor
    for key, value in categorizedskills.items():
        skillregressor.writeback(key, value)