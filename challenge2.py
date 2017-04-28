'''
author: Ofir Dubi
date: 25/4/2017
description: a function that receives 3 names, and returns the number of different people these names represents.
I found an online nickname database, containing thousands of different names.
im using a Fuzzy Logic based library -  fuzzywuzzy  to determent if a name has a typo in it.
The fuzzzywuzzy function i use is fuzz.ration(str1, str2) - it returns a number between 0-100 that represents the similarity of the strings.
after many testing, iv'e decided to accept strings with a similarity level of over 67 - 67 allows typo's in strings the length of 3,
but doesn't allow to many typo's in other strings.
for the middle names, i decided that if both people specify their middle name and they both have different middle names - they are not the same person.
i used fuzz.partial_ratio(str1, str2) function for middle names. it's like the ratio() function, but if one string is a substring of the other string
it accepts it. for example, fuzz.ratio("brown", "brown charlie") = 56; fuzz.partial_ratio("brown", "brown charlie") = 100
i chose to accept values over 75 - to accept typo's

'''


import collections
import csv
import operator
import functools
from fuzzywuzzy import fuzz

# NickNameData is an object that represents the nickname's database
class NicknameData(object):
    def __init__(self, filename=None):
        filename = filename or 'names.csv'
        lookup = collections.defaultdict(list)
        #read from the nickname database
        with open(filename) as f:
            reader = csv.reader(f)
            for line in reader:
                matches = set(line)
                for match in matches:
                    lookup[match].append(matches)
        self.lookup = lookup

    def __getitem__(self, name):
        name = name.lower()
        if name not in self.lookup:
            raise KeyError(name)
        names = functools.reduce(operator.or_, self.lookup[name])

        return names

    def getFuzzyNicknames(self, name):
        name = name.lower()
        try:
            names = list(filter(lambda nickname: fuzz.ratio(name, nickname)>=67, self.lookup))
            names = [functools.reduce(operator.or_, self.lookup[name]) for name in names]

            return names
        except KeyError:

            return None

#a function that decides if 2 names represent the same person, based on a list of nicknames
def samePeople(nicknames, LastName, secondName, secondLastName, billMiddleName = " ", shipMiddleName  = " "):
    #checks if the second name matchs any of the first name possible nickname
    return any(fuzz.ratio(secondName, nickname)>=67 for groups in nicknames for nickname in groups) and fuzz.ratio(LastName, secondLastName) >= 67 and fuzz.partial_ratio(billMiddleName, shipMiddleName) > 75

#the main function, counts the number of unique names
def countUniqueNames(billFirstName,billLastName, shipFirstName, shipLastName,billNameOnCard):
    nicknameData = NicknameData()
    uniqueNames = 1
    billMiddleName = " "
    shipMiddleName = " "
    billFirstName = billFirstName.split(" ", 1) #get read of the middle name
    shipFirstName = shipFirstName.split(" ", 1) #get read of the middle name
    if len(billFirstName)>=2 and len(shipFirstName)>=2: #consider middle names only if both of them have middle names
        billMiddleName = billFirstName[1]
        shipMiddleName = shipFirstName[1]

    firstNameOnCard = billNameOnCard.split(" ", 1)[0]
    lastNameOnCard = billNameOnCard.split(" ", 2)[1]

    bill_possible_names = nicknameData.getFuzzyNicknames(billFirstName[0])

    print("billMiddleName: " +billMiddleName  + " shipMiddleName: " + shipMiddleName )
    if samePeople(bill_possible_names, billLastName, shipFirstName[0], shipLastName, billMiddleName, shipMiddleName):

        # billing and shipment are the same person
        if( not samePeople(bill_possible_names, billLastName, firstNameOnCard, lastNameOnCard)
            and not samePeople(bill_possible_names, billLastName,lastNameOnCard, firstNameOnCard)):
            #billing and shipment are the same, card is different
            uniqueNames +=1

    else:
        # billing and shipment are 2 different people
        uniqueNames += 1

        ship_possible_names = nicknameData.getFuzzyNicknames(shipFirstName[0])
        if( not samePeople(bill_possible_names, billLastName, firstNameOnCard, lastNameOnCard)
            and not samePeople(bill_possible_names, billLastName,lastNameOnCard, firstNameOnCard)
           and not samePeople(ship_possible_names, shipLastName, firstNameOnCard, lastNameOnCard)
           and not samePeople(ship_possible_names, shipLastName, lastNameOnCard, lastNameOnCard)):
            uniqueNames+=1
    return uniqueNames

#test cases:

res = countUniqueNames("Deborah mekonhey","Egli","Deborah zipora","Egli","Deborah Egli") #returns 2
print("result iss: "+ str(res))
res = countUniqueNames("nenjamin","brown","benjamin","brow","benn brown") #returns 1
print("result is: "+ str(res))
res = countUniqueNames("Deborah","Egli","Deborah","Egli","Deborah Egli") #returns 1
print("result is: "+ str(res))
res = countUniqueNames("Deborah","Egli","Debbie","Egli","Debbie Egli") #returns 1
print("result is: "+ str(res))
res = countUniqueNames("Deborah","Egni","Deborah","Egli","Deborah Egli") #returns 1
print("result is: "+ str(res))
res = countUniqueNames("Deborah S","Egli","Deborah","Egli","Egli Deborah") #returns 1
print("result is: "+ str(res))
res = countUniqueNames("Michele","Egli","Deborah","Egli","Michele Egli") #returns 2
print("result is: "+ str(res))
res = res = countUniqueNames("ofir","brown","itay","brow","debbie gold") #returns 3
print("result is: "+ str(res))


print(fuzz.partial_ratio("brown", "brown charlie"))