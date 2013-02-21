from connect.models import Profile,Friendship,FacebookUser
from getProfileAuthToken import GetProfileAuthToken
import facebook

# use kwargs to set friendlist limits and offsets for updating parts of the friend list. this can be used for quickly
# updating a subset of the friendlist when time is of the essence and the entire friendlist isn't needed.
# Note: if kwargs is empty then it updates the entire friendlist with no limit
# e.g. 1 update friendlist with at most 50 of the user's friends):
# UpdateFriendList(profile,**{"limit" : 50})
# e.g. 2 update friendlist with limit and offset
# UpdateFriendList(profile, **{limit" : 10, "offset" : 10})
def UpdateFriendList(profile,**kwargs):
    try:
        friendListData = getFriendListFromFacebook(profile,**kwargs)
        for friend in friendListData:
            facebookUser = createOrUpdateFacebookUser(friend)
            friendship = createOrUpdateFriendShip(profile,facebookUser)
        return True
    except:
        return False

def getFriendListFromFacebook(profile,**kwargs):
    graph = facebook.GraphAPI(GetProfileAuthToken(profile))
    fields = ['name','location','picture','gender','birthday','relationship_status']
    kwargs['fields'] = fields
    # kwargs = {"fields": fields, "limit" : limit}
    friendList = graph.get_connections("me","friends",**kwargs)['data']
    return friendList


def createOrUpdateFacebookUser(friendFacebookData):
    facebookUser, created = FacebookUser.objects.get_or_create(
        facebookID = friendFacebookData['id']
    )
    facebookUser.updateUsingFacebookDictionary(friendFacebookData)
    facebookUser.save()
    return facebookUser

def createOrUpdateFriendShip(profile,facebookUser):
    friendship, created = Friendship.objects.get_or_create(
    user = profile,friend = facebookUser)
    return friendship
