import scraper
import categorizer

def computeSkillRegression(profile, skills):
    """Compute skill regression value"""
    skillindex = dict()
    for item in profile['skills']:
        skillFlag = False
        for category, topics in skills.items():
            if item in topics: # If the skill is already present in one of our lists
                skillindex[category] = skillindex.get(category, 0) + 100.0/len(profile['skills'])
                skillFlag = True
        if not skillFlag:
            # if not, get related skills from the relevant linkedin page
            relatedskills = scraper.extractRelatedSkills(item)
            categorycount = dict()
            for relskill in relatedskills:
                for category, topics in skills.items():
                    if relskill in topics:
                        categorycount[category] = (categorycount.get(category, 0) + 1)
                        break
                else:
                    # if none of the related skills are present in any of the lists,
                    # go the extra mile and make a wild guess on which category it might belong to
                    category = categorizer.categorize(relskill)
                    categorycount[category] = (categorycount.get(category, 0) + 1)

            try:
                # Guess the closest category the related skills might belong to
                closestcategory = categorycount.keys()[categorycount.values().index(max(categorycount.values()))]
                writeback(closestcategory, relatedskills)
                skillindex[closestcategory] = skillindex.get(closestcategory, 0) + (100.0/len(profile['skills']))
            except:
                pass
    return skillindex

def writeback(category, relatedskills):
    skillfile = open('data/skills/'+category, 'a')
    for skill in relatedskills:
        skillfile.write(skill+'\n')
    skillfile.close()
