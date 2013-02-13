#!/usr/bin/python
"""This module parses the query string and returns a meaningful dictionary of parameters 
that can be used to filter the profiles"""
from random import randint
from random import shuffle
def querystring(sqlstmt, all_profiles):
    fpart = sqlstmt[:sqlstmt.index('[')]

    returnvals = fpart[7:fpart.index('from')]
    return_fields = returnvals.split(',')   # [email,fname]
    return_fields = [field.strip() for field in return_fields]
    
    no_of_results = fpart[fpart.index('from')+5:fpart.index('profiles')]
    no_of_results = no_of_results.strip()
    if not no_of_results == 'all':
        no_of_results = int(no_of_results)     # 5

    # (location=bengaluru;or;(location=bangalore;and;industry = computer science));and;experience<2;or;education<>BE at Pesit
    qs = sqlstmt[sqlstmt.index('[')+1:sqlstmt.index(']')]
    resultset = parse(qs, all_profiles) # all results
    
    resultset.sort()
    templist = list()
    for profile in resultset:
        if profile not in templist:
            templist.append(profile)

    resultset = templist

    shuffle(resultset)

    results = list()
    if len(resultset) > no_of_results:
        for x in xrange(0,no_of_results):
            results.append(resultset.pop(randint(0,len(resultset)-1)))
    else:
        for result in resultset:
            results.append(result)

    templist = list()
    if not return_fields[0] == '*':
        for profile in results:
            temprofile = dict()
            for field in profile:
                if field in return_fields:
                    temprofile[field] = profile[field]
            templist.append(temprofile)
        results = templist

    return results

def parse(qstring, profiles):
    qstring = qstring.strip()
    qstring = qstring.strip(';')
    if qstring[0] == '(' and qstring[-1] == ')' and qstring.find('(',1) == -1:
        qstring = qstring.strip('(')
        qstring = qstring.strip(')')  # removeinstances of "(query)"
    index = qstring.find(';and;')
    if qstring.find(';or;') != -1 and (index == -1 or index > qstring.find(';or;')): 
        index=qstring.find(';or;')    # if 'or' is present and comes before 'and'
    
    if qstring.find('(') > -1 and qstring.find('(') < index:
        ob = qstring.find('(')        # if open braces are present and first one comes before an 'and' or 'or'
        substr = qstring[ob+1:]
        cb=ob+1       # initialize closing braces
        count=0
        for char in substr:
            if char == '(':
                count += 1  # To handle nested braces
            elif char == ')':
                if count == 0:
                    break   # outermost nest
                else:
                    count -= 1
            cb+=1           # To get position of closing brace
        left = qstring[ob:cb+1]
        
        op = qstring[cb+2:]
        if op[:3].lower() == 'and':
            op = 'and'
        elif op[:2].lower() == 'or':
            op = 'or'
        else:
            print "Wrong operator", op
            print "qstring:", qstring, "left: ",left,'right: ',right
            raise ValueError
        right = qstring[qstring.find(';',cb+2)+1:]

        resultset = process(left,op,right,profiles)
    elif index > -1:  # no bracket-business on left side of operator
        left = qstring[:index]
        op = qstring[index+1:qstring.find(';',index+1)]
        right = qstring[qstring.find(';', index+2):]
        resultset = process(left,op,right,profiles)
    if index == -1:
        resultset = evaluate(qstring, profiles)
    return resultset

def process(left, op, right, profiles):
    if left.find('(') != -1:
        resultset = parse(left, profiles)
    else:
        resultset = evaluate(left,profiles)
    if right.find('(') == -1 and right.find(';and;') == -1 and right.find(';or;') == -1:
        if op == 'and':
            resultdict = dict()
            for profile in resultset:
                resultdict[profile['email']] = profile # Dirty hack alert!!
            resultset = evaluate(right, resultdict)

        elif op == 'or':
            templist = evaluate(right, profiles)
            for profile in templist:
                if profile not in resultset:
                    resultset.append(profile)
    else:
        if op == 'and':
            resultdict = dict()
            for profile in resultset:
                resultdict[profile['email']] = profile # Dirty hack alert!!
            resultset = parse(right, resultdict)
        elif op == 'or':
            templist = parse(right, profiles)
            for profile in templist:
                if profile not in resultset:
                    resultset.append(profile)
    return resultset

def evaluate(atomic, profiles):
    atomic = atomic.strip()
    resultset = list()
    if atomic.find('<>') != -1:
        key = atomic[:atomic.find('<>')]
        value = atomic[atomic.find('<>')+2:]
        key.strip();value.strip();
        for profile in profiles:
            if profiles[profile].has_key(key):
                if profiles[profile][key].lower().find(value.lower()) == -1:
                    resultset.append(profiles[profile])

    elif atomic.find('<=') != -1:
        key = atomic[:atomic.find('<=')]
        value = atomic[atomic.find('<=')+2:]
        key.strip();value.strip();
        for profile in profiles:
            if profiles[profile].has_key(key):
                if type(profiles[profile][key]) == int and profiles[profile][key] <= int(value): # check valueerror
                    resultset.append(profiles[profile])

    elif atomic.find('>=') != -1:
        key = atomic[:atomic.find('>=')]
        value = atomic[atomic.find('>=')+2:]
        key.strip();value.strip();
        for profile in profiles:
            if profiles[profile].has_key(key):
                if type(profiles[profile][key]) == int and profiles[profile][key] >= int(value): # check valueerror
                    resultset.append(profiles[profile])

    elif atomic.find('<') != -1:
        key = atomic[:atomic.find('<')]
        value = atomic[atomic.find('<')+1:]
        key.strip();value.strip();
        for profile in profiles:
            if profiles[profile].has_key(key):
                if type(profiles[profile][key]) == int and profiles[profile][key] < int(value): # check valueerror
                    resultset.append(profiles[profile])

    elif atomic.find('>') != -1:
        key = atomic[:atomic.find('>')]
        value = atomic[atomic.find('>')+1:]
        key.strip();value.strip();
        for profile in profiles:
            if profiles[profile].has_key(key):
                if type(profiles[profile][key]) == int and profiles[profile][key] > int(value): # check valueerror
                    resultset.append(profiles[profile])

    elif atomic.find('=') != -1:
        key = atomic[:atomic.find('=')]
        value = atomic[atomic.find('=')+1:]
        key.strip();value.strip();
        for profile in profiles:
            if profiles[profile].has_key(key):
                if type(profiles[profile][key]) == str and profiles[profile][key].lower().find(value.lower()) != -1:
                    resultset.append(profiles[profile])
                elif type(profiles[profile][key]) == int and profiles[profile][key] == int(value):
                    resultset.append(profiles[profile])
            else:
                for profile in profiles:
                    for field in profiles[profile]:
                        if type(profiles[profile][field]) == str and profiles[profile][field].lower().find(value.lower()) != -1:
                            resultset.append(profiles[profile])
                            break

    return resultset