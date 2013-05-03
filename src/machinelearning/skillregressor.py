import scraper
import categorizer

def computeSkillRegression(profile, skills):
    skillindex = dict()
    for item in profile['skills']:
        skillFlag = False
        for category, topics in skills.items():
            if item in topics:
                skillindex[category] = skillindex.get(category, 0) + 100.0/len(profile['skills'])
                skillFlag = True
        if not skillFlag:
            relatedskills = scraper.extractRelatedSkills(item)
            categorycount = dict()
            for relskill in relatedskills:
                for category, topics in skills.items():
                    if relskill in topics:
                        categorycount[category] = (categorycount.get(category, 0) + 1)
                        break
                else:
                    category = categorizer.categorize(relskill)
                    categorycount[category] = (categorycount.get(category, 0) + 1)

            closestcategory = categorycount.keys()[categorycount.values().index(max(categorycount.values()))]
            writeback(closestcategory, relatedskills)
            skillindex[closestcategory] = skillindex.get(closestcategory, 0) + (100.0/len(profile['skills']))
    return skillindex

def writeback(category, relatedskills):
    skillfile = open('data/skills/'+category, 'a')
    for skill in relatedskills:
        skillfile.write(skill+'\n')
    skillfile.close()
