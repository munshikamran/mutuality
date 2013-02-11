from connect.models import Friendship
from connect.models import FacebookUser
from getFriendList import GetFriendIDs
from common.enums import RELATIONSHIP_STATUS
def GetFriendsOfFriends(profile):
    friendIDs = GetFriendIDs(profile)
    friendshipsOfFriends = list(Friendship.objects.filter(user__in=friendIDs).exclude(friend__in=friendIDs+[profile.facebookID]).values_list('friend'))
    friendsOfFriendsIDs = []
    for friendship in friendshipsOfFriends:
        friendsOfFriendsIDs.append(friendship[0])

    friendsOfFriendsList = FacebookUser.objects.filter(facebookID__in=friendsOfFriendsIDs)
    return friendsOfFriendsList

def GetFriendsOfFriendsInArea(profile):
    fofInArea = GetFriendsOfFriends(profile).filter(state = profile.state)
    return fofInArea

def GetFriendsOfFriendsSingleInArea(profile):
    fofInArea = GetFriendsOfFriendsInArea(profile)
    genderToExclude = profile.gender
    relationshipStatusesToExclude = [RELATIONSHIP_STATUS.RELATIONSHIP,RELATIONSHIP_STATUS.ENGAGED,RELATIONSHIP_STATUS.MARRIED]
    fofSingleInArea = fofInArea.exclude(gender=genderToExclude).exclude(relationshipStatus__in=relationshipStatusesToExclude)
    return fofSingleInArea


