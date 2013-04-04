from connect.models import Profile,Friendship,FacebookUser
from getProfileAuthToken import GetProfileAuthToken
import facebook
import sys
from django.db import connection, transaction


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
    try:
        facebookUsers = []
        friendships = []
        facebookIDs = []
        friendListData = getFriendListFromFacebook(profile,**kwargs)
        for friend in friendListData:
            facebookIDs.append(friend['id'])
            facebookUser = createFacebookUser(friend)
            facebookUsers.append(facebookUser)
            friendship = createFriendShip(profile,facebookUser)
            friendships.append(friendship)

        deleteWithoutCascaseFacebookUsersWithIDs(facebookIDs)
        # we don't have to worry about cascading deletions for Friendship objects
        Friendship.objects.filter(user=profile,friend__in=facebookIDs).delete()
        bulkSave(facebookUsers,friendships)
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

def createFriendShip(profile,facebookUser):
    friendship = Friendship(user = profile,friend = facebookUser)
    return friendship

def bulkSave(facebookUsers,friendships):
    bulkSize = 500
    for i in range(len(facebookUsers)/bulkSize+1):
        startIdx = i*bulkSize
        stopIdx = (i+1)*bulkSize
        FacebookUser.objects.bulk_create(facebookUsers[startIdx:stopIdx])
        Friendship.objects.bulk_create(friendships[startIdx:stopIdx])

# if we do not delete facebook users without cascade then the delete will also delete the friendship objects for other users
def deleteWithoutCascaseFacebookUsersWithIDs(facebookIDs):
    if len(facebookIDs) == 0:
        return
    idString = str(facebookIDs).replace("[","(").replace("]",")")
    sql = 'DELETE FROM connect_facebookuser where facebookid IN {0}'.format(idString)
    cursor = connection.cursor()
    cursor.execute(sql)
    return True


