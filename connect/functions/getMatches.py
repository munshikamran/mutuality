from getFriendList import GetFriendList
from connect.classes import FriendMatch
import random

def GetNewMatch(profile,gender1,gender2):
    person1 = getRandomFriend(profile,gender1)
    friendMatch = GetNewMatchIncludingPerson(profile,person1,gender2)
    return friendMatch

def GetNewMatchIncludingPerson(profile,person,genderOtherPerson):
    friendsInSameState = getPotentialsForPersonInSameState(profile,person,genderOtherPerson)
    if friendsInSameState.exists():
        otherPerson = randomElementFromList(friendsInSameState)
        return FriendMatch(person,otherPerson)
    friendList = getPotentialsForPerson(profile,person,genderOtherPerson)
    otherPerson = randomElementFromList(friendList)
    return FriendMatch(person,otherPerson)

#helper functions
def getRandomFriend(profile,gender):
    friendList = GetFriendList(profile).filter(gender=gender)
    randomFriend = randomElementFromList(friendList)
    return randomFriend

def getPotentialsForPerson(profile,person,genderOtherPerson):
    friendList = GetFriendList(profile).filter(gender=genderOtherPerson).exclude(facebookID=person.facebookID)
    return friendList

def getPotentialsForPersonInSameState(profile,person,genderOtherPerson):
    friendList = GetFriendList(profile).filter(state=person.state,gender=genderOtherPerson).exclude(facebookID=person.facebookID)
    return friendList

def randomElementFromList(aList):
    return aList[random.randint(0,len(aList)-1)]
