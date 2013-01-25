from getProfileAuthToken import GetProfileAuthToken
import facebook

#friendList is a list of FacebookUser objects. This method calculates the number of mutual friends the profile object
#shares with each friend in FriendList and orders friendList by the this number in descending order
def OrderByNumberOfMutualFriends(profile,friendList):
    if len(friendList) < 1:
        print "friendlist most not be empty"
        return friendList
    graph = facebook.GraphAPI(GetProfileAuthToken(profile))
    idsString = ""
    facebookUserDict = {}
    for friend in friendList[0:len(friendList)-1]:
        idsString = idsString + friend.facebookID + ","
        facebookUserDict[friend.facebookID] = friend
    lastFriend = friendList[-1]
    idsString = idsString + lastFriend.facebookID
    facebookUserDict[lastFriend.facebookID] = lastFriend

    query = "SELECT uid,mutual_friend_count FROM user WHERE uid IN (%s) ORDER BY mutual_friend_count DESC" % idsString
    numMutualFriendList =  graph.fql(query)
    orderedFriendList = []
    for friendData in numMutualFriendList:
        id = str(friendData["uid"])
        orderedFriendList.append(facebookUserDict[id])
    return orderedFriendList