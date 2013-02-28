from connect.models import Profile,Friendship,FacebookUser
from getProfileAuthToken import GetProfileAuthToken
import facebook
import time
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
    try:
        facebookUsers = []
        friendships = []
        facebookIDs = []
        start_time = time.time()
        friendListData = getFriendListFromFacebook(profile,**kwargs)
        elapsed_time = time.time() - start_time
        print "%f seconds to return from facebook" % elapsed_time
        start_time = time.time()
        for friend in friendListData:
            facebookIDs.append(friend['id'])
            facebookUser = createFacebookUser(friend)
            facebookUsers.append(facebookUser)
            start_time1 = time.time()
            friendship = createFriendShip(profile,facebookUser)
            friendships.append(friendship)
            elapsed_time1 = time.time() - start_time1
            print "%f seconds to create friendship" % elapsed_time1
        elapsed_time = time.time() - start_time
        FacebookUser.objects.filter(pk__in=facebookIDs).delete()
        print "deleted"
        Friendship.objects.filter(user=profile,friend__in=facebookIDs).delete()
        print "deleted"
        bulkSave(facebookUsers,friendships)
        print "%f seconds to process all" % elapsed_time
        return True
    except:
        print "Unexpected error:", sys.exc_info()
        return False

def getFriendListFromFacebook(profile,**kwargs):
    graph = facebook.GraphAPI(GetProfileAuthToken(profile))
    fields = ['name','location','picture','gender','birthday','relationship_status']
    kwargs['fields'] = fields
    # kwargs = {"fields": fields, "limit" : limit}
    friendList = graph.get_connections("me","friends",**kwargs)['data']
    return friendList


def createFacebookUser(friendFacebookData):
    start_time1 = time.time()
    # facebookUser, created = FacebookUser.objects.get_or_create(
    #     facebookID = friendFacebookData['id']
    # )
    facebookUser = FacebookUser(facebookID = friendFacebookData['id'])
    elapsed_time1 = time.time() - start_time1
    print "%f seconds to get or create fb user" % elapsed_time1
    start_time1 = time.time()
    facebookUser.updateUsingFacebookDictionary(friendFacebookData)
    # facebookUser.save()
    elapsed_time1 = time.time() - start_time1
    print "%f seconds to update user" % elapsed_time1
    return facebookUser

def createFriendShip(profile,facebookUser):
    # friendship, created = Friendship.objects.get_or_create(
    # user = profile,friend = facebookUser)
    friendship = Friendship(user = profile,friend = facebookUser)
    return friendship

def bulkSave(facebookUsers,friendships):
    bulkSize = 500
    for i in range(len(facebookUsers)/bulkSize+1):
        startIdx = i*bulkSize
        stopIdx = (i+1)*bulkSize
        FacebookUser.objects.bulk_create(facebookUsers[startIdx:stopIdx])
        Friendship.objects.bulk_create(friendships[startIdx:stopIdx])


