from connect.models import Profile,Friendship,FacebookUser
from getProfileAuthToken import GetProfileAuthToken
import facebook

def UpdateFriendList(profile):
    friendListData = getFriendListFromFacebook(profile)
    for friend in friendListData:
        facebookUser = createOrUpdateFacebookUser(friend)
        friendship = createOrUpdateFriendShip(profile,facebookUser)


def getFriendListFromFacebook(profile):
    graph = facebook.GraphAPI(GetProfileAuthToken(profile))
    fields = ['name','location','picture','gender','birthday','relationship_status']
    kwargs = {"fields": fields}
    friendList = graph.get_connections("me","friends",**kwargs)['data']
    return friendList


def createOrUpdateFacebookUser(friendFacebookData):
    facebookUser, created = FacebookUser.objects.get_or_create(
        facebookID = friendFacebookData['id']
    )
    facebookUser.updateUsingFacebookDictionary(friendFacebookData)
    return facebookUser

def createOrUpdateFriendShip(profile,facebookUser):
    friendship, created = Friendship.objects.get_or_create(
    user = profile,friend = facebookUser)
    return friendship
