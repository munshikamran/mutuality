from connect.models import Profile,Friendship,FacebookUser
from getProfileAuthToken import GetProfileAuthToken
import facebook
import sys


def UpdateFriendListHasBeenCalled(profile):
    return Friendship.objects.filter(user=profile).exists()

# use kwargs to set friendlist limits and offsets for updating parts of the friend list. this can be used for quickly
# updating a subset of the friendlist when time is of the essence and the entire friendlist isn't needed.
# Note: if kwargs is empty then it updates the entire friendlist with no limit
# e.g. 1 update friendlist with at most 50 of the user's friends):
# UpdateFriendList(profile,**{"limit" : 50})
# e.g. 2 update friendlist with limit and offset
# UpdateFriendList(profile, **{limit" : 10, "offset" : 10})
def UpdateFriendList(profile,**kwargs):
    """

    :param profile:
    :param kwargs:
    :return:
    """
    try:
        facebookIDs = set()
        friendListData = getFriendListFromFacebook(profile,**kwargs)
        friendDataDictionary = {}
        for friend in friendListData:
            facebookIDs.add(friend['id'])
            friendDataDictionary[friend['id']] = friend
        fbUserInDatabase = FacebookUser.objects.filter(facebookID__in=facebookIDs).values_list('facebookID', flat=True)
        fbUserNeedInsert = facebookIDs.difference(fbUserInDatabase)
        friendshipsInDatabase = Friendship.objects.filter(user=profile, friend__in=facebookIDs).values_list('friend', flat=True)
        friendshipNeedInsert = facebookIDs.difference(friendshipsInDatabase)
        facebookUsers = []
        friendships = []
        for facebookID in fbUserNeedInsert:
            facebookUser = createFacebookUser(friendDataDictionary[facebookID])
            facebookUsers.append(facebookUser)
        for facebookID in friendshipNeedInsert:
            friendship = Friendship(user=profile, friend_id=facebookID)
            friendships.append(friendship)

        bulkSave(facebookUsers, friendships)
        # should also go through fbUser in database and update
        return True
    except:
        print "Unexpected error:", sys.exc_info()
        return False

def getFriendListFromFacebook(profile,**kwargs):
    graph = facebook.GraphAPI(GetProfileAuthToken(profile))
    fields = ['name','location','picture','gender','birthday','relationship_status']
    kwargs['fields'] = fields
    friendList = graph.get_connections("me","friends",**kwargs)['data']
    return friendList


def createFacebookUser(friendFacebookData):
    facebookUser = FacebookUser(facebookID = friendFacebookData['id'])
    facebookUser.updateUsingFacebookDictionary(friendFacebookData)
    return facebookUser


def bulkSave(facebookUsers,friendships):
    bulkSize = 500
    for i in range(len(facebookUsers)/bulkSize+1):
        startIdx = i*bulkSize
        stopIdx = (i+1)*bulkSize
        FacebookUser.objects.bulk_create(facebookUsers[startIdx:stopIdx])
    for i in range(len(friendships)/bulkSize+1):
        startIdx = i*bulkSize
        stopIdx = (i+1)*bulkSize
        Friendship.objects.bulk_create(friendships[startIdx:stopIdx])



