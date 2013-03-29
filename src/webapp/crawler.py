import re
import dbinterface
import nltk

def contentExtractor(page, public_profile_url):
    tags = list()
    first_name = descriptionExtractor(page, '<span class="given-name">', "</span>")

    last_name = descriptionExtractor(page, '<span class="family-name">', "</span>")

    headline = descriptionExtractor(page, '<p class="headline-title title" style="display:block">', "</p>")
    tokens = nltk.word_tokenize(str(headline))
    figureOfspeech = nltk.pos_tag(tokens)
    for word in figureOfspeech:
        if word[1] == 'NNP':
            tags.append(word[0])

    locality = descriptionExtractor(page, '<span class="locality">', "</span>")
    tags.append(locality)

    industry = descriptionExtractor(page, '<dd class="industry">','</dd>')
    tags.append(industry)

    description_summary = descriptionExtractor(page, '<p class=" description summary">', '</p>')
    if description_summary:
        description_summary = description_summary.replace('<br>', '')
        description_summary = description_summary.replace('<br/>', '')
        tokens = nltk.word_tokenize(str(description_summary))
        figureOfspeech = nltk.pos_tag(tokens)
        for word in figureOfspeech:
            if word[1] == 'NNP':
                tags.append(word[0])

    degrees = multipleInstanceExtractor(page, '<span class="degree">', '</span>')
    for degree in degrees:
        tags.append(degree)

    majors = multipleInstanceExtractor(page, '<span class="major">', '</span>')
    for major in majors:
        tags.append(major)

    colleges = multipleInstanceExtractor(page, '<h3 class="summary fn org">', '</h3>')
    for college in colleges:
        tags.append(college)

    skills = multipleInstanceExtractor(page, 'class="jellybean">', '</a>')
    for skill in skills:
        tags.append(skill)

    job_titles = multipleInstanceExtractor(page, '<span class="title">', '</span>')
    for job in job_titles:
        tags.append(job)

    companies = multipleInstanceExtractor(page, '<span class="org summary">', '</span>')
    for company in companies:
        tags.append(company)

    profile = {
        'first_name'         : first_name,
        'last_name'          : last_name,
        'headline'           : headline,
        'locality'           : locality,
        'industry'           : industry,
        'description_summary': description_summary,
        'degrees'            : degrees,
        'majors'             : majors,
        'colleges'           : colleges,
        'skills'             : skills,
        'job_titles'         : job_titles,
        'companies'          : companies,
        'tags'               : tags,
        'public_profile_url' : public_profile_url

    }

    if dbinterface.collection.find(profile).count() == 0:
        dbinterface.collection.save(profile)

def descriptionExtractor(page, startTag, endTag):
    splitstring = re.split(startTag, page)
    if len(splitstring) > 1:
        splitstring = splitstring[1]
        content = splitstring[:splitstring.index(endTag)]
        return content.strip().replace('&amp;','&').lower()
    else:
        return None

def multipleInstanceExtractor(page, startTag, endTag):
    instances = re.findall(startTag+r'(?:[a-zA-Z0-9\.-]|[ \n]|[,&;\(\)])*'+endTag, page, re.MULTILINE)
    for instance in instances:
        newinstance = instance.replace(startTag,'').replace(endTag,'').replace('&amp;','&')
        newinstance = newinstance.strip().lower()
        instances[instances.index(instance)] = newinstance
    return instances

if __name__ == '__main__':
    count = 0
    for person in dbinterface.collection.find():
        count+=1
    print count