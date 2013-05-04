from connect.functions.getFriendList import GetFriendList
from connect.models import FacebookUser
from connect.functions.getProfileAuthToken import GetProfileAuthToken
from connect.functions.orderByNumberOfMutualFriends import OrderByNumberOfMutualFriends
import facebook


#get the mutual friendlist between two Mutuality users
def GetMutualFriendList(profile1,profile2):
    friendList1 = GetFriendList(profile1)
    friendList2 = GetFriendList(profile2)
    friendListIntersection = friendList1.filter(pk__in=friendList2)
    return friendListIntersection


#get the mutual friendlist between a Mutuality user and an arbitrary Facebook user
#list is ordered by number of mutual friends shared
def GetMutualFriendListWithFacebookUserID(profile, facebookUserID):
    friendList = []
    try:
        graph = facebook.GraphAPI(GetProfileAuthToken(profile))
        mutualFriendsData = graph.get_connections("me","mutualFriends/"+str(facebookUserID))["data"]
        for friendData in mutualFriendsData:
            facebookUser = FacebookUser(facebookID=friendData["id"])
            #create a facebookUser object but don't save. We don't care about having this in the db
            facebookUser.updateUsingFacebookDictionary(friendData)
            friendList.append(facebookUser)
            friendList = OrderByNumberOfMutualFriends(profile,friendList)
    except:
        print 'error when retrieving mutual friendList'

    return friendList


