from connect.functions.getProfileAuthToken import GetProfileAuthToken
from connect.classes.goodFriendsResponse import GoodFriendsResponse
from connect.functions.getFriendList import GetFriendList
from connect.models import PotentialMatch
import facebook

# Returns the friends which profile.facebookID shares most mutual friends with in particular location
# limit is the number of friends you want to return
def GetGoodFriendsForInvites(profile, limit):
    graph = facebook.GraphAPI(GetProfileAuthToken(profile))
    query = "SELECT uid, name, mutual_friend_count FROM user WHERE uid IN (SELECT uid1 FROM friend WHERE uid2 =" + profile.facebookID + ") AND '" + profile.state + "' IN current_location AND NOT is_app_user ORDER BY mutual_friend_count DESC LIMIT " + str(limit)
    goodFriends = graph.fql(query)
    for goodFriend in goodFriends:
        goodFriend['friendIncrease'] = generateFakePotentialFriendIncrease(goodFriend['name'])
    return GoodFriendsResponse(goodFriends, len(GetFriendList(profile)), PotentialMatch.objects.filter(profile=profile).count())


def generateFakePotentialFriendIncrease(name):
    vowelCount = 0
    specialLetterCount = 0
    multiplier = 20
    for letter in name:
        if letter in ['a', 'e', 'i', 'o', 'u']:
            vowelCount += 1
        if letter in ['r', 's', 't', 'l', 'z']:
            specialLetterCount += 1

    return multiplier * vowelCount + specialLetterCount


