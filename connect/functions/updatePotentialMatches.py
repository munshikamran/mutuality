from connect.functions.getMutualityUsers import GetNonFriendUsersInArea
from connect.functions.getFriendsOfFriends import GetFriendsOfFriendsInArea
from connect.functions.getNumberOfMutualFriends import GetNumberOfMutualFriends
from connect.models import Profile
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
        print 'no potential matches were found'
        return []
    existingPotentialMatches = set(PotentialMatch.objects.filter(profile=profile).values_list('facebookUser_id', flat=True))
    for result in mutualFriendCounts:
        facebookID = str(result['uid'])
        mutualFriendCount = result['mutual_friend_count']
        if (not facebookID in existingPotentialMatches) and mutualFriendCount > 0:
            facebookUser = userDictionary[facebookID]
            isMutualityConnection = facebookID in mutualityUserIDSet
            potentialMatch = PotentialMatch(profile=profile, facebookUser=facebookUser,
                                            numMutualFriends=mutualFriendCount,
                                            isMutualityConnection=isMutualityConnection)
            potentialMatches.append(potentialMatch)
    bulkSave(potentialMatches)
    potentialMatchUpdate = PotentialMatchUpdate(profile=profile)
    potentialMatchUpdate.save()
    # TODO also update existing potential matches

    # update isMutualityConnection
    profileIDs = Profile.objects.all().values_list('facebookID', flat=True)
    PotentialMatch.objects.filter(facebookUser__in=profileIDs).update(isMutualityConnection=True)
    return potentialMatches



def bulkSave(potentialMatches):
    bulkSize = 500
    for i in range(len(potentialMatches)/bulkSize+1):
        startIdx = i*bulkSize
        stopIdx = (i+1)*bulkSize
        print '{0} batch len={1}'.format(i, len(potentialMatches[startIdx:stopIdx]))
        PotentialMatch.objects.bulk_create(potentialMatches[startIdx:stopIdx])





