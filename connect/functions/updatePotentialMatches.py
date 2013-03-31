from connect.functions import GetNonFriendUsersInArea
from connect.functions import GetFriendsOfFriendsInArea
from connect.functions import GetAllViewedUsers
from connect.functions import GetNumberOfMutualFriends
from connect.models import FacebookUser
from connect.models import PotentialMatch
from connect.models import PotentialMatchUpdate


def UpdatePotentialMatches(profile):
    mutualityUsers = GetNonFriendUsersInArea(profile)
    friendsOfFriends = GetFriendsOfFriendsInArea(profile)
    facebookUserIDSet = set()
    mutualityUserIDSet = set()
    for person in mutualityUsers:
        mutualityUserIDSet.add(person.facebookID)
    for person in friendsOfFriends:
        facebookUserIDSet.add(person.facebookID)

    combinedUserIDSet = facebookUserIDSet.union(mutualityUserIDSet)
    #remove users who have already been seen
    viewedUsers = GetAllViewedUsers(profile)
    viewedUserSet = set()
    for viewedUser in viewedUsers:
        viewedUserSet.add(viewedUser.facebookID)
    combinedUserIDSet = combinedUserIDSet.difference(viewedUserSet)

    freshUsers = FacebookUser.objects.filter(facebookID__in=list(combinedUserIDSet)).exclude(facebookID__in=viewedUsers)
#     create  a list of ids for all users so we can get the mutual friend counts
    userDictionary = {}
    for freshUser in freshUsers:
        userDictionary[freshUser.facebookID] = freshUser
    mutualFriendCounts = GetNumberOfMutualFriends(profile, userDictionary.keys())
    potentialMatches = []
    potentialMatchUpdate = PotentialMatchUpdate(profile=profile)
    potentialMatchUpdate.save()
    for result in mutualFriendCounts:
        facebookID = result['uid']
        facebookUser = userDictionary[str(facebookID)]
        mutualFriendCount = result['mutual_friend_count']
        potentialMatch = PotentialMatch(profile=profile, facebookUser=facebookUser, numMutualFriends=mutualFriendCount, potentialMatchUpdate=potentialMatchUpdate)
        potentialMatches.append(potentialMatch)
    bulkSave(potentialMatches)



def bulkSave(potentialMatches):
    bulkSize = 500
    for i in range(len(potentialMatches)/bulkSize+1):
        startIdx = i*bulkSize
        stopIdx = (i+1)*bulkSize
        PotentialMatch.objects.bulk_create(potentialMatches[startIdx:stopIdx])





