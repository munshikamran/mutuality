from connect.models import Friendship
from connect.models import FacebookUser
from connect.models.profile import Profile
from getFriendList import GetFriendIDs
from common.enums import RELATIONSHIP_STATUS

def GetFriendsOfFriends(profile):
    friendIDs = GetFriendIDs(profile)
    friendsOnMutuality = Profile.objects.filter(facebookID__in=friendIDs)
    friendsOfFriendsIDs = Friendship.objects.filter(user__in=friendsOnMutuality).exclude(friend__in=set(friendIDs).add(profile.facebookID)).values_list('friend_id')
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


