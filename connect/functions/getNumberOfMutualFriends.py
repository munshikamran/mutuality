from connect.functions.getProfileAuthToken import GetProfileAuthToken
import facebook


def GetNumberOfMutualFriends(profile, facebookIDList):
    if len(facebookIDList) < 1:
        print "list most not be empty"
        return False
    graph = facebook.GraphAPI(GetProfileAuthToken(profile))
    idsString = ""
    for fbID in facebookIDList[0:len(facebookIDList)-1]:
        idsString = idsString + fbID + ","
    idsString = idsString + facebookIDList[-1]

    query = "SELECT uid,mutual_friend_count FROM user WHERE uid IN (%s)" % idsString
    numMutualFriendList = graph.fql(query)
    return numMutualFriendList