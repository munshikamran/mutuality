from connect.functions.getMutualityUsers import GetNonFriendUsersInArea
from connect.functions.getFriendsOfFriends import GetFriendsOfFriendsInArea
from connect.functions.getNumberOfMutualFriends import GetNumberOfMutualFriends
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

    freshUsers = FacebookUser.objects.filter(facebookID__in=list(combinedUserIDSet))
#     create  a list of ids for all users so we can get the mutual friend counts
    userDictionary = {}
    for freshUser in freshUsers:
        userDictionary[freshUser.facebookID] = freshUser
    mutualFriendCounts = GetNumberOfMutualFriends(profile, userDictionary.keys())
    potentialMatches = []
    if len(mutualFriendCounts) < 1:
        return 'no potential matches were found'
    potentialMatchUpdate = PotentialMatchUpdate(profile=profile)
    potentialMatchUpdate.save()
    for result in mutualFriendCounts:
        facebookID = str(result['uid'])
        facebookUser = userDictionary[facebookID]
        mutualFriendCount = result['mutual_friend_count']
        isMutualityConnection = facebookID in mutualityUserIDSet
        potentialMatch = PotentialMatch(profile=profile, facebookUser=facebookUser, numMutualFriends=mutualFriendCount, potentialMatchUpdate=potentialMatchUpdate, isMutualityConnection=isMutualityConnection)
        potentialMatches.append(potentialMatch)
    bulkSave(potentialMatches)



def bulkSave(potentialMatches):
    bulkSize = 500
    for i in range(len(potentialMatches)/bulkSize+1):
        startIdx = i*bulkSize
        stopIdx = (i+1)*bulkSize
        PotentialMatch.objects.bulk_create(potentialMatches[startIdx:stopIdx])





