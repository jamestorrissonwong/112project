import path
import string


#converts list into string
def listString(lst):
    result = ""
    for i in lst:
        result += i + " "
    return result



#converts codes text file to dictionary
def codes():
    d = {}
    p = path.absPath()
    with open(p + "/allDefs.txt", "rt") as f:
        all = f.read()
        
    lines = all.split("\n")

    for i in range(len(lines)-1):
        definition = lines[i].split(" ")
        if definition[1] in string.digits:
            d[definition[0] + definition[1]] = listString(definition[2:])
        else:
            d[definition[0]] = listString(definition[1:])
        
    return d
    
#gets defition from code dictionary
def getDefinition(lst):
    flags = ""
    for i in lst:
        flags += i[0]
        
    codesDict = codes()
    
    try:
        meaning = codesDict[flags]
    
    except:
        meaning = ""
    return (flags, meaning)