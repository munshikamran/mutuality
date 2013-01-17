from connect.models import Friendship
from connect.models import FacebookUser
from getFriendList import GetFriendIDs

def GetFriendsOfFriends(profile):
    friendIDs = GetFriendIDs(profile)
    friendsOfFriends = Friendship.objects.filter(user__in=friendIDs).exclude(friend__in=friendIDs + [profile.facebookID])
    return friendsOfFriends

